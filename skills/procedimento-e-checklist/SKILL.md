---
name: procedimento-e-checklist
description: Cria procedimento operacional (POP), checklist ou comunicado interno em documento pronto (DOCX/PDF). Use quando pedirem procedimento, passo a passo, rotina, checklist, instrução de trabalho, fluxo de processo ou comunicado para a equipe.
---

# Procedimento, checklist e comunicado

Scripts: `${CLAUDE_PLUGIN_ROOT}/scripts/html2pdf.py` (HTML para PDF). Para DOCX, use a skill de Word se estiver disponível.

## Passo a passo
1. **Entenda o processo real antes de escrever.** Pergunte só o essencial: quem executa, quando acontece, o que entra e o que sai, e onde costuma dar errado. Se o usuário já descreveu, não repita a pergunta.
2. **Redija em passos curtos e numerados**, cada um com um verbo de ação e **um responsável**. Nada de parágrafo corrido onde cabe uma lista.
3. **Estrutura do POP**: objetivo · quem executa · quando · o que precisa ter à mão (sistemas, arquivos, acessos) · passos numerados · **conferência final** (como saber que deu certo) · o que fazer se der errado · quem acionar · histórico de versões (data e o que mudou).
4. **Checklist**: itens verificáveis (sim/não), na ordem em que acontecem, com campo para data e responsável. Cada item deve poder ser conferido por outra pessoa.
5. **Comunicado**: assunto claro, o que muda, desde quando, quem é afetado, o que a pessoa precisa fazer e a quem perguntar. Tom cordial e direto.
6. **Gere o documento** com a identidade da empresa (`${CLAUDE_PLUGIN_ROOT}/contexto/identidade-visual.md`; fonte Calibri ou Arial), salve em `Documentos/Beza Adm/` e converta para PDF quando pedirem.
7. **Não invente regra, prazo ou responsável.** O que não foi dito vai para uma lista "Pontos a confirmar" no fim do documento.

## Cuidados
- **Não envie** o documento por e-mail ou mensagem. Se pedirem, redija o texto do envio.
- Processo com **dado pessoal, valor ou acesso a sistema**: não coloque senha, chave ou link com credencial no documento; indique onde a pessoa encontra o acesso.
- Em tema **jurídico, trabalhista ou tributário**, avise que o documento precisa de validação do setor responsável antes de valer.
