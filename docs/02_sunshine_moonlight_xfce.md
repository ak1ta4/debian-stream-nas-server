[⬅️ Anterior](01_dashboard_homepage_glances.md) | [🏠 Índice](index.md) | [➡️ Siguiente](03_inputs_uinput_udev.md)

# Sunshine + Moonlight + XFCE (streaming)

## Objetivo
- Servidor Debian con XFCE para tener escritorio
- Sunshine emite el escritorio
- Moonlight conecta desde el cliente

## Notas importantes
- Si Moonlight no controla (teclado/mando), el fix está en `docs/03_inputs_uinput_udev.md`
- Si `systemctl status sunshine` dice “Unit not found”, es que Sunshine no está como servicio systemd en tu caso (puede estar lanzado por autostart/otro método). Se documenta cuando lo dejes definitivo.
