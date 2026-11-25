#!/usr/bin/env bash
# Injeta o contexto da empresa e as regras no início da sessão.
# Sem dependência de Python: funciona no Git Bash do Windows e no macOS/Linux.
R="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
mkdir -p "$HOME/Documents/Beza Adm" 2>/dev/null
TXT=""
for f in contexto/empresa.md contexto/regras.md; do
  [ -f "$R/$f" ] && TXT="${TXT}$(cat "$R/$f")"$'\n\n'
done
# escapa para JSON: barra, aspas, tabs e quebras de linha; remove CR
ESC="$(printf '%s' "$TXT" | tr -d '\r' | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\t/\\t/g' | awk 'BEGIN{ORS="\\n"} {print}')"
printf '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"%s"}}\n' "$ESC"
