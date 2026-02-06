#!/usr/bin/env bash
set -euo pipefail

mkdir -p docs

cat > README.md <<'MD'
# debian-stream-nas-server (setup replicable, explicado para novatos)

Este repo documenta un servidor Debian con:
- Dashboard web: Homepage + Glances (Docker)
- Streaming escritorio: XFCE + Sunshine + Moonlight
- Fix de input/control: uinput + udev + grupo `input`
- Troubleshooting real: errores típicos y cómo salir de ellos (incluye el `>`)

Guías (léelas en orden):
1) docs/01_dashboard_homepage_glances.md
2) docs/02_sunshine_moonlight_xfce.md
3) docs/03_inputs_uinput_udev.md
4) docs/04_troubleshooting.md
5) docs/05_repo_workflow_github.md
MD

cat > docs/01_dashboard_homepage_glances.md <<'MD'
# Dashboard (Homepage + Glances)

Comprobación rápida:
```bash
cd /srv/docker/dashboard/stack
docker compose up -d
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | egrep 'homepage|glances|NAMES'
docker exec -it homepage sh -lc 'wget -qO- --timeout=2 http://glances:61208/api/4/status | head -c 120; echo'
