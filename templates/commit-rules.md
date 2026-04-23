# Commit Rules

## Default Standard: Conventional Commits (English)

All commit messages must be written in **English** and follow this format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

---

## Types

| Type | Use when... |
|---|---|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug |
| `chore` | Maintenance tasks, dependencies, config |
| `docs` | Documentation changes only |
| `style` | Formatting, missing semicolons, no logic change |
| `refactor` | Code restructuring without fixing bugs or adding features |
| `test` | Adding or updating tests |
| `perf` | Performance improvements |
| `ci` | CI/CD configuration changes |
| `revert` | Reverting a previous commit |
| `hotfix` | Urgent fix for production |

---

## Rules

1. **Subject line max 72 characters**
2. **Use imperative mood**: "add feature" not "added feature"
3. **No period at the end of subject**
4. **Scope is optional** but recommended: `feat(auth): add login validation`
5. **Breaking changes**: Add `!` after type: `feat!: change API response format`

---

## Auto-detection

Before generating a commit message, the agent should:
1. Run `git diff --cached --stat` to see changed files
2. Run `git diff --cached` to understand what changed
3. Infer the type from the nature of changes
4. Infer the scope from the folder/module affected
5. Generate a meaningful description

---

## Prompt de generación de commit

Cuando generes el mensaje de commit, sigue este razonamiento interno antes de mostrar la sugerencia:

### Paso A — Clasificar el tipo de cambio
Analizar `git diff --cached` y determinar el tipo:
- Archivos nuevos con funcionalidad → `feat`
- Corrección de lógica incorrecta → `fix`
- Solo archivos de documentación (`.md`, `.txt`) → `docs`
- Archivos de configuración o dependencias (`package.json`, `.env`, `config/`) → `chore`
- Archivos de prueba (`*.test.*`, `*.spec.*`, `__tests__/`) → `test`
- Archivos de CI/CD (`.github/`, `Dockerfile`, `.gitlab-ci.yml`) → `ci`
- Restructuración sin cambio de funcionalidad → `refactor`
- Cambios de formato sin lógica → `style`
- Corrección urgente para producción → `hotfix`
- Mejoras de rendimiento → `perf`

### Paso B — Determinar el scope
Revisar las rutas de los archivos cambiados:
- Si todos pertenecen a una carpeta o módulo común → ese módulo es el scope
  Ejemplos: `src/auth/` → `auth`, `components/Button` → `ui`, `api/users` → `users`
- Si los cambios son transversales (múltiples módulos sin relación clara) → omitir el scope
- Si es un proyecto pequeño sin estructura de módulos → omitir el scope

### Paso C — Redactar la descripción
Reglas:
1. Verbo en imperativo en inglés: "add", "fix", "update", "remove", "extract", "prevent"
2. Describir el QUÉ, no el CÓMO: "add email validation" no "add regex check to email field"
3. Máximo 60 caracteres (por debajo del límite de 72)
4. Sin punto al final
5. Si hay cambios que rompen compatibilidad → agregar `!`: `feat!: change API response format`

### Paso D — Evaluar si necesita cuerpo
Agregar cuerpo solo si los cambios no son evidentes por sí solos:
- Por qué se hizo el cambio (contexto o limitación encontrada)
- Qué alternativas se descartaron (si es relevante)
Separar del subject con una línea en blanco.

### Ejemplos del razonamiento aplicado

**Ejemplo 1:**
Cambios: se agregó `src/auth/validators.js` con funciones de validación de email y contraseña
→ Tipo: `feat` (funcionalidad nueva)
→ Scope: `auth` (carpeta src/auth/)
→ Descripción: "add input validators for email and password"
→ Resultado: `feat(auth): add input validators for email and password`

**Ejemplo 2:**
Cambios: se modificó `src/cart/CartItem.jsx` corrigiendo que los items se duplicaban al recargar
→ Tipo: `fix` (corrección de error)
→ Scope: `cart` (carpeta src/cart/)
→ Descripción: "prevent item duplication on page reload"
→ Resultado: `fix(cart): prevent item duplication on page reload`

**Ejemplo 3:**
Cambios: se actualizaron `README.md` y `docs/api.md`
→ Tipo: `docs` (solo documentación)
→ Scope: omitir (múltiples docs sin módulo claro)
→ Descripción: "update API documentation and README"
→ Resultado: `docs: update API documentation and README`

---

## Examples

```
feat(auth): add JWT token refresh logic
fix(cart): resolve item duplication on reload
chore(deps): update react to v18.2
docs(api): update endpoint documentation for /users
refactor(components): extract Button into shared module
hotfix(payment): fix null reference on checkout
```

---

## Project Override

If the project has a `.commitlintrc`, `commitlint.config.js`, or `CONTRIBUTING.md`,
those rules take **priority** over this default standard.
The agent must read and apply them instead.
