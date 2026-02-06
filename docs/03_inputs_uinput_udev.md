[⬅️ Anterior](02_sunshine_moonlight_xfce.md) | [🏠 Índice](index.md) | [➡️ Siguiente](04_troubleshooting.md)

# Fix controles/input (Moonlight sin control): uinput + udev + grupo input

## 1) Cargar uinput al arrancar
Archivo: `/etc/modules-load.d/uinput.conf`
Contenido:


## 2) Permisos /dev/uinput con udev
Archivo: `/etc/udev/rules.d/99-uinput.rules`
Contenido:
