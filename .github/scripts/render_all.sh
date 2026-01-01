#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

WF_DIR="$ROOT/.github/workflows"
PY_DIR="$ROOT/.github/scripts"

OUT_SVG="$ROOT/assets/svg"
OUT_MMD="$ROOT/assets/mmd"

TMP_WF="$ROOT/.tmp/workflows"
TMP_PY="$ROOT/.tmp/scripts"

mkdir -p "$OUT_SVG" "$OUT_MMD" "$TMP_WF" "$TMP_PY"

# deps: node + @mermaid-js/mermaid-cli + python3 + pyyaml
if [ ! -d "$ROOT/node_modules/@mermaid-js/mermaid-cli" ]; then
  (cd "$ROOT" && npm init -y >/dev/null 2>&1 || true)
  (cd "$ROOT" && npm i -D @mermaid-js/mermaid-cli >/dev/null)
fi

python3 - <<'PY' >/dev/null 2>&1 || (echo "Instale PyYAML: pip3 install pyyaml" && exit 1)
import yaml
PY

MMDC="$ROOT/node_modules/.bin/mmdc"
PUPPET="$ROOT/.github/scripts/puppeteer-no-sandbox.json"

# -------------------------------
# WORKFLOWS (.yml) -> .mmd -> svg
# -------------------------------
python3 "$ROOT/.github/scripts/workflow_to_mermaid.py" "$WF_DIR" "$TMP_WF"

for mmd in "$TMP_WF"/*.mmd; do
  [ -f "$mmd" ] || continue
  base="$(basename "$mmd" .mmd)"

  # saída padronizada
  cp "$mmd" "$OUT_MMD/${base}.mmd"

  "$MMDC" -i "$mmd" -o "$OUT_SVG/${base}.svg" -b transparent \
    --puppeteerConfigFile "$PUPPET"

  echo "OK: $OUT_SVG/${base}.svg"
done

# -------------------------------
# SCRIPTS (.py) -> .mmd -> svg
# -------------------------------
python3 "$ROOT/.github/scripts/py_to_mermaid.py" "$PY_DIR" "$TMP_PY"

for mmd in "$TMP_PY"/*.mmd; do
  [ -f "$mmd" ] || continue
  base="$(basename "$mmd" .mmd)"

  # colisão: se já existir (ex.: workflow com mesmo base), preserva o existente e cria sufixo
  if [ -f "$OUT_MMD/${base}.mmd" ] || [ -f "$OUT_SVG/${base}.svg" ]; then
    base="script_${base}"
  fi

  cp "$mmd" "$OUT_MMD/${base}.mmd"

  "$MMDC" -i "$mmd" -o "$OUT_SVG/${base}.svg" -b transparent \
    --puppeteerConfigFile "$PUPPET"

  echo "OK: $OUT_SVG/${base}.svg"
done
