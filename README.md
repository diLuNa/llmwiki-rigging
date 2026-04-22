# Rigging Wiki

Personal research knowledge base for character rigging papers.

## Quick Start

Open this folder as an Obsidian vault. Point your LLM agent at `CLAUDE.md`.

## Structure

- `CLAUDE.md` — agent schema and instructions (start here)
- `wiki/` — all wiki pages (agent writes, you read)
  - `index.md` — master catalog
  - `log.md` — activity log
  - `overview.md` — field synthesis
  - `papers/` — one page per paper
  - `concepts/` — algorithm and concept pages
  - `techniques/` — Houdini/VEX implementation pages
  - `authors/` — key researchers
  - `comparisons/` — side-by-side analyses
  - `queries/` — saved answers  
  - `explorations/` — saved exploration and research requests and answers
- `raw/` — your source documents (immutable)
- `tools/` — helper scripts

## Common Commands

```bash
# Search the wiki
./tools/search.sh "dual quaternion"

# Show recent activity
./tools/recent.sh 5
```

## Obsidian Setup

1. Open folder as vault
2. Enable: Graph view, Dataview plugin (optional), Marp plugin (optional)
3. Settings → Files → Attachment folder: `raw/assets/`
4. Install Obsidian Web Clipper for capturing papers/articles
