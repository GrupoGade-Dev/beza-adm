"""Testa a ponte MCP (scripts/painel-mcp.sh) de ponta a ponta, falando JSON-RPC por stdio com um Painel falso."""
import json
import os
import subprocess
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = "beza_" + "B" * 43
VISTAS = []
RESPOSTAS = {}


class Falso(BaseHTTPRequestHandler):
    def do_GET(self):
        VISTAS.append({"caminho": self.path, "auth": self.headers.get("Authorization")})
        if self.headers.get("Authorization") != f"Bearer {TOKEN}":
            codigo, corpo = 401, {"message": "Token do Beza ausente ou inválido."}
        else:
            codigo, corpo = RESPOSTAS.get(self.path.split("?")[0].replace("/api/beza/v1", ""), (404, {"message": "nada"}))
        dados = json.dumps(corpo).encode()
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(dados)))
        self.end_headers()
        self.wfile.write(dados)

    def log_message(self, *_):
        pass


def sessao(url, token, mensagens):
    env = {**os.environ, "BEZA_PAINEL_URL": url}
    env.pop("BEZA_PAINEL_TOKEN", None)
    if token is not None:
        env["BEZA_PAINEL_TOKEN"] = token
    entrada = "".join(json.dumps(m) + "\n" for m in mensagens)
    r = subprocess.run(["bash", os.path.join(RAIZ, "scripts", "painel-mcp.sh")], input=entrada, capture_output=True, text=True, env=env, timeout=30)
    return [json.loads(l) for l in r.stdout.splitlines() if l.strip()], r.stderr


def chamada(i, nome, args=None):
    return {"jsonrpc": "2.0", "id": i, "method": "tools/call", "params": {"name": nome, "arguments": args or {}}}


INIT = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "t", "version": "1"}}}
INITIALIZED = {"jsonrpc": "2.0", "method": "notifications/initialized"}


class TesteMcp(unittest.TestCase):
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

    def test_handshake_e_lista_de_ferramentas_somente_leitura(self):
        resp, _ = sessao(self.url, TOKEN, [INIT, INITIALIZED, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}])
        self.assertEqual(resp[0]["result"]["protocolVersion"], "2025-06-18")
        self.assertIn("tools", resp[0]["result"]["capabilities"])
        self.assertEqual(len(resp), 2, "notificação não pode gerar resposta")
        ferramentas = resp[1]["result"]["tools"]
        nomes = {f["name"] for f in ferramentas}
        self.assertEqual(nomes, {"painel_eu", "painel_gade_resumo", "painel_inside_caixa", "painel_inside_lancamentos",
                                 "painel_inside_clientes_resumo", "painel_inside_clientes", "painel_inside_superliga"})
        for f in ferramentas:
            self.assertTrue(f["annotations"]["readOnlyHint"])
            self.assertFalse(f["inputSchema"]["additionalProperties"])

    def test_consulta_devolve_json_e_envia_a_senha_no_cabecalho(self):
        RESPOSTAS["/inside/clientes/resumo"] = (200, {"totalAtivos": 2})
        resp, _ = sessao(self.url, TOKEN, [INIT, chamada(2, "painel_inside_clientes_resumo")])
        resultado = resp[1]["result"]
        self.assertFalse(resultado["isError"])
        self.assertEqual(json.loads(resultado["content"][0]["text"])["totalAtivos"], 2)
        self.assertEqual(VISTAS[0]["auth"], f"Bearer {TOKEN}")
        self.assertNotIn(TOKEN, json.dumps(resp))

    def test_so_repassa_parametros_declarados(self):
        RESPOSTAS["/inside/caixa"] = (200, {"mes": "2026-10"})
        sessao(self.url, TOKEN, [INIT, chamada(2, "painel_inside_caixa", {"mes": "2026-10", "supervisor": "OUTRO", "regional": "X"})])
        self.assertIn("mes=2026-10", VISTAS[0]["caminho"])
        self.assertNotIn("supervisor", VISTAS[0]["caminho"])
        self.assertNotIn("regional", VISTAS[0]["caminho"])

    def test_sem_permissao_vira_erro_legivel_para_o_assistente(self):
        RESPOSTAS["/inside/clientes"] = (403, {"message": 'Sem permissão para "Lista de clientes da Inside".'})
        resp, _ = sessao(self.url, TOKEN, [INIT, chamada(2, "painel_inside_clientes")])
        resultado = resp[1]["result"]
        self.assertTrue(resultado["isError"])
        self.assertIn("Sem permissão", resultado["content"][0]["text"])

    def test_sem_senha_configurada_orienta_a_configurar(self):
        resp, _ = sessao(self.url, None, [INIT, chamada(2, "painel_eu")])
        self.assertTrue(resp[1]["result"]["isError"])
        self.assertIn("configure", resp[1]["result"]["content"][0]["text"])
        self.assertEqual(VISTAS, [])

    def test_ferramenta_inexistente_e_metodo_desconhecido(self):
        resp, _ = sessao(self.url, TOKEN, [INIT, chamada(2, "apagar_tudo"), {"jsonrpc": "2.0", "id": 3, "method": "resources/list"}])
        self.assertTrue(resp[1]["result"]["isError"])
        self.assertEqual(resp[2]["error"]["code"], -32601)

    def test_painel_fora_do_ar_nao_derruba_a_ponte(self):
        resp, _ = sessao("http://127.0.0.1:1", TOKEN, [INIT, chamada(2, "painel_eu"), chamada(3, "painel_eu")])
        self.assertEqual(len(resp), 3)
        self.assertTrue(resp[1]["result"]["isError"] and resp[2]["result"]["isError"])


if __name__ == "__main__":
    unittest.main()
