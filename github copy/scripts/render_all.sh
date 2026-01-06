#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

WF_DIR="$ROOT/.github/workflows"
PY_DIR="$ROOT/.github/scripts"

# Saídas finais (hierárquicas)
OUT_MMD_WF="$ROOT/assets/mmd/workflows"
OUT_MMD_PY="$ROOT/assets/mmd/scripts"

OUT_SVG_WF="$ROOT/assets/svg/workflows"
OUT_SVG_PY="$ROOT/assets/svg/scripts"

# Temporários
TMP_WF="$ROOT/.tmp/workflows"
TMP_PY="$ROOT/.tmp/scripts"

mkdir -p \
  "$OUT_MMD_WF" "$OUT_MMD_PY" \
  "$OUT_SVG_WF" "$OUT_SVG_PY" \
  "$TMP_WF" "$TMP_PY"

# deps: node + mermaid-cli + python3 + pyyaml
if [ ! -d "$ROOT/node_modules/@mermaid-js/mermaid-cli" ]; then
  (cd "$ROOT" && npm init -y >/dev/null 2>&1 || true)
  (cd "$ROOT" && npm i -D @mermaid-js/mermaid-cli >/dev/null)
fi

python3 - <<'PY' >/dev/null 2>&1 || (echo "Instale PyYAML: pip3 install pyyaml" && exit 1)
import yaml
PY

MMDC="$ROOT/node_modules/.bin/mmdc"
PUPPET="$ROOT/.github/scripts/puppeteer-no-sandbox.json"

# =================================
# WORKFLOWS (.yml) -> .mmd -> .svg
# =================================
python3 "$ROOT/.github/scripts/workflow_to_mermaid.py" "$WF_DIR" "$TMP_WF"

for mmd in "$TMP_WF"/*.mmd; do
  [ -f "$mmd" ] || continue
  base="$(basename "$mmd" .mmd)"

  cp "$mmd" "$OUT_MMD_WF/${base}.mmd"

  "$MMDC" \
    -i "$mmd" \
    -o "$OUT_SVG_WF/${base}.svg" \
    -b transparent \
    --puppeteerConfigFile "$PUPPET"

  echo "OK (workflow): $OUT_SVG_WF/${base}.svg"
done

# =================================
# SCRIPTS (.py) -> .mmd -> .svg
# =================================
python3 "$ROOT/.github/scripts/py_to_mermaid.py" "$PY_DIR" "$TMP_PY"

for mmd in "$TMP_PY"/*.mmd; do
  [ -f "$mmd" ] || continue
  base="$(basename "$mmd" .mmd)"

  cp "$mmd" "$OUT_MMD_PY/${base}.mmd"

  "$MMDC" \
    -i "$mmd" \
    -o "$OUT_SVG_PY/${base}.svg" \
    -b transparent \
    --puppeteerConfigFile "$PUPPET"

  echo "OK (script): $OUT_SVG_PY/${base}.svg"
done