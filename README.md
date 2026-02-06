# debian-stream-nas-server 

Este repo documenta **tu servidor Debian** tal y como lo tienes montado (sin NAS por ahora):

- **Dashboard web**: Homepage + Glances (Docker)
- **Streaming escritorio**: XFCE + Sunshine + Moonlight
- **Fix de controles/input**: uinput + udev + grupo `input`
- **Troubleshooting real**: errores típicos y cómo salir de ellos (incluye el `>` y `GnuTLS handshake failed`)

## Qué está “estable” ahora mismo
- Glances ✅
- Homepage ✅
- Enlaces a Portainer / Sunshine / Nextcloud ✅
- Widget Docker ❌ (si vuelve a dar “Missingdocker”, se deja fuera)

## Guías (léelas en este orden)
1) `docs/01_dashboard_homepage_glances.md`
2) `docs/02_sunshine_moonlight_xfce.md`
3) `docs/03_inputs_uinput_udev.md`
4) `docs/04_troubleshooting.md`
5) `docs/05_repo_workflow_github.md`

## Comprobación rápida (dashboard)
```bash
cd /srv/docker/dashboard/stack
docker compose up -d
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | egrep "homepage|glances|NAMES"
docker exec -it homepage sh -lc "wget -qO- --timeout=2 http://glances:61208/api/4/status | head -c 120; echo"

## Documentación
- [Guía paso a paso](docs/index.md)

