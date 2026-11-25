#!/usr/bin/env python3
"""Consulta o Painel de Resultados Gade (somente leitura) em nome do Beza.

Uso:
  python painel.py eu                      o que este acesso pode buscar (e o que está bloqueado)
  python painel.py gade-resumo             números gerais de clientes Gade
  python painel.py inside-caixa [--mes AAAA-MM|all]
  python painel.py inside-lancamentos [--mes AAAA-MM|all] [--pagina N]
  python painel.py inside-clientes-resumo
  python painel.py inside-clientes
  python painel.py inside-superliga

Uso de diagnóstico: a senha vem da variável BEZA_PAINEL_TOKEN (o plugin usa a ponte MCP, painel_mcp.py).
A resposta é JSON no stdout. Erros vão para o stderr, em português, e o código de saída diz o motivo:
  0 ok · 2 sem permissão para essa informação · 3 senha do Beza inválida/ausente ·
  4 sem conexão com o Painel · 5 o Painel recusou o pedido ou deu erro.

Quem decide o que cada acesso pode buscar é o servidor do Painel (tela "Acessos do Beza"):
este script não tem como contornar a permissão. A senha nunca é impressa nem aparece na linha de comando.
Só usa a biblioteca padrão do Python (nada para instalar).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

URL_PADRAO = "https://painel.gadeconsultoria.com"
EXPIRA_EM_SEGUNDOS = 60

ROTAS = {
    "eu": "/eu",
    "gade-resumo": "/gade/resumo",
    "inside-caixa": "/inside/caixa",
    "inside-lancamentos": "/inside/lancamentos",
    "inside-clientes-resumo": "/inside/clientes/resumo",
    "inside-clientes": "/inside/clientes",
    "inside-superliga": "/inside/superliga",
}

SAIDA_OK, SAIDA_SEM_PERMISSAO, SAIDA_SENHA, SAIDA_SEM_CONEXAO, SAIDA_ERRO = 0, 2, 3, 4, 5


class ErroBeza(Exception):
    def __init__(self, mensagem, codigo):
        super().__init__(mensagem)
        self.codigo = codigo


def ler_configuracao():
    url = os.environ.get("BEZA_PAINEL_URL") or URL_PADRAO
    token = (os.environ.get("BEZA_PAINEL_TOKEN") or "").strip()
    if not token:
        raise ErroBeza("O Beza ainda não tem a senha do Painel. Rode /plugin configure beza-adm@beza-adm e cole a senha.", SAIDA_SENHA)
    return url.rstrip("/"), token


def validar_url(url):
    partes = urllib.parse.urlparse(url)
    local = partes.hostname in ("localhost", "127.0.0.1", "::1")
    if partes.scheme != "https" and not (partes.scheme == "http" and local):
        raise ErroBeza("O endereço do Painel precisa ser https (a senha não pode ir sem criptografia).", SAIDA_ERRO)
    if not partes.hostname:
        raise ErroBeza("Endereço do Painel inválido.", SAIDA_ERRO)


# ── Chamada ao Painel ────────────────────────────────────────────────────────

def chamar(url_base, token, rota, parametros=None):
    validar_url(url_base)
    consulta = {chave: valor for chave, valor in (parametros or {}).items() if valor is not None}
    endereco = f"{url_base}/api/beza/v1{rota}"
    if consulta:
        endereco += "?" + urllib.parse.urlencode(consulta)
    pedido = urllib.request.Request(
        endereco,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json", "User-Agent": "Beza-Adm/0.2 (+Grupo Gade)"},
    )
    try:
        with urllib.request.urlopen(pedido, timeout=EXPIRA_EM_SEGUNDOS) as resposta:
            return json.loads(resposta.read().decode("utf-8"))
    except urllib.error.HTTPError as erro:
        try:
            mensagem = json.loads(erro.read().decode("utf-8")).get("message")
        except (ValueError, OSError, AttributeError):
            mensagem = None
        if erro.code == 403:
            raise ErroBeza(mensagem or "Sem permissão para essa informação. Peça ao administrador do Painel para liberar.", SAIDA_SEM_PERMISSAO)
        if erro.code in (401, 429):
            raise ErroBeza(
                mensagem or "A senha do Beza foi recusada pelo Painel. Peça ao administrador do Painel uma senha nova.", SAIDA_SENHA
            )
        raise ErroBeza(mensagem or f"O Painel respondeu com erro {erro.code}.", SAIDA_ERRO)
    except (urllib.error.URLError, TimeoutError, OSError):
        raise ErroBeza("Não consegui falar com o Painel. Confira a internet e tente de novo.", SAIDA_SEM_CONEXAO)
    except ValueError:
        raise ErroBeza("O Painel devolveu uma resposta que não consegui ler.", SAIDA_ERRO)


# ── Linha de comando ─────────────────────────────────────────────────────────

def montar_parser():
    parser = argparse.ArgumentParser(description="Consulta o Painel Gade (somente leitura).")
    sub = parser.add_subparsers(dest="comando", required=True)
    for nome in ROTAS:
        item = sub.add_parser(nome)
        if nome in ("inside-caixa", "inside-lancamentos"):
            item.add_argument("--mes", help="AAAA-MM ou 'all' (padrão: mês atual)")
        if nome == "inside-lancamentos":
            item.add_argument("--pagina", help="página (50 por página)")
    return parser


def executar(argumentos):
    url, token = ler_configuracao()
    parametros = {"mes": getattr(argumentos, "mes", None), "pagina": getattr(argumentos, "pagina", None)}
    return chamar(url, token, ROTAS[argumentos.comando], parametros)


def main(argv=None):
    argumentos = montar_parser().parse_args(argv)
    try:
        resultado = executar(argumentos)
    except ErroBeza as erro:
        print(f"ERRO: {erro}", file=sys.stderr)
        return erro.codigo
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return SAIDA_OK


if __name__ == "__main__":
    sys.exit(main())
