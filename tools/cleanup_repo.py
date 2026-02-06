#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
README = ROOT / "README.md"

NAV_RE = re.compile(r"^\[⬅️.*?\]\(.*?\)\s*\|\s*\[🏠.*?\]\(.*?\)\s*\|\s*\[➡️.*?\]\(.*?\)\s*$", re.M)
H1_RE = re.compile(r"^#\s+(.+)\s*$", re.M)

def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^\w\s\-áéíóúüñ]", "", s, flags=re.U)
    s = re.sub(r"\s+", "-", s)
    return s[:64].strip("-") or "seccion"

def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write_text(p: Path, content: str) -> None:
    p.write_text(content, encoding="utf-8", newline="\n")

def ensure_docs_index(md_files: list[Path]) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    index = DOCS / "index.md"

    lines = []
    lines.append("# Índice\n")
    lines.append("Guía paso a paso para montar el servidor (NAS + streaming + sync/backup).\n")
    lines.append("## Orden recomendado\n")
    for f in md_files:
        if f.name == "index.md":
            continue
        title = extract_title(f) or f.stem
        lines.append(f"- [{title}]({f.name})")
    lines.append("\n## Troubleshooting\n")
    # intenta enlazar un troubleshooting si existe
    t = [f for f in md_files if "trouble" in f.name.lower() or "problema" in f.name.lower()]
    if t:
        title = extract_title(t[0]) or t[0].stem
        lines.append(f"- [{title}]({t[0].name})")
    else:
        lines.append("- (Añade aquí tu doc de troubleshooting si no existe)")
    lines.append("")
    write_text(index, "\n".join(lines))

def extract_title(p: Path) -> str | None:
    txt = read_text(p)
    m = H1_RE.search(txt)
    return m.group(1).strip() if m else None

def strip_existing_nav(txt: str) -> str:
    # quita nav existente si está (para no duplicar)
    txt2 = NAV_RE.sub("", txt).lstrip("\n")
    return txt2

def add_nav(md_files: list[Path]) -> None:
    # Ordena por nombre: 00_xxx.md, 01_xxx.md...
    ordered = [f for f in md_files if f.name != "index.md"]
    ordered.sort(key=lambda p: p.name.lower())

    for i, f in enumerate(ordered):
        prev_file = ordered[i - 1].name if i > 0 else None
        next_file = ordered[i + 1].name if i < len(ordered) - 1 else None

        prev_label = "Inicio" if prev_file is None else "Anterior"
        next_label = "Siguiente" if next_file is not None else "Fin"

        left = f"[⬅️ {prev_label}]({prev_file})" if prev_file else "[⬅️ Inicio](index.md)"
        mid = "[🏠 Índice](index.md)"
        right = f"[➡️ {next_label}]({next_file})" if next_file else "[➡️ Fin](index.md)"
        nav = f"{left} | {mid} | {right}\n\n"

        txt = read_text(f)
        txt = strip_existing_nav(txt)
        write_text(f, nav + txt.rstrip() + "\n")

def normalize_codeblocks(md_files: list[Path]) -> None:
    # Pone ```bash para bloques que parecen comandos y no tienen lenguaje
    fence = "```"
    for f in md_files:
        if f.name == "index.md":
            continue
        txt = read_text(f)
        out = []
        lines = txt.splitlines()
        in_block = False
        block_lang = None
        block_lines = []

        def looks_like_shell(block: list[str]) -> bool:
            sample = "\n".join(block).strip()
            if not sample:
                return False
            # heurística
            return bool(re.search(r"(^|\n)\s*(sudo|apt|systemctl|nano|mkdir|chmod|chown|rsync|ufw|lsblk|mount|cp|mv|git)\b", sample))

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith(fence):
                if not in_block:
                    # abrir
                    in_block = True
                    m = re.match(r"^```(\w+)?\s*$", line.strip())
                    block_lang = m.group(1) if m else None
                    block_lines = []
                    out.append(line)  # lo ajustaremos al cerrar si hace falta
                else:
                    # cerrar
                    # decide si ponemos bash en el fence de apertura
                    if block_lang is None and looks_like_shell(block_lines):
                        # reemplaza el último fence de apertura en out
                        # buscar hacia atrás la última línea que sea ```
                        for j in range(len(out)-1, -1, -1):
                            if out[j].strip() == "```":
                                out[j] = "```bash"
                                break
                    out.extend(block_lines)
                    out.append(line)
                    in_block = False
                    block_lang = None
                    block_lines = []
                i += 1
                continue

            if in_block:
                block_lines.append(line)
            else:
                out.append(line)
            i += 1

        write_text(f, "\n".join(out).rstrip() + "\n")

def ensure_readme() -> None:
    if not README.exists():
        write_text(README, "# debian-stream-nas-server\n\nVer documentación: [docs/index.md](docs/index.md)\n")
        return

    txt = read_text(README)
    # Añade un bloque "Documentación" si no existe
    if "docs/index.md" not in txt:
        insert = "\n\n## Documentación\n- [Guía paso a paso](docs/index.md)\n"
        write_text(README, txt.rstrip() + insert + "\n")

def create_editorconfig() -> None:
    p = ROOT / ".editorconfig"
    if p.exists():
        return
    write_text(p, """root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.py]
indent_size = 4

[Makefile]
indent_style = tab
""")

def create_markdownlint() -> None:
    p = ROOT / ".markdownlint.json"
    if p.exists():
        return
    write_text(p, """{
  "default": true,
  "MD013": { "line_length": 120 },
  "MD033": false,
  "MD041": false
}
""")

def create_workflow_markdownlint() -> None:
    wf = ROOT / ".github" / "workflows" / "markdownlint.yml"
    wf.parent.mkdir(parents=True, exist_ok=True)
    if wf.exists():
        return
    write_text(wf, """name: markdownlint

on:
  push:
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run markdownlint
        uses: DavidAnson/markdownlint-cli2-action@v16
        with:
          globs: |
            **/*.md
            !node_modules/**
""")

def main() -> None:
    if not DOCS.exists():
        DOCS.mkdir(parents=True, exist_ok=True)

    md_files = sorted([p for p in DOCS.glob("*.md")], key=lambda p: p.name.lower())

    # Si no hay docs, crea un esqueleto básico
    if not md_files:
        skeleton = [
            ("00_prerequisitos.md", "# 00 Prerrequisitos\n\n## Objetivo\n\n## Pasos\n\n## Verificación\n"),
            ("01_base_debian.md", "# 01 Base Debian\n\n## Objetivo\n\n## Pasos\n\n## Verificación\n"),
            ("02_xfce_sunshine.md", "# 02 XFCE + Sunshine\n\n## Objetivo\n\n## Pasos\n\n## Verificación\n"),
            ("03_storage_mounts.md", "# 03 Storage y montajes\n\n## Objetivo\n\n## Pasos\n\n## Verificación\n"),
            ("04_syncthing_rsync.md", "# 04 Syncthing y rsync\n\n## Objetivo\n\n## Pasos\n\n## Verificación\n"),
            ("05_troubleshooting.md", "# 05 Troubleshooting\n\n## Síntomas\n\n## Causas\n\n## Soluciones\n")
        ]
        for name, content in skeleton:
            write_text(DOCS / name, content)
        md_files = sorted([p for p in DOCS.glob("*.md")], key=lambda p: p.name.lower())

    ensure_docs_index(md_files)
    md_files = sorted([p for p in DOCS.glob("*.md")], key=lambda p: p.name.lower())

    add_nav(md_files)
    normalize_codeblocks(md_files)
    ensure_readme()
    create_editorconfig()
    create_markdownlint()
    create_workflow_markdownlint()

    # Nota de ejecución
    stamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%SZ")
    print(f"[OK] Repo limpio: navegación + índice + lint + editorconfig ({stamp})")

if __name__ == "__main__":
    main()
