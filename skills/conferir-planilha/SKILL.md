---
name: conferir-planilha
description: Confere uma planilha (xlsx/csv) e entrega uma cópia conferida, sem mexer no original. Use quando pedirem para validar, conferir, checar, limpar, cruzar ou comparar planilhas, listas de CNPJ/clientes, fechamentos ou relatórios.
---

# Conferir planilha

Regra da casa: **sem conferência, sem entrega**. O original **nunca** é alterado.

## Passo a passo
1. **Leia a planilha** com Python (`openpyxl` ou `pandas`; peça autorização antes de instalar o que faltar). Mostre em 3 ou 4 linhas: abas, colunas, quantidade de linhas e o período, e **como entendeu cada coluna**. Corrija com o usuário se algo estiver trocado.
2. **Pergunte só o que falta** para definir a conferência: o que deve estar certo? (ex.: CNPJ válido, sem duplicados, soma que fecha com outro total, coluna obrigatória preenchida).
3. **Rode as conferências**, no que for relevante:
   - linhas duplicadas (inteiras e por chave, como CNPJ ou número do contrato);
   - células vazias em colunas obrigatórias;
   - **CNPJ/CPF**: 14/11 dígitos e dígitos verificadores; zeros à esquerda preservados (texto, não número);
   - datas inválidas ou fora do período; valores negativos ou zerados;
   - totais e subtotais que não fecham com a soma das linhas;
   - texto com espaços sobrando e variações do mesmo nome.
4. **Entregue uma cópia** com sufixo ` - conferido` (nunca sobrescreva o original), com:
   - a aba original **intacta**;
   - uma aba **"Conferência"** com o resumo (o que foi checado, quantas linhas, quantos achados por tipo);
   - uma aba **"Achados"** com as linhas com problema (linha de origem, campo, problema), para o usuário corrigir.
5. **Confira o que você mesmo entregou**: compare a aba original da cópia com o original (mesmas linhas, mesmos valores, hiperlinks e formatação preservados) e diga o resultado.
6. Diga o caminho completo da cópia em `Documentos/Beza Adm/` (ou na pasta que o usuário indicar).

## Cuidados
- **Hiperlinks e formatação**: ao inserir colunas com `openpyxl`, links, larguras de coluna e filtro **não acompanham**; reaplique e confira. Se não conseguir preservar, avise antes de entregar.
- **Dado pessoal** (CPF, telefone, e-mail): não repita em mensagens do chat além do necessário para explicar o achado.
- **Não corrija por conta própria** valores do usuário: aponte o achado e proponha a correção; só aplique na cópia quando ele aprovar.
- **Cruzamento com o ERP ou com o banco**: não faz parte do seu acesso. Se o pedido exigir isso (ex.: "esse CNPJ tem contrato ativo?"), explique que o cruzamento é feito pela equipe responsável e que você pode deixar a lista pronta e conferida para ele.
