#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TS="$(date +%F-%H%M%S)"
OUT="$ROOT/inventory/$TS"
mkdir -p "$OUT"

copy_if_exists() {
  local src="$1" dst="$2"
  if [ -e "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    sudo rsync -a "$src" "$dst"
    echo "[+] $src -> $dst"
  else
    echo "[-] no existe: $src"
  fi
}

# Inventario básico
{
  echo "# date: $(date -Is)"
  echo "# host: $(hostname)"
  uname -a || true
  echo
  cat /etc/os-release 2>/dev/null || true
} > "$OUT/system.txt"

(lsblk -f || true) > "$OUT/lsblk.txt"
(ip a || true) > "$OUT/ip_a.txt"
(systemctl list-unit-files --state=enabled || true) > "$OUT/enabled_services.txt"

# Copias de config útiles (si existen)
copy_if_exists "/srv/docker" "$ROOT/configs/docker/srv_docker"
copy_if_exists "/etc/modules-load.d/uinput.conf" "$ROOT/configs/modules/uinput.conf"
copy_if_exists "/etc/udev/rules.d" "$ROOT/configs/udev/rules.d"
copy_if_exists "/etc/lightdm" "$ROOT/configs/lightdm/lightdm"
copy_if_exists "/etc/ssh/sshd_config" "$ROOT/configs/ssh/sshd_config"
copy_if_exists "/etc/ssh/sshd_config.d" "$ROOT/configs/ssh/sshd_config.d"
copy_if_exists "/home/$USER/.config/sunshine" "$ROOT/configs/sunshine/user_config_sunshine"
copy_if_exists "/home/$USER/.config/xfce4" "$ROOT/configs/xfce/xfce4"
copy_if_exists "/home/$USER/.config/syncthing" "$ROOT/configs/syncthing/user_config_syncthing"

echo "[*] inventario guardado en $OUT"
