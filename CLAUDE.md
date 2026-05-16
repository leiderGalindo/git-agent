# Git Agent — Guía para Mantenedores

## Arquitectura

Este proyecto es un subagente de Claude Code para automatización de Git en lenguaje natural.
Usa una arquitectura de carga bajo demanda: el agente principal es ligero (~10 KB) y
lee cada flujo de trabajo solo cuando lo necesita usando la herramienta `Read`.

```
EN EL REPO (fuentes de verdad)         EN EL PROYECTO USUARIO (instalado)
──────────────────────────────         ────────────────────────────────────
agent.md              ──────────────→  .claude/agents/git-agent.md   (~10 KB)
                                                     ↓ lee con Read al usarse
flows/01-commit-push.md  ───────────→  .claude/git-agent/flows/01-commit-push.md
flows/02-pull-request.md ───────────→  .claude/git-agent/flows/02-pull-request.md
flows/03-branch-create.md ──────────→  .claude/git-agent/flows/03-branch-create.md
flows/04-branch-switch.md ──────────→  .claude/git-agent/flows/04-branch-switch.md
flows/05-pull-update.md  ───────────→  .claude/git-agent/flows/05-pull-update.md
flows/06-edge-cases.md   ───────────→  .claude/git-agent/flows/06-edge-cases.md
                                                     ↓ lee con Read al usarse
templates/commit-rules.md ──────────→  .claude/git-agent/templates/commit-rules.md
templates/pr-template.md  ──────────→  .claude/git-agent/templates/pr-template.md
```

**Ventaja:** solo el agente principal (~10 KB) se carga en el system prompt.
Los flujos se leen bajo demanda, reduciendo el uso del contexto un 77%.

## Archivos del proyecto

| Archivo | Propósito | ¿Editar? |
|---|---|---|
| `agent.md` | Comportamiento, reglas y tabla de intenciones | ✅ Sí |
| `flows/*.md` | Implementación de cada flujo de trabajo | ✅ Sí |
| `templates/*.md` | Plantillas de commits y PRs | ✅ Sí |
| `.claude/agents/git-agent.md` | Agente ligero (generado por build.py) | ❌ No |
| `install-git-agent.md` | Skill de instalación por proyecto | ✅ Sí (si cambia URL o estructura) |
| `scripts/build.py` | Genera el agente ligero | ✅ Sí (si cambia la estructura) |
| `tests/run_tests.py` | Suite de pruebas automatizadas | ✅ Sí (para nuevos tests) |

## Flujo de trabajo para modificaciones

1. Edita el archivo fuente (`agent.md`, `flows/XX-flujo.md` o `templates/*.md`)
2. Si editaste `agent.md`, regenera el agente ligero:
   ```bash
   python scripts/build.py
   ```
   Si solo editaste flujos o plantillas, no necesitas regenerar el agente.
3. Corre los tests:
   ```bash
   export ANTHROPIC_API_KEY=sk-...
   python tests/run_tests.py
   ```
4. Commit incluyendo los archivos modificados:
   ```bash
   # Si cambió agent.md:
   git add agent.md .claude/agents/git-agent.md
   # Si cambió un flujo:
   git add flows/XX-flujo.md
   git commit -m "feat(agent): descripción del cambio"
   ```

## Agregar un nuevo flujo

1. Crea `flows/07-nuevo-flujo.md` con esta estructura:
   - Sección "Cuándo se activa" con frases de ejemplo
   - Pasos numerados con bloques bash
   - Diagrama de decisión al final

2. Registra el flujo en la tabla de intenciones en `agent.md` (sección "Tabla de intenciones")

3. Agrega la ruta en `scripts/build.py` → lista `SOURCES["flows"]`

4. Agrega la ruta en `tests/run_tests.py` → lista `FLOW_FILES`

5. Agrega la ruta en `install-git-agent.md` → sección PASO 3

6. Escribe test cases en `tests/run_tests.py`

7. Regenera y valida:
   ```bash
   python scripts/build.py
   python tests/run_tests.py
   ```

## Ejecutar los tests

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-...

python tests/run_tests.py              # todos los tests
python tests/run_tests.py --test 01-A  # un test específico
python tests/run_tests.py --verbose    # con respuestas completas
```

## Distribución y URLs

Los archivos se distribuyen desde:
```
https://raw.githubusercontent.com/leiderGalindo/git-agent/main/
```

Si el repo cambia de ubicación, actualizar esta URL en:
- `install-git-agent.md` (PASO 3, variable `BASE`)
- `README.md` (sección Instalación)
