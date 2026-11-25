---
name: consultar-painel
description: Busca números no Painel de Resultados Gade (somente leitura) pelas ferramentas painel_*: resultados e caixa da Inside Sales, carteira de clientes da Inside, Superliga da Inside e números gerais de clientes Gade, conforme o que o acesso da pessoa permitir. Use quando pedirem dado "do sistema", "do Painel", "quantos clientes", "como foi o mês", "resultado", "caixa", "ranking" ou qualquer número que não veio de uma planilha enviada.
---

# Consultar o Painel

O Painel é a fonte oficial dos números. Você **só lê**: nunca altera nada lá.
**Quem decide o que você pode buscar é o Painel**, na tela "Acessos do Beza" (o administrador libera ou bloqueia cada informação para cada pessoa). Você não consegue nem deve tentar contornar isso.

## Ferramentas (servidor MCP `painel` deste plugin)
| Ferramenta | O que traz |
|---|---|
| `painel_eu` | Quem é a pessoa e o que este acesso pode buscar e o que está bloqueado. **Chame primeiro** na conversa. |
| `painel_gade_resumo` | Números gerais de clientes Gade: contratos, clientes ativos, parceiros, meta do mês, crescimento, contratos por líder. |
| `painel_inside_caixa` (`mes`: AAAA-MM ou `all`) | Caixa da Inside: receita, custo, lucro, saldo, série mensal e custos por categoria. |
| `painel_inside_lancamentos` (`mes`, `pagina`) | Pagamentos e títulos a receber da Inside (50 por página). |
| `painel_inside_clientes_resumo` | Clientes da Inside: ativos/inativos, valor e entradas por mês, por carteira. |
| `painel_inside_clientes` | Lista dos clientes da Inside (razão social, CNPJ, carteira, produto, valor, entrada). |
| `painel_inside_superliga` | Resultado da Superliga só dos consultores da Inside, em campanhas já liberadas. |

A resposta é JSON. Use só as ferramentas que `painel_eu` mostrar como liberadas.

## Se uma ferramenta devolver erro (leia a mensagem)
- **"Sem permissão" (403):** diga com clareza que essa informação não está liberada para o acesso da pessoa e que o **administrador do Painel libera em "Acessos do Beza"**. Não tente outra ferramenta para chegar ao mesmo dado, não peça que a pessoa cole a senha, não use a internet para burlar. Ofereça trabalhar com uma planilha ou relatório que ela exporte.
- **Senha ausente ou inválida (401):** a senha precisa ser refeita: o administrador gera uma nova na tela "Acessos do Beza" e a pessoa roda `/plugin configure beza-adm@beza-adm` para colá-la. Nunca peça a senha na conversa.
- **Sem conexão:** peça para conferir a internet e tente de novo uma vez.
- **Erro do Painel (500 etc.):** diga o que a mensagem informa e que o administrador precisa olhar. Não invente número.

## Regras
- **Escopo:** só o que o acesso da pessoa permitir. Não há outras fontes.
- **Sem conferência, sem entrega:** diga de onde veio cada número (ferramenta, mês, data de atualização `atualizadoEm` quando existir) e **não arredonde valores em reais**: use o valor completo, com centavos.
- Se `pronto` vier `false` ou o mês não estiver coberto (`coberto: false`), avise que o Painel ainda não tem aquele dado, em vez de usar zero.
- **Dado pessoal e de cliente** (CNPJ, razão social): use no trabalho da pessoa, mas não repita além do necessário e não coloque em material que vá a terceiros.
- **Nunca** peça, leia ou mostre a senha do Beza. Você não precisa dela: a ponte já cuida da autenticação.
- Uma consulta por necessidade: não varra o Painel "para ver o que tem".
