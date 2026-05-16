---
name: install-git-agent
description: >
  Instala el agente git-agent en este proyecto. Actívalo cuando el usuario diga
  "instala git-agent", "quiero usar el agente de git aquí", "configura git-agent",
  "agrega git-agent a este proyecto", "quiero el asistente de git", "instala el
  asistente de control de versiones".
model: claude-haiku-4-5-20251001
tools: Bash, Write
color: blue
---

# Instalador de Git Agent

Instala el agente `git-agent` en el proyecto actual. El agente se compone de:
- Un archivo de definición ligero en `.claude/agents/git-agent.md` (~10 KB)
- Archivos de flujo en `.claude/git-agent/flows/` (leídos bajo demanda)
- Plantillas en `.claude/git-agent/templates/`

Después de la instalación, el agente responderá frases como "sube mis cambios",
"crea una rama", "haz un PR", "actualiza mi rama".

---

## Pasos de instalación

### PASO 1 — Verificar si ya está instalado

```bash
ls .claude/agents/git-agent.md 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```

- Si el resultado es `EXISTS`:
  → Preguntar: "git-agent ya está instalado en este proyecto. ¿Quieres actualizarlo a la versión más reciente? (sí/no)"
  - Si dice **sí** → continuar
  - Si dice **no** → informar que se mantiene la versión actual y terminar

- Si el resultado es `NOT_FOUND` → continuar

---

### PASO 2 — Crear estructura de directorios

```bash
mkdir -p .claude/agents .claude/git-agent/flows .claude/git-agent/templates
```

---

### PASO 3 — Descargar todos los archivos del agente

Ejecutar este script de descarga completo:

```bash
BASE="https://raw.githubusercontent.com/leiderGalindo/git-agent/main"

# Agente principal (ligero — solo reglas de comportamiento)
curl -sSL "$BASE/.claude/agents/git-agent.md" -o .claude/agents/git-agent.md

# Flujos de trabajo (se leen bajo demanda durante el uso)
curl -sSL "$BASE/flows/01-commit-push.md"   -o .claude/git-agent/flows/01-commit-push.md
curl -sSL "$BASE/flows/02-pull-request.md"  -o .claude/git-agent/flows/02-pull-request.md
curl -sSL "$BASE/flows/03-branch-create.md" -o .claude/git-agent/flows/03-branch-create.md
curl -sSL "$BASE/flows/04-branch-switch.md" -o .claude/git-agent/flows/04-branch-switch.md
curl -sSL "$BASE/flows/05-pull-update.md"   -o .claude/git-agent/flows/05-pull-update.md
curl -sSL "$BASE/flows/06-edge-cases.md"    -o .claude/git-agent/flows/06-edge-cases.md

# Plantillas (commit y PR)
curl -sSL "$BASE/templates/commit-rules.md" -o .claude/git-agent/templates/commit-rules.md
curl -sSL "$BASE/templates/pr-template.md"  -o .claude/git-agent/templates/pr-template.md
```

Si `curl` no está disponible, intentar cada descarga con `wget -q URL -O destino`.

Si ninguno está disponible:
→ Mostrar: "No encontré herramientas de descarga (curl ni wget). Instala uno de ellos o descarga los archivos manualmente desde: https://github.com/leiderGalindo/git-agent"

---

### PASO 4 — Verificar integridad

```bash
head -3 .claude/agents/git-agent.md
ls .claude/git-agent/flows/ | wc -l
ls .claude/git-agent/templates/ | wc -l
```

Verificar:
- El agente comienza con `---` (YAML válido)
- Hay exactamente 6 archivos en `flows/`
- Hay exactamente 2 archivos en `templates/`

Si alguna verificación falla → mostrar error específico y limpiar archivos descargados.

---

### PASO 5 — Confirmar instalación exitosa

Mostrar:

```
✅ ¡git-agent instalado correctamente en este proyecto!

Archivos instalados:
  .claude/agents/git-agent.md          ← Agente (reglas de comportamiento)
  .claude/git-agent/flows/             ← 6 flujos de trabajo
  .claude/git-agent/templates/         ← 2 plantillas

Ahora puedes decirme:
  • "sube mis cambios"   → add + commit + push guiado
  • "crea una rama"      → rama con nombre automático siguiendo GitFlow
  • "haz un PR"          → Pull Request con descripción generada
  • "haz pull"           → trae cambios y maneja conflictos
  • "cambia de rama"     → switch seguro con verificación

El agente siempre habla en español y nunca te mostrará comandos git crudos.
```

---

### PASO 6 — Ofrecer limpiar este archivo de instalación

Preguntar:
"¿Quieres que elimine el archivo `install-git-agent.md` ahora que la instalación terminó?
Puedes conservarlo si deseas poder actualizar git-agent en el futuro con el mismo proceso."

- Si dice **sí** → eliminar este archivo desde su ubicación actual
- Si dice **no** → dejarlo para futuras actualizaciones

---

## Para desinstalar git-agent de este proyecto

```bash
rm -f .claude/agents/git-agent.md
rm -rf .claude/git-agent/
```

---

## Notas

- La instalación es **por proyecto**: solo afecta el directorio actual
- Los archivos en `.claude/git-agent/` pueden agregarse al `.gitignore` del proyecto
  si no quieres versionarlos, o commitearse si el equipo completo va a usar el agente
- Para actualizar a la versión más reciente: descarga `install-git-agent.md` de nuevo y ejecútalo
