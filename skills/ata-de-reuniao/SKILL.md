---
name: ata-de-reuniao
description: Gera ata de reunião (PDF e texto) a partir de transcrição ou gravação. Use quando pedirem ata, resumo de reunião, pauta/decisões/pendências ou enviarem arquivo de transcrição, áudio ou vídeo de reunião.
---

# Ata de reunião

Scripts: `${CLAUDE_PLUGIN_ROOT}/scripts/transcrever.py` (áudio → texto) e `${CLAUDE_PLUGIN_ROOT}/scripts/html2pdf.py` (HTML → PDF).

## Entradas aceitas
- **Transcrição pronta** (.txt, .docx, .vtt, .srt do Teams/Meet/Zoom ou texto colado): vá direto ao passo 2.
- **Gravação** (.mp3, .m4a, .mp4, .wav): explique que será transcrita **no próprio computador** (nada sai da máquina) e peça autorização para instalar o que faltar (`ffmpeg`, `openai-whisper`). Então rode:
  ```bash
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/transcrever.py" "<gravacao>" "<saida>.txt"
  ```
  Gravações longas demoram; avise o tempo estimado. Nomes próprios saem errados com frequência: **liste os nomes que ficaram em dúvida** para o usuário confirmar.

## Passo a passo
1. Pergunte só o que faltar: **data, participantes, assunto** (se não estiverem na transcrição).
2. Redija a ata em português, **fiel ao que foi dito** — nunca invente decisão, número ou prazo. O que estiver confuso vai para "Pontos a confirmar".
3. Estrutura: cabeçalho (título, data, participantes) · **Resumo** (3–5 linhas) · **Assuntos discutidos** (um bloco curto por tema) · **Decisões** · **Ações e responsáveis** (tabela: ação, responsável, prazo) · **Pontos a confirmar**.
4. Gere HTML com a identidade da empresa (siga `${CLAUDE_PLUGIN_ROOT}/contexto/identidade-visual.md`; fonte Calibri/Arial), salve em `~/Documents/Beza Adm/` e converta para PDF com `html2pdf.py`. Entregue também o texto da ata em .txt/.md para colar em e-mail.
5. **Não envie e-mail.** Se o usuário quiser, redija o texto do e-mail de envio da ata.

## Cuidados
- Se a reunião tiver conteúdo sensível (dados pessoais, valores internos), avise antes de a ata circular.
- Mantenha tom neutro e objetivo; sem opinião sua.
