[⬅️ Anterior](03_inputs_uinput_udev.md) | [🏠 Índice](index.md) | [➡️ Siguiente](05_repo_workflow_github.md)

# Troubleshooting (errores reales)

## 1) Me sale `>` y no puedo escribir comandos
Eso no es Git: es el **shell esperando que cierres algo** (comillas o heredoc).

Salir:
- `Ctrl + C`
- opcional: `reset`

## 2) Me sale `^[[200~`
Eso es “bracketed paste” pegando raro.
Solución rápida:
- `reset`
- vuelve a copiar solo el comando (no texto extra)

## 3) Homepage “Unable to connect”
Comprobar contenedores:
```bash
