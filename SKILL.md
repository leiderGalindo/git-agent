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

## Capacidades

- ✅ Guardar y subir cambios (add + commit + push)
- ✅ Crear Pull Requests con descripción automática
- ✅ Crear ramas siguiendo GitFlow
- ✅ Cambiar entre ramas con verificación de seguridad
- ✅ Actualizar rama con cambios del servidor (pull)
- ✅ Resolución guiada de conflictos con opciones interactivas
- ✅ Auto-detección de plataforma (GitHub / Bitbucket)
- ✅ Compatible con cualquier proyecto

## Inicio rápido

Al activarse, el agente:
1. Detecta automáticamente el estado del repositorio y la plataforma
2. Lee la configuración del proyecto (si existe)
3. Identifica la intención del usuario
4. Ejecuta el flujo correspondiente con confirmación en pasos críticos

## Archivos del agente

```
git-agent/
├── SKILL.md                  ← Este archivo (punto de entrada)
├── agent.md                  ← Cerebro: comportamiento, reglas, tabla de intenciones
├── flows/
│   ├── 01-commit-push.md     ← add + commit + push
│   ├── 02-pull-request.md    ← Crear / actualizar PR
│   ├── 03-branch-create.md   ← Crear nueva rama
│   ├── 04-branch-switch.md   ← Cambiar de rama
│   ├── 05-pull-update.md     ← Pull y manejo de conflictos
│   └── 06-edge-cases.md      ← Casos especiales y situaciones de borde
└── templates/
    ├── commit-rules.md       ← Conventional Commits en inglés (default)
    └── pr-template.md        ← Estructura de PR en español (default)
```

## Instrucciones para Claude

1. **Lee `agent.md`** — contiene las reglas de comportamiento, tabla de intenciones y manejo de errores.
2. **Identifica la intención del usuario** usando la tabla de intenciones en `agent.md`.
3. **Lee el flujo correspondiente** en `flows/` y síguelo paso a paso.
4. **Consulta las plantillas** en `templates/` cuando el flujo lo indique.
5. **Detecta y respeta** las convenciones del proyecto antes que las plantillas por defecto.

## Configuración por proyecto

El agente guarda la configuración detectada en `.git-agent-config.json` en la raíz del proyecto.
Esto evita preguntar las mismas cosas en cada sesión.

Si el usuario trabaja en múltiples proyectos, cada uno tiene su propia configuración independiente.

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
