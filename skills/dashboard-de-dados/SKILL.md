---
name: dashboard-de-dados
description: Cria dashboard (página HTML com gráficos e indicadores) a partir de planilhas xlsx/csv. Use quando pedirem dashboard, painel, gráfico, análise de vendas/carteira/metas ou "transformar essa planilha em algo visual".
---

# Dashboard a partir de planilha

Carregue também a skill `dataviz` se estiver disponível, para as boas práticas de gráfico.

## Passo a passo
1. **Leia a planilha** com Python (`pandas` ou `openpyxl`; peça autorização para instalar se faltar). Mostre ao usuário, em 3–4 linhas: abas, colunas, período e quantidade de linhas — e **como entendeu cada coluna**. Corrija com ele se algo estiver trocado.
2. **Defina as perguntas** que o dashboard responde (ex.: "como vão as vendas por regional?", "quem está abaixo da meta?"). Se o usuário não disse, proponha 3–5 e siga.
3. **Cheque a qualidade dos dados** antes de plotar: duplicados, vazios, datas inválidas, valores negativos, totais que não fecham. Relate o que encontrou e o que fez.
4. **Gere um único arquivo HTML autônomo** em `~/Documents/Beza Adm/` (dados embutidos, abre com duplo clique, **sem servidor e sem enviar dados para fora**). Gráficos com Chart.js de CDN versionado (`https://cdn.jsdelivr.net/npm/chart.js@4.4.1`) ou SVG simples.
5. **Layout**: título + período + **fonte dos dados** (nome do arquivo e data) no topo · linha de indicadores (KPIs) · 3–6 gráficos com título que diz a conclusão · tabela de detalhe no fim. Funciona no celular.
6. **Identidade**: siga `${CLAUDE_PLUGIN_ROOT}/contexto/identidade-visual.md` (Gade, Issacar ou Benjamin). Nunca use vermelho/verde como única forma de distinguir (daltonismo).
7. Se pedirem **PDF**, converta com `html2pdf.py`.
8. **Confira os números**: recalcule totais do dashboard contra a planilha e diga que conferiu.

## Cuidados
- Planilha com CPF, telefone ou e-mail de cliente: **não exiba dado pessoal**; agregue ou mascare, e avise.
- Não invente metas, comparativos ou projeções que não estejam nos dados; rotule estimativas como estimativas.
- Dashboard é uma foto dos dados na data do arquivo: escreva isso no rodapé. Para atualizar, o usuário envia a planilha nova e você gera de novo.
