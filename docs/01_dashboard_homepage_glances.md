# Dashboard (Homepage + Glances)

Comprobación rápida:
```bash
cd /srv/docker/dashboard/stack
docker compose up -d
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | egrep 'homepage|glances|NAMES'
docker exec -it homepage sh -lc 'wget -qO- --timeout=2 http://glances:61208/api/4/status | head -c 120; echo'
