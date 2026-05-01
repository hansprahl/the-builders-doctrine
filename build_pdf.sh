#!/bin/bash
# Builds two PDFs from the source markdowns:
#   1. The Builders Doctrine v1.2-draft (Hans-specific, biographical)
#   2. The Builders' Method v1.0 (agnostic, distributable)
#
# Pipeline: mermaid-cli (system Chrome) → pandoc → headless Chrome PDF.

set -euo pipefail

cd "$(dirname "$0")"
DIST=dist
mkdir -p "$DIST"

# --- Shared assets -----------------------------------------------------------

# Puppeteer config — use system Chrome to avoid Apple Silicon Chromium issues.
cat > "$DIST/puppeteer.json" <<'PUPPETEER_EOF'
{
  "executablePath": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  "args": ["--no-sandbox"]
}
PUPPETEER_EOF

# Print CSS shared by both PDFs.
cat > "$DIST/print.css" <<'CSS_EOF'
@page {
  size: letter;
  margin: 0.85in 0.75in 0.85in 0.75in;
}
html { font-size: 11pt; }
body {
  font-family: -apple-system, "Helvetica Neue", "Arial", sans-serif;
  line-height: 1.45;
  color: #1a1a1a;
  max-width: none;
}
h1, h2, h3, h4, h5 {
  font-family: -apple-system, "Helvetica Neue", "Arial", sans-serif;
  font-weight: 600;
  line-height: 1.2;
  margin-top: 1.4em;
  margin-bottom: 0.5em;
  page-break-after: avoid;
}
h1 { font-size: 1.85em; border-bottom: 2px solid #1a1a1a; padding-bottom: 0.2em; }
h2 { font-size: 1.4em; border-bottom: 1px solid #999; padding-bottom: 0.15em; margin-top: 1.6em; }
h3 { font-size: 1.15em; }
h4 { font-size: 1.0em; }
p { margin: 0.55em 0; orphans: 3; widows: 3; }
ul, ol { margin: 0.5em 0; padding-left: 1.5em; }
li { margin: 0.15em 0; }
code {
  font-family: "SF Mono", "Menlo", "Consolas", monospace;
  font-size: 0.92em;
  background: #f4f4f4;
  padding: 0.08em 0.3em;
  border-radius: 2px;
}
pre {
  font-family: "SF Mono", "Menlo", "Consolas", monospace;
  font-size: 0.85em;
  background: #f4f4f4;
  border: 1px solid #ddd;
  padding: 0.7em 0.9em;
  border-radius: 3px;
  overflow-x: auto;
  page-break-inside: avoid;
}
pre code { background: transparent; padding: 0; }
blockquote {
  border-left: 3px solid #888;
  margin: 0.7em 0;
  padding: 0.1em 0 0.1em 1em;
  color: #444;
}
table {
  border-collapse: collapse;
  margin: 0.8em 0;
  font-size: 0.95em;
  page-break-inside: avoid;
}
th, td {
  border: 1px solid #bbb;
  padding: 0.35em 0.6em;
  text-align: left;
  vertical-align: top;
}
th { background: #f0f0f0; font-weight: 600; }
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0.7em auto;
  page-break-inside: avoid;
}
a { color: #0066cc; text-decoration: none; }
hr { border: none; border-top: 1px solid #999; margin: 1.4em 0; }
strong { font-weight: 600; }
CSS_EOF

# Helper — render a single markdown's mermaid blocks to SVG and emit a
# variant in dist/ with image references.
render_mermaid() {
  local src="$1"
  local out="$2"
  npx -y -p @mermaid-js/mermaid-cli@10.9.1 mmdc \
    -i "$src" \
    -o "$out" \
    -e svg \
    --backgroundColor white \
    --puppeteerConfigFile "$DIST/puppeteer.json"
}

# Helper — turn a combined markdown into a PDF with shared CSS.
build_pdf() {
  local combined_md="$1"
  local title="$2"
  local out_pdf="$3"
  local html="${combined_md%.md}.html"

  pandoc "$combined_md" \
    --standalone \
    --metadata title="$title" \
    --css print.css \
    --resource-path="$DIST" \
    -o "$html"

  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --no-pdf-header-footer \
    --print-to-pdf="$out_pdf" \
    --print-to-pdf-no-header \
    "file://$(pwd)/$html" 2>&1 | tail -3

  echo "  → $out_pdf ($(ls -lh "$out_pdf" | awk '{print $5}'))"
}

# --- Render mermaid in source markdowns --------------------------------------

echo "Rendering Mermaid diagrams…"
render_mermaid WIRING_DIAGRAM.md "$DIST/WIRING_DIAGRAM.md"
render_mermaid THE_BUILDERS_METHOD.md "$DIST/THE_BUILDERS_METHOD.md"

# --- PDF 1: The Builders Doctrine v1.2-draft (biographical, Hans-specific) ---

echo ""
echo "Building PDF 1: The Builders Doctrine v1.2-draft…"

cat > "$DIST/00-doctrine-title.md" <<'EOF'
# THE BUILDERS DOCTRINE

**v1.2-draft**
**2026-05-01**
**Hans Prahl**

---

The meta-doctrine that sits above every Hans Prahl AI product. Defines the principles, the person, the architecture of trust, the doctrine layering, and the measurement surface that make a product his — not anyone else's.

This bundle contains:

1. **The Builders Doctrine** — the canonical principles document (Section II is the founding eleven)
2. **Wiring Diagram and Walkthrough** — visual explanation of how biography compiles into product behavior, including a runtime trace of a real request end-to-end
3. **Explainer** — plain-language translation for non-technical readers
4. **Stress Test v1.0** — conformance audit across all three live products (TOP, Operator, Custer)
5. **Candidates v1.2** — what is in flight for the next doctrine version, including the synthetic portability test findings
6. **Anatomy Doctrine v2 — Implementation Plan** — the next six-session sprint to extend the body-system measurement framework

The v1.1 tag remains the canonical released version. v1.2-draft is in flight pending external test of the portability principle.

For the agnostic version of this method (for any builder, not biographical), see *The Builders' Method v1.0* — separate document.

<div style="page-break-after: always;"></div>
EOF

{
  cat "$DIST/00-doctrine-title.md"
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat THE_BUILDERS_DOCTRINE.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat "$DIST/WIRING_DIAGRAM.md"
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat EXPLAINER.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat STRESS_TEST_v1.0.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat CANDIDATES_v1.2.md
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat ANATOMY_V2_PLAN.md
} > "$DIST/doctrine-combined.md"

build_pdf "$DIST/doctrine-combined.md" \
  "The Builders Doctrine — v1.2-draft" \
  "$DIST/the-builders-doctrine-v1.2-draft.pdf"

# --- PDF 2: The Builders' Method v1.0 (agnostic, distributable) --------------

echo ""
echo "Building PDF 2: The Builders' Method v1.0…"

cat > "$DIST/00-method-title.md" <<'EOF'
# THE BUILDERS' METHOD

**Method v1.0**
**2026-05-01**
**by Hans Prahl**

---

A reproducible framework for AI builders whose lived experience should compile into product behavior, not be lost to it.

The method is portable. The biography is yours to bring.

This document is method v1.0 of The Builders' Method, an instance of the broader brand AI Tradecraft. The method is offered as a framework for adoption. Cite the source when you apply or extend it. The method is meant to spread. The biographies that compile through it are not.

<div style="page-break-after: always;"></div>
EOF

{
  cat "$DIST/00-method-title.md"
  echo ""
  echo '<div style="page-break-before: always;"></div>'
  echo ""
  cat "$DIST/THE_BUILDERS_METHOD.md"
} > "$DIST/method-combined.md"

build_pdf "$DIST/method-combined.md" \
  "The Builders' Method — v1.0" \
  "$DIST/the-builders-method-v1.0.pdf"

# --- Done --------------------------------------------------------------------

echo ""
echo "Done."
ls -lh "$DIST"/*.pdf
