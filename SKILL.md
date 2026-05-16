---
name: git-agent
description: >
  Agente de automatización de Git en lenguaje natural. Úsalo cuando el usuario quiera realizar
  cualquier operación de Git sin escribir comandos: subir cambios, hacer commit, crear o cambiar ramas,
  abrir Pull Requests, traer actualizaciones del servidor, o resolver situaciones de conflicto.
  También se activa con frases como: "sube mis cambios", "crea una rama", "haz pull", "quiero hacer un PR",
  "guarda lo que hice", "cambia de rama", "actualiza mi código", "manda esto a revisión".
  Funciona con GitHub y Bitbucket, sigue Conventional Commits, GitFlow y genera PRs en español.
  Usar en cualquier proyecto de software sin configuración previa.
---

# Git Agent

Asistente de control de versiones que convierte lenguaje natural en operaciones Git seguras y guiadas.
Diseñado para equipos con perfiles mixtos: funciona igual para desarrolladores experimentados y usuarios sin conocimiento técnico de Git.

> **Nota:** El agente principal está definido en `.claude/agents/git-agent.md`.
> Para instalar en un proyecto nuevo, consulta el README o usa `install-git-agent.md`.

## Capacidades

- ✅ Guardar y subir cambios (add + commit + push)
- ✅ Crear Pull Requests con descripción automática
- ✅ Crear ramas siguiendo GitFlow
- ✅ Cambiar entre ramas con verificación de seguridad
- ✅ Actualizar rama con cambios del servidor (pull)
- ✅ Resolución guiada de conflictos con opciones interactivas
- ✅ Auto-detección de plataforma (GitHub / Bitbucket)
- ✅ Compatible con cualquier proyecto

## Estructura del agente

```
git-agent/
├── .claude/agents/git-agent.md   ← Subagente consolidado (punto de entrada principal)
├── install-git-agent.md          ← Skill de instalación por proyecto
├── SKILL.md                      ← Este archivo (entrada legacy / slash command)
├── agent.md                      ← Fuente: comportamiento y reglas
├── flows/
│   ├── 01-commit-push.md         ← Fuente: add + commit + push
│   ├── 02-pull-request.md        ← Fuente: Pull Request
│   ├── 03-branch-create.md       ← Fuente: crear rama
│   ├── 04-branch-switch.md       ← Fuente: cambiar rama
│   ├── 05-pull-update.md         ← Fuente: pull y conflictos
│   └── 06-edge-cases.md          ← Fuente: casos especiales
├── templates/
│   ├── commit-rules.md           ← Fuente: Conventional Commits
│   └── pr-template.md            ← Fuente: plantilla de PR
└── scripts/
    └── build.py                  ← Genera .claude/agents/git-agent.md
```

## Instrucciones para Claude

1. **Lee `.claude/agents/git-agent.md`** — contiene el comportamiento completo del agente.
2. **Identifica la intención del usuario** usando la tabla de intenciones en ese archivo.
3. **Ejecuta el flujo correspondiente** siguiendo los pasos definidos.
4. **Detecta y respeta** las convenciones del proyecto antes que las plantillas por defecto.

## Compatibilidad

| Plataforma | Soporte |
|---|---|
| GitHub | ✅ Completo (gh CLI si disponible, fallback con link si no) |
| Bitbucket | ✅ Completo (abre navegador con link pre-configurado) |
| GitLab | ⚠️ Parcial (abre navegador con link pre-configurado) |

| Estrategia de ramas | Soporte |
|---|---|
| GitFlow (main, develop, feature, hotfix, release) | ✅ |
| GitHub Flow (main + feature) | ✅ |
| Sin estrategia definida | ✅ (modo flexible) |
