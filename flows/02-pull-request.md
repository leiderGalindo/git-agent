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

**GitHub (usando gh CLI):**
```bash
gh pr create \
  --title "<título>" \
  --body "<cuerpo>" \
  --base <rama-base> \
  --head <rama-actual>
```

**Bitbucket / GitLab sin CLI:**
→ Generar el cuerpo del PR en markdown listo para copiar y pegar.
→ Proporcionar el link directo para crear el PR:
  - Bitbucket: `https://bitbucket.org/<workspace>/<repo>/pull-requests/new?source=<rama>`
  - GitLab: `https://gitlab.com/<namespace>/<repo>/-/merge_requests/new?merge_request[source_branch]=<rama>`

→ Mostrar: "✅ PR creado exitosamente. Puedes verlo aquí: [link]"

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
