#!/usr/bin/env python3
"""Ponte MCP (stdio) entre o Claude e o Painel de Resultados Gade — somente leitura.

O Claude Code inicia este programa sozinho (ver .mcp.json) e entrega a senha do Beza pela variável
BEZA_PAINEL_TOKEN, vinda da caixinha de configuração do plugin. A senha nunca passa pela conversa
nem por arquivo. Só usa a biblioteca padrão do Python.

Cada ferramenta chama uma rota de /api/beza/v1. Quem decide o que a pessoa pode buscar é o servidor
do Painel (tela "Acessos do Beza"); aqui não há como contornar.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import painel  # noqa: E402

VERSAO = "0.3.0"
VERSOES_SUPORTADAS = ("2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05")

MES = {"mes": {"type": "string", "description": "AAAA-MM ou 'all' (padrão: mês atual)"}}
FERRAMENTAS = {
    "painel_eu": ("Mostra quem é o usuário e o que o Beza pode (e não pode) buscar no Painel. Use primeiro.", "/eu", {}),
    "painel_gade_resumo": ("Números gerais de clientes Gade: contratos, clientes ativos, parceiros, meta, crescimento, contratos por líder.", "/gade/resumo", {}),
    "painel_inside_caixa": ("Caixa da Inside Sales: receita, custo, lucro, saldo, série mensal e custos por categoria.", "/inside/caixa", MES),
    "painel_inside_lancamentos": (
        "Pagamentos e títulos a receber da Inside Sales (50 por página).",
        "/inside/lancamentos",
        {**MES, "pagina": {"type": "string", "description": "número da página"}},
    ),
    "painel_inside_clientes_resumo": ("Clientes da Inside: ativos/inativos, valor de contratos e entradas por mês, por carteira.", "/inside/clientes/resumo", {}),
    "painel_inside_clientes": ("Lista de clientes da Inside (razão social, CNPJ, carteira, produto, valor, entrada).", "/inside/clientes", {}),
    "painel_inside_superliga": ("Resultado da Superliga só dos consultores da Inside, em campanhas já liberadas.", "/inside/superliga", {}),
}


def lista_de_ferramentas():
    return [
        {
            "name": nome,
            "description": descricao + " Somente leitura; o Painel decide o que está liberado.",
            "inputSchema": {"type": "object", "properties": props, "additionalProperties": False},
            "annotations": {"readOnlyHint": True, "openWorldHint": False},
        }
        for nome, (descricao, _rota, props) in FERRAMENTAS.items()
    ]


def chamar_ferramenta(nome, argumentos):
    if nome not in FERRAMENTAS:
        raise painel.ErroBeza(f"Ferramenta desconhecida: {nome}", painel.SAIDA_ERRO)
    _desc, rota, props = FERRAMENTAS[nome]
    parametros = {chave: str(valor) for chave, valor in (argumentos or {}).items() if chave in props and valor is not None}
    token = os.environ.get("BEZA_PAINEL_TOKEN", "").strip()
    if not token:
        raise painel.ErroBeza(
            "O Beza ainda não tem a senha do Painel. Rode /plugin configure beza-adm@beza-adm e cole a senha que o administrador do Painel entregou.",
            painel.SAIDA_SENHA,
        )
    url = (os.environ.get("BEZA_PAINEL_URL") or painel.URL_PADRAO).rstrip("/")
    return painel.chamar(url, token, rota, parametros)


def tratar(mensagem):
    """Devolve a resposta JSON-RPC (dict) ou None para notificações."""
    metodo = mensagem.get("method")
    ident = mensagem.get("id")
    if ident is None:  # notificação (ex.: notifications/initialized): sem resposta
        return None
    if metodo == "initialize":
        pedida = (mensagem.get("params") or {}).get("protocolVersion")
        versao = pedida if pedida in VERSOES_SUPORTADAS else VERSOES_SUPORTADAS[0]
        resultado = {
            "protocolVersion": versao,
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "beza-painel", "version": VERSAO},
        }
    elif metodo == "ping":
        resultado = {}
    elif metodo == "tools/list":
        resultado = {"tools": lista_de_ferramentas()}
    elif metodo == "tools/call":
        params = mensagem.get("params") or {}
        try:
            dados = chamar_ferramenta(params.get("name"), params.get("arguments"))
            resultado = {"content": [{"type": "text", "text": json.dumps(dados, ensure_ascii=False)}], "isError": False}
        except painel.ErroBeza as erro:
            resultado = {"content": [{"type": "text", "text": f"ERRO ({erro.codigo}): {erro}"}], "isError": True}
    else:
        return {"jsonrpc": "2.0", "id": ident, "error": {"code": -32601, "message": f"Método não suportado: {metodo}"}}
    return {"jsonrpc": "2.0", "id": ident, "result": resultado}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    for linha in sys.stdin:
        linha = linha.strip()
        if not linha:
            continue
        try:
            resposta = tratar(json.loads(linha))
        except ValueError:
            resposta = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "JSON inválido"}}
        if resposta is not None:
            sys.stdout.write(json.dumps(resposta, ensure_ascii=False) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
