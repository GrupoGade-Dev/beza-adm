#!/usr/bin/env bash
# Inicia a ponte MCP do Painel com o Python que existir na máquina (python3, python ou py -3).
DIR="$(cd "$(dirname "$0")" && pwd)"
ok() { "$@" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; }
for py in python3 python; do
  if command -v "$py" >/dev/null 2>&1 && ok "$py"; then exec "$py" "$DIR/painel_mcp.py"; fi
done
if command -v py >/dev/null 2>&1 && ok py -3; then exec py -3 "$DIR/painel_mcp.py"; fi
echo "Python 3.8 ou mais novo não encontrado. Peça ajuda a quem administra o Beza." >&2
exit 1
