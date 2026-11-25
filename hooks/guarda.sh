#!/usr/bin/env bash
# Guarda de segurança do Beza Adm: bloqueia comandos de infraestrutura/destrutivos e arquivos de segredo.
# É um guard rail de processo; a trava real é este usuário não ter acesso a servidores.
ENTRADA="$(cat)"
bloquear() {
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Bloqueado pelo Beza: %s. Se for realmente necessário, peça ao administrador do Painel."}}\n' "$1"
  exit 0
}
if printf '%s' "$ENTRADA" | grep -Eqi '"tool_name" *: *"Bash"'; then
  printf '%s' "$ENTRADA" | grep -Eq '(^|[^a-zA-Z])(ssh|scp|sftp|sudo|su|docker|kubectl|psql|mysql|nc|ncat)[ \\"]' && bloquear "acesso a servidores/infraestrutura não faz parte do uso comercial"
  printf '%s' "$ENTRADA" | grep -Eq 'git +(push|remote|reset +--hard|clean)' && bloquear "operações de git remoto/destrutivas"
  printf '%s' "$ENTRADA" | grep -Eq 'rm +(-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)|rm +-r|mkfs|dd +if=|chmod +-R|chown +-R|shutdown|reboot' && bloquear "comando destrutivo"
  printf '%s' "$ENTRADA" | grep -Eq '(curl|wget)[^|]*\|[ ]*(ba|z)?sh' && bloquear "executar script baixado da internet"
fi
# segredos: .env, chaves, credenciais
printf '%s' "$ENTRADA" | grep -Eqi '(\.env([^a-z]|$)|id_rsa|id_ed25519|\.pem|credentials|\.npmrc|\.ssh/|\.beza[/\\\\]|BEZA_PAINEL_TOKEN)' && bloquear "arquivo que pode conter senha ou chave"
exit 0
