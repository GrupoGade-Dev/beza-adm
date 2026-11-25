"""Testes do cliente do Painel (scripts/painel.py) contra um servidor falso.

Rodar: python3 -m unittest discover -s tests -v
"""
import io
import json
import os
import sys
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import painel  # noqa: E402

TOKEN = "beza_" + "A" * 43
RESPOSTAS = {}
VISTAS = []


class Falso(BaseHTTPRequestHandler):
    def do_GET(self):
        VISTAS.append({"caminho": self.path, "auth": self.headers.get("Authorization"), "ua": self.headers.get("User-Agent")})
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            return self._enviar(401, {"message": "Token do Beza ausente ou inválido."})
        rota = self.path.split("?")[0].replace("/api/beza/v1", "")
        codigo, corpo = RESPOSTAS.get(rota, (404, {"message": "nada"}))
        self._enviar(codigo, corpo)

    def _enviar(self, codigo, corpo):
        dados = json.dumps(corpo).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def log_message(self, *_):
        pass


def rodar(argv, env=None):
    saida, erro = io.StringIO(), io.StringIO()
    antigo = dict(os.environ)
    os.environ.update(env or {})
    try:
        with redirect_stdout(saida), redirect_stderr(erro):
            codigo = painel.main(argv)
    finally:
        os.environ.clear()
        os.environ.update(antigo)
    return codigo, saida.getvalue(), erro.getvalue()


class TestePainel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.servidor = HTTPServer(("127.0.0.1", 0), Falso)
        threading.Thread(target=cls.servidor.serve_forever, daemon=True).start()
        cls.url = f"http://127.0.0.1:{cls.servidor.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.servidor.shutdown()

    def setUp(self):
        VISTAS.clear()
        RESPOSTAS.clear()

    def env(self):
        return {"BEZA_PAINEL_URL": self.url, "BEZA_PAINEL_TOKEN": TOKEN}

    def test_consulta_ok_imprime_json_e_manda_a_senha_so_no_cabecalho(self):
        RESPOSTAS["/gade/resumo"] = (200, {"pronto": True, "kpis": {"totalCtr": 3}})
        codigo, saida, erro = rodar(["gade-resumo"], self.env())
        self.assertEqual(codigo, 0, erro)
        self.assertEqual(json.loads(saida)["kpis"]["totalCtr"], 3)
        self.assertEqual(VISTAS[0]["auth"], f"Bearer {TOKEN}")
        self.assertNotIn(TOKEN, VISTAS[0]["caminho"])
        self.assertNotIn(TOKEN, saida + erro)

    def test_parametros_vao_codificados_e_so_os_informados(self):
        RESPOSTAS["/inside/lancamentos"] = (200, {"pagamentos": []})
        rodar(["inside-lancamentos", "--mes", "2026-10", "--pagina", "2"], self.env())
        self.assertIn("mes=2026-10", VISTAS[0]["caminho"])
        self.assertIn("pagina=2", VISTAS[0]["caminho"])
        VISTAS.clear()
        RESPOSTAS["/inside/clientes"] = (200, {"clientes": []})
        rodar(["inside-clientes"], self.env())
        self.assertNotIn("?", VISTAS[0]["caminho"])
        VISTAS.clear()
        rodar(["inside-caixa", "--mes", "x&supervisor=OUTRO"], self.env())
        self.assertIn("mes=x%26supervisor%3DOUTRO", VISTAS[0]["caminho"])
        self.assertNotIn("&supervisor", VISTAS[0]["caminho"])

    def test_403_vira_codigo_2_com_mensagem_do_painel(self):
        RESPOSTAS["/inside/clientes"] = (403, {"message": 'Sem permissão para "Lista de clientes da Inside".'})
        codigo, saida, erro = rodar(["inside-clientes"], self.env())
        self.assertEqual(codigo, 2)
        self.assertEqual(saida, "")
        self.assertIn("Sem permissão", erro)

    def test_senha_errada_vira_codigo_3(self):
        codigo, _, erro = rodar(["eu"], {"BEZA_PAINEL_URL": self.url, "BEZA_PAINEL_TOKEN": "beza_errada"})
        self.assertEqual(codigo, 3)
        self.assertNotIn("beza_errada", erro)

    def test_sem_senha_configurada_vira_codigo_3(self):
        antigo = os.environ.pop("BEZA_PAINEL_TOKEN", None)
        try:
            codigo, _, erro = rodar(["eu"], {"BEZA_PAINEL_URL": self.url})
        finally:
            if antigo:
                os.environ["BEZA_PAINEL_TOKEN"] = antigo
        self.assertEqual(codigo, 3)
        self.assertIn("configure", erro)

    def test_painel_fora_do_ar_vira_codigo_4(self):
        codigo, _, erro = rodar(["eu"], {"BEZA_PAINEL_URL": "http://127.0.0.1:1", "BEZA_PAINEL_TOKEN": TOKEN})
        self.assertEqual(codigo, 4)
        self.assertIn("internet", erro)

    def test_erro_500_do_painel_vira_codigo_5(self):
        RESPOSTAS["/eu"] = (500, {"message": "Erro interno no servidor."})
        codigo, _, _ = rodar(["eu"], self.env())
        self.assertEqual(codigo, 5)

    def test_recusa_enviar_a_senha_por_http_fora_da_maquina(self):
        codigo, _, erro = rodar(["eu"], {"BEZA_PAINEL_URL": "http://painel.exemplo.com", "BEZA_PAINEL_TOKEN": TOKEN})
        self.assertEqual(codigo, 5)
        self.assertIn("https", erro)
        self.assertEqual(VISTAS, [])

    def test_nao_aceita_comando_fora_da_lista(self):
        with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
            painel.main(["apagar-tudo"])


if __name__ == "__main__":
    unittest.main()
