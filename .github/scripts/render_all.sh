#!/usr/bin/env bash
set -euo pipefail

# este script está em: <repo>/.github/scripts/render_all.sh
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

WF_DIR="$ROOT/.github/workflows"
OUT_DIR="$ROOT/assets/svg/workflows"
TMP_DIR="$ROOT/.tmp/workflows"

mkdir -p "$OUT_DIR" "$TMP_DIR"

# deps: node + @mermaid-js/mermaid-cli + python3 + pyyaml
# instala mermaid-cli local (sem sujar global)
if [ ! -d "$ROOT/node_modules/@mermaid-js/mermaid-cli" ]; then
  (cd "$ROOT" && npm init -y >/dev/null 2>&1 || true)
  (cd "$ROOT" && npm i -D @mermaid-js/mermaid-cli >/dev/null)
fi

# garante pyyaml
python3 - <<'PY' >/dev/null 2>&1 || (echo "Instale PyYAML: pip3 install pyyaml" && exit 1)
import yaml
PY

python3 "$ROOT/.github/scripts/workflow_to_mermaid.py" "$WF_DIR" "$TMP_DIR"

for mmd in "$TMP_DIR"/*.mmd; do
  [ -f "$mmd" ] || continue
  base="$(basename "$mmd" .mmd)"
  "$ROOT/node_modules/.bin/mmdc" -i "$mmd" -o "$OUT_DIR/${base}.svg" -b transparent --puppeteerConfigFile "$ROOT/.github/scripts/puppeteer-no-sandbox.json"
  echo "OK: $OUT_DIR/${base}.svg"
done

# --- scripts (.py) -> mermaid -> svg ---
# --- scripts (.py) -> mermaid -> svg (na raiz assets/svg) ---
PY_DIR="$ROOT/.github/scripts"
PY_TMP="$ROOT/.tmp/scripts"
PY_OUT="$ROOT/assets/svg"

mkdir -p "$PY_TMP" "$PY_OUT"

python3 "$ROOT/.github/scripts/py_to_mermaid.py" "$PY_DIR" "$PY_TMP"

for mmd in "$PY_TMP"/*.mmd; do
  [ -f "$mmd" ] || continue
  base="$(basename "$mmd" .mmd)"
  "$ROOT/node_modules/.bin/mmdc" -i "$mmd" -o "$PY_OUT/script-${base}.svg" -b transparent \
    --puppeteerConfigFile "$ROOT/.github/scripts/puppeteer-no-sandbox.json"
  echo "OK: $PY_OUT/script-${base}.svg"
done

# --- publicar fontes Mermaid para edição ---
mkdir -p "$ROOT/assets/mmd"

# workflows -> assets/mmd/workflow-*.mmd
for f in "$TMP_DIR"/*.mmd; do
  [ -f "$f" ] || continue
  base="$(basename "$f")"
  cp "$f" "$ROOT/assets/mmd/workflow-$base"
done

# scripts -> assets/mmd/script-*.mmd
for f in "$PY_TMP"/*.mmd; do
  [ -f "$f" ] || continue
  base="$(basename "$f")"
  cp "$f" "$ROOT/assets/mmd/script-$base"
done