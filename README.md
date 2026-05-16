# Git Agent

Agente de automatización de Git en lenguaje natural. Convierte frases cotidianas en operaciones Git seguras y guiadas, sin que el usuario necesite conocer los comandos.

Diseñado para equipos con perfiles mixtos: funciona igual para desarrolladores experimentados y usuarios sin conocimiento técnico de Git.

---

## Instalación

La instalación es **por proyecto** — el agente solo estará disponible en los proyectos donde lo instales.

### Opción 1 — Dile a Claude (sin comandos)

Si ya tienes Claude Code abierto en el proyecto, dale esta instrucción exacta:

> "Instala git-agent ejecutando: `curl -sSL https://raw.githubusercontent.com/leiderGalindo/git-agent/main/setup.sh | bash`"

Claude ejecutará el script directamente. No necesitas abrir la terminal ni recordar ningún comando.

### Opción 2 — Con skill de instalación

**Paso 1:** Descarga el skill de instalación en el proyecto donde quieres usar git-agent:

```bash
mkdir -p .claude/agents
curl -sSL https://raw.githubusercontent.com/leiderGalindo/git-agent/main/install-git-agent.md \
  -o .claude/agents/install-git-agent.md
```

**Paso 2:** Dile a Claude en ese proyecto:

> "instala git-agent"

Claude descargará y configurará todo automáticamente (agente + 6 flujos + 2 plantillas).
Al terminar, te preguntará si conservar el skill de instalación para futuras actualizaciones.

### Opción 3 — One-liner (para usuarios técnicos)

```bash
curl -sSL https://raw.githubusercontent.com/leiderGalindo/git-agent/main/setup.sh | bash
```

Descarga e instala todo en un solo comando (agente + 6 flujos + 2 plantillas).

### Para desarrolladores del agente

```bash
git clone https://github.com/leiderGalindo/git-agent.git
cd git-agent
python scripts/build.py        # genera .claude/agents/git-agent.md
python tests/run_tests.py      # valida el agente (requiere ANTHROPIC_API_KEY)
```

### Desinstalar

```bash
rm -f .claude/agents/git-agent.md
rm -rf .claude/git-agent/
```

---

## Qué hace

| El usuario dice... | Lo que ocurre |
|---|---|
| "sube mis cambios", "haz commit", "push" | add + commit + push con mensaje generado automáticamente |
| "crea un PR", "manda a revisión" | Genera título y descripción del PR, crea en GitHub o abre link para Bitbucket/GitLab |
| "crea una rama", "nueva rama" | Guía el tipo, nombre y rama base; crea la rama siguiendo GitFlow |
| "cambia de rama", "muéveme a develop" | Verifica cambios pendientes, confirma y cambia; ofrece respaldo opcional |
| "actualiza mi rama", "haz pull" | Trae cambios, gestiona conflictos y maneja el stash automáticamente |

---

## Características principales

- **Lenguaje natural** — el usuario nunca escribe comandos git
- **Conventional Commits** — mensajes de commit generados automáticamente en inglés
- **PRs en español** — descripciones de Pull Request generadas en español por defecto
- **Detección de archivos sensibles** — alerta ante `.env`, `*.key`, `*.pem` y similares antes de hacer commit
- **Manejo guiado de conflictos** — 4 opciones interactivas cuando hay merge conflicts
- **Configuración persistente** — guarda preferencias del proyecto en `.git-agent-config.json` para no preguntar dos veces
- **Multi-plataforma** — GitHub (con o sin `gh` CLI), Bitbucket y GitLab parcial
- **Compatible con cualquier proyecto** — no requiere configuración previa

---

## Estructura del proyecto

```
git-agent/
├── SKILL.md                  ← Punto de entrada del agente (registro como skill)
├── agent.md                  ← Comportamiento, reglas, tabla de intenciones y manejo de errores
├── flows/
│   ├── 01-commit-push.md     ← Flujo: add + commit + push
│   ├── 02-pull-request.md    ← Flujo: crear o actualizar Pull Request
│   ├── 03-branch-create.md   ← Flujo: crear nueva rama
│   ├── 04-branch-switch.md   ← Flujo: cambiar de rama
│   ├── 05-pull-update.md     ← Flujo: pull y resolución de conflictos
│   └── 06-edge-cases.md      ← Casos especiales y situaciones de borde
├── templates/
│   ├── commit-rules.md       ← Estándar Conventional Commits (default: inglés)
│   └── pr-template.md        ← Estructura de PR (default: español)
└── tests/
    ├── run_tests.py           ← Suite de pruebas automatizadas con la API de Anthropic
    └── requirements.txt       ← Dependencia: anthropic SDK
```

---

## Cómo funciona

### Arquitectura

El agente es un conjunto de archivos Markdown que actúan como instrucciones estructuradas para Claude. No tiene código ejecutable propio — Claude lee los archivos y los sigue como un protocolo de comportamiento.

```
Usuario → Claude (con SKILL.md + agent.md como contexto)
             ↓
         Identifica intención
             ↓
         Lee flows/<flujo>.md
             ↓
         Ejecuta comandos git, procesa resultados
             ↓
         Comunica al usuario en español sin jerga técnica
```

### Flujo de activación

1. Claude detecta la intención del usuario usando la tabla de intenciones en `agent.md`
2. Lee el archivo de flujo correspondiente en `flows/`
3. Ejecuta los pasos en orden (comandos bash, validaciones, confirmaciones)
4. Consulta las plantillas en `templates/` cuando el flujo lo indica
5. Siempre comunica en español claro, nunca muestra comandos git crudos al usuario

### Auto-detección al inicio

Al activarse, el agente detecta silenciosamente:
- Plataforma del repositorio (GitHub / Bitbucket / GitLab) mediante `git remote -v`
- Rama actual y estado del repositorio
- Disponibilidad de `gh` CLI para crear PRs en GitHub
- Convenciones del proyecto (`.commitlintrc`, `.github/pull_request_template.md`, `CONTRIBUTING.md`)
- Configuración guardada en `.git-agent-config.json`

---

## Flujos detallados

### Flujo 01 — Guardar y subir cambios

1. Revisa `git status` y muestra un resumen en lenguaje natural (modificados, nuevos, eliminados)
2. Alerta si hay archivos sensibles (`.env`, `*.key`, etc.) — pide confirmación antes de incluirlos
3. Alerta si la rama actual es `main` o `master` — ofrece crear una rama nueva
4. Genera el mensaje de commit automáticamente siguiendo Conventional Commits (4 pasos: tipo → scope → descripción → cuerpo si es necesario)
5. Pide confirmación del mensaje — el usuario puede editarlo
6. Ejecuta `git add .` + `git commit`
7. Pide confirmación para el push (acción crítica)
8. Al terminar, ofrece crear un PR

### Flujo 02 — Pull Request

1. Detecta plataforma, rama actual y rama base automáticamente por tipo (`feature/*` → `develop`, `hotfix/*` → `main`, etc.)
2. Verifica si ya existe un PR abierto para la rama
3. Busca plantilla del proyecto; si no existe, usa `templates/pr-template.md`
4. Genera título y descripción automáticamente a partir de los commits y el diff
5. Pregunta por evidencias visuales (solo si aplica según el tipo de cambio), bloqueantes y comentarios para el revisor
6. Muestra un preview completo del PR antes de crearlo
7. **GitHub con `gh` CLI**: crea el PR directamente con `gh pr create`
8. **GitHub sin `gh`**: genera el link de comparación listo para pegar en el navegador, más instrucciones para instalar `gh`
9. **Bitbucket / GitLab**: construye la URL con ramas pre-cargadas e intenta abrirla en el navegador

### Flujo 03 — Crear rama

1. Verifica cambios pendientes — ofrece guardarlos antes de continuar
2. Pregunta el tipo de trabajo (feature, fix, hotfix, release, chore, docs)
3. Pide descripción breve del trabajo y genera el nombre de rama automáticamente (`"login con Google"` → `feature/login-con-google`)
4. Sugiere la rama base según el tipo y pide confirmación
5. Ejecuta `git checkout <base>` + `git pull` + `git checkout -b <nueva-rama>`

### Flujo 04 — Cambiar de rama

1. Lista todas las ramas disponibles (locales y remotas) de forma legible
2. Verifica cambios sin commit — ofrece guardarlos antes de cambiar
3. Pide confirmación explícita antes de ejecutar el checkout (acción crítica)
4. Tras el cambio, ofrece crear una rama de respaldo (`backup/<rama>-<fecha>`) para preservar el estado actual

### Flujo 05 — Actualizar rama (pull)

1. Muestra cuántos commits nuevos hay en el servidor antes de bajarlos
2. Maneja el stash automáticamente si hay cambios pendientes, con comunicación en lenguaje natural ("voy a poner en pausa tus cambios momentáneamente")
3. Si el pull genera conflictos, presenta 4 opciones:
   - Conservar mis cambios (ours)
   - Conservar los del servidor (theirs)
   - Revisar archivo por archivo
   - Pedir ayuda al equipo / abortar el merge

### Flujo 06 — Casos de borde

| Situación | Manejo |
|---|---|
| Rama remota eliminada | Explica qué pasó y da 3 opciones: recrear, verificar si el trabajo ya está en otra rama, o eliminar la copia local |
| Más de 10 commits sin push | Muestra la lista completa antes de hacer push para revisión |
| Archivos eliminados sin stagear | Pregunta si fue intencional o accidental; restaura si fue accidental |
| Rama local y remota divergidas | Explica la situación y ofrece merge, rebase o force-push (con doble advertencia) |
| Sin upstream configurado | Explica que la rama no existe en el servidor y la crea automáticamente con `--set-upstream` |

---

## Manejo de errores

El agente traduce todos los errores de Git a español claro:

| Error de Git | Mensaje al usuario |
|---|---|
| `rejected — non-fast-forward` | "Hay cambios en el servidor que no tienes localmente. Primero necesitamos traer esos cambios." |
| `Authentication failed` | "Hay un problema con tu acceso al repositorio. Verifica tus credenciales." |
| `not a git repository` | "Esta carpeta no está conectada a un repositorio Git. ¿Estás en la carpeta correcta?" |
| `nothing to commit` | "No hay cambios nuevos. ¿Guardaste los archivos en tu editor?" |
| `branch already exists` | "Ya existe una rama con ese nombre. ¿Usamos otra o la que ya existe?" |
| `CONFLICT` | Activa el sub-flujo de resolución de conflictos con 4 opciones |

---

## Configuración del proyecto

En la primera sesión de cada proyecto el agente pregunta el idioma preferido para commits y PRs, y guarda la elección en `.git-agent-config.json`:

```json
{
  "platform": "github | bitbucket | gitlab",
  "commit_language": "english",
  "pr_language": "spanish",
  "base_branches": {
    "feature": "develop",
    "fix": "develop",
    "hotfix": "main",
    "release": "main"
  },
  "commit_standard": "conventional-commits",
  "gh_cli_available": true,
  "language_configured": true
}
```

Esta configuración se reutiliza en sesiones futuras. Si el proyecto tiene `.commitlintrc` o `commitlint.config.js`, esas reglas tienen prioridad sobre el estándar por defecto.

---

## Compatibilidad

| Plataforma | Soporte |
|---|---|
| GitHub | Completo (gh CLI si disponible, fallback con link si no) |
| Bitbucket | Completo (abre navegador con link pre-configurado) |
| GitLab | Parcial (abre navegador con link pre-configurado) |

| Estrategia de ramas | Soporte |
|---|---|
| GitFlow (main, develop, feature, hotfix, release) | Completo |
| GitHub Flow (main + feature) | Completo |
| Sin estrategia definida | Modo flexible |

---

## Tests

La suite de pruebas simula conversaciones completas con el agente a través de la API de Anthropic y valida que las respuestas cumplan con los requisitos de comportamiento definidos.

**Requisitos:**
```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-...
```

**Ejecutar todas las pruebas:**
```bash
python tests/run_tests.py
```

**Ejecutar un test específico:**
```bash
python tests/run_tests.py --test 01-A
```

**Ver respuestas completas del agente:**
```bash
python tests/run_tests.py --verbose
```

### Pruebas incluidas (16 en total)

| ID | Escenario |
|---|---|
| 01-A | Sin cambios pendientes |
| 01-B | Cambios normales — sugerencia de commit con scope `auth` |
| 01-C | Archivo sensible detectado (`.env`) |
| 01-D | Alerta al estar en rama `main` |
| 01-E | Archivos eliminados — preguntar intención |
| 02-A | Crear PR en GitHub con `gh` CLI disponible |
| 02-B | GitHub sin `gh` CLI — fallback a URL |
| 03-A | Crear rama feature sin cambios pendientes |
| 03-B | Crear rama con cambios pendientes |
| 04-A | Cambiar a rama existente sin cambios |
| 04-B | Cambiar rama con cambios sin guardar |
| 05-A | Pull simple sin conflictos |
| 05-B | Pull con cambios pendientes (stash automático) |
| 05-C | Pull con conflictos — menú de opciones |
| 06-A | Rama remota eliminada |
| 06-B | Rama local y remota divergidas |
| 06-C | Sin upstream configurado |

Cada prueba verifica que la respuesta contenga las palabras clave esperadas, omita comandos git crudos hacia el usuario, y tenga una longitud mínima razonable.
