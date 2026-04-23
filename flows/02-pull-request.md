# Flujo 02: Crear Pull Request

## Cuándo se activa
El usuario dice algo como:
- "crea un PR", "abre un pull request", "quiero hacer un PR"
- "manda esto a revisión", "solicita revisión de código"
- También se activa automáticamente al final del Flujo 01 si el usuario lo solicita.

---

## Pasos del flujo

### PASO 1 — Recopilar contexto del repositorio
```bash
git branch --show-current          # Rama actual
git remote -v                      # URL del remoto → detectar plataforma
git log origin/<base>..HEAD --oneline  # Commits nuevos respecto a la base
git diff origin/<base>...HEAD --stat   # Archivos cambiados
```

**Detectar plataforma:**
- URL contiene `github.com` → GitHub
- URL contiene `bitbucket.org` → Bitbucket
- URL contiene `gitlab.com` → GitLab

**Determinar rama base automáticamente:**
| Rama actual | Rama base |
|---|---|
| `feature/*` | `develop` |
| `fix/*` | `develop` |
| `chore/*` | `develop` |
| `docs/*` | `develop` |
| `hotfix/*` | `main` |
| `release/*` | `main` |
| Cualquier otra | Preguntar al usuario |

---

### PASO 2 — Verificar si ya existe un PR abierto
Intentar detectar si ya existe un PR para esta rama usando la CLI de la plataforma:
- GitHub: `gh pr list --head <rama-actual>`
- Bitbucket/GitLab: informar al usuario que verifique manualmente si ya existe uno.

**Si ya existe un PR:**
→ Notificar: "Ya existe un PR abierto para esta rama. ¿Quieres actualizarlo o crear uno nuevo?"

---

### PASO 3 — Verificar plantilla del proyecto
Buscar en este orden:
1. `.github/pull_request_template.md`
2. `.github/PULL_REQUEST_TEMPLATE.md`
3. `docs/pull_request_template.md`
4. `bitbucket/pull_request_template.md`
5. `PULL_REQUEST_TEMPLATE.md` (raíz)

Si encuentra → usar esa plantilla.
Si no encuentra → usar `templates/pr-template.md` por defecto.

---

### PASO 4 — Generar título del PR
Analizar los commits y cambios para generar un título descriptivo.

→ Mostrar al usuario:
"Sugerí este título para tu PR:
`[FEATURE] Agregar validación en formulario de login`
¿Lo dejamos así o quieres cambiarlo?"

---

### PASO 5 — Generar descripción automática
Analizar `git diff` y commits para pre-llenar:
- **Descripción**: resumen de qué se hizo y por qué
- **Lista de cambios**: basada en los archivos y commits

→ Mostrar borrador al usuario para revisión.

---

### PASO 6 — Recopilar información adicional del usuario

**Evidencias visuales:**

Primero evaluar si aplica según el tipo de cambio (ver tabla en pr-template.md).

- Si aplica → preguntar:
  "¿Tienes evidencias visuales para agregar al PR? (capturas de pantalla, videos, GIFs)
  Puedes pegarlas aquí o escribir 'omitir' si no tienes."

- Si no aplica → poner automáticamente "No aplica para este tipo de cambio"

**Bloqueantes:**
→ Preguntar: "¿Hay algo que bloquee el merge de este PR? Por ejemplo, otro PR del que depende, una configuración pendiente, etc.
Si no hay nada, escribe 'ninguno'."

**Comentarios adicionales:**
→ Preguntar: "¿Quieres dejarle algún comentario al revisor? Por ejemplo, áreas en las que quieres feedback específico, decisiones técnicas que tomaste, etc.
Si no hay nada, escribe 'ninguno'."

---

### PASO 7 — Mostrar preview del PR (ACCIÓN CRÍTICA)
→ Mostrar el PR completo formateado para revisión del usuario:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PREVIEW DEL PULL REQUEST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔀 Rama: feature/login-validation → develop
📌 Título: [FEATURE] Agregar validación en formulario de login

📋 Descripción:
Se implementó la validación del formulario de login para...

✅ Cambios:
- Validación de email con regex
- Mensaje de error en campos vacíos
- Tests unitarios del componente

🖼️ Evidencias: [las que el usuario proporcionó / No aplica]
🚫 Bloqueantes: Ninguno
💬 Comentarios: Revisar especialmente la lógica de...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Creamos el PR con esta información?
```

→ Esperar confirmación del usuario.

---

### PASO 8 — Crear el PR

**GitHub con `gh` CLI disponible** (`gh_cli_available: true` en config):
```bash
gh pr create \
  --title "<título>" \
  --body "<cuerpo>" \
  --base <rama-base> \
  --head <rama-actual>
```
→ Mostrar: "✅ PR creado exitosamente. Puedes verlo aquí: [link que devuelve gh]"

---

**GitHub sin `gh` CLI** (`gh_cli_available: false`):
→ Notificar:
"No tengo la herramienta `gh` instalada, así que no puedo crear el PR directamente.
Te doy todo para crearlo en menos de un minuto:"

1. Abre este link:
   `https://github.com/<owner>/<repo>/compare/<rama-base>...<rama-actual>`

2. Pega este título: `<título>`

3. Pega esta descripción:
   `<cuerpo completo en markdown>`

→ Preguntar: "¿Quieres que te muestre cómo instalar `gh` para automatizar esto en el futuro?"
- Si sí → mostrar instrucciones según sistema operativo:
  - macOS: `brew install gh`
  - Linux (apt): `sudo apt install gh`
  - Windows: `winget install GitHub.cli`
  - Nota: "Después de instalarlo, el agente lo detectará automáticamente en la próxima sesión."

---

**Bitbucket / GitLab:**
→ Construir URL con ramas pre-cargadas:
  - Bitbucket: `https://bitbucket.org/<workspace>/<repo>/pull-requests/new?source=<rama-actual>&dest=<rama-base>`
  - GitLab: `https://gitlab.com/<namespace>/<repo>/-/merge_requests/new?merge_request[source_branch]=<rama-actual>&merge_request[target_branch]=<rama-base>`

→ Intentar abrir el navegador automáticamente:
```bash
# macOS:
open "<url>"
# Linux:
xdg-open "<url>"
# Windows:
start "<url>"
```

→ Mostrar al usuario:
"Intenté abrir el navegador en la página de creación del PR con tu rama ya seleccionada.
Si no se abrió automáticamente, usa este link: [url]"

→ Mostrar el cuerpo del PR en markdown formateado, listo para copiar y pegar en el campo de descripción.

---

## Diagrama de decisión

```
Detectar rama actual + plataforma + rama base
→ ¿Ya existe PR? → Notificar opciones
→ ¿Hay plantilla del proyecto? → Usar esa / usar default
→ Generar título + descripción automática
→ Pedir evidencias (si aplica) + bloqueantes + comentarios
→ Mostrar preview (CONFIRMAR)
→ Crear PR en plataforma
```
