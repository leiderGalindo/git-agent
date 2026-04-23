# Flujo 03: Crear Nueva Rama

## Cuándo se activa
El usuario dice algo como:
- "crea una rama", "nueva rama", "necesito una rama para..."
- "voy a empezar algo nuevo", "quiero trabajar en una feature"
- "crea un branch"

---

## Pasos del flujo

### PASO 1 — Verificar cambios pendientes
```bash
git status
git diff --stat
```

**Si hay cambios sin commit:**
→ Preguntar al usuario:
"Tienes cambios que aún no guardaste. ¿Qué quieres hacer con ellos antes de crear la nueva rama?

1. 💾 Guardar (commit) y continuar creando la rama
2. 💾📤 Guardar, subir (push) y crear PR antes de la nueva rama
3. ⏭️ Ignorarlos por ahora y crear la rama de todas formas

¿Qué prefieres?"

- Opción 1 → Ejecutar Flujo 01 (solo hasta commit, sin push) → continuar aquí
- Opción 2 → Ejecutar Flujo 01 completo + Flujo 02 → continuar aquí
- Opción 3 → Continuar directamente al PASO 2

**Si no hay cambios:**
→ Continuar al PASO 2.

---

### PASO 2 — Determinar tipo de rama
Preguntar en lenguaje simple:
"¿Qué tipo de trabajo vas a hacer en esta nueva rama?

🚀 Nueva funcionalidad (feature)
🐛 Corrección de error (fix)
🚨 Corrección urgente en producción (hotfix)
📦 Preparar un lanzamiento (release)
🔧 Tarea de mantenimiento o configuración (chore)
📝 Solo documentación (docs)"

→ Según la respuesta, asignar el prefijo de rama correspondiente.

---

### PASO 3 — Definir nombre de la rama
Preguntar: "¿Cómo se llama lo que vas a trabajar? Descríbelo brevemente."

→ El agente genera el nombre de rama automáticamente:
- Convertir a minúsculas
- Reemplazar espacios por guiones `-`
- Eliminar caracteres especiales
- Agregar prefijo según tipo

Ejemplo: "login con Google" → `feature/login-con-google`

→ Confirmar con el usuario:
"El nombre de la rama sería: `feature/login-con-google`
¿Está bien o quieres cambiarlo?"

---

### PASO 4 — Determinar rama base (ACCIÓN CRÍTICA)
Preguntar al usuario:
"¿Desde dónde quieres crear esta rama?

🌿 Desde `develop` (recomendado para features y fixes)
🏠 Desde `main` (solo para hotfixes o releases)
📍 Desde la rama en la que estoy ahora (`<rama-actual>`)
🔀 Desde otra rama (dime cuál)"

→ Según el tipo de rama seleccionado en el PASO 2, mostrar la recomendación:
- `feature/*`, `fix/*`, `chore/*`, `docs/*` → sugerir `develop`
- `hotfix/*`, `release/*` → sugerir `main`

---

### PASO 5 — Crear la rama
```bash
git checkout <rama-base>
git pull origin <rama-base>   # Asegurarse de tener la versión más reciente
git checkout -b <nombre-rama>
```

→ Mostrar confirmación:
"✅ ¡Listo! Se creó la rama `feature/login-con-google` a partir de `develop`.
Ya estás trabajando en ella. Cuando termines, recuérdame subirla con 'sube mis cambios'."

---

## Diagrama de decisión

```
¿Hay cambios pendientes?
  SÍ → ¿Qué hacemos con ellos? → commit / commit+push+PR / ignorar
  NO → Continuar

→ ¿Qué tipo de rama? → Determinar prefijo
→ ¿Nombre del trabajo? → Generar nombre
→ ¿Desde qué rama base? (CONFIRMAR)
→ git checkout base + pull + checkout -b nueva-rama
→ Confirmar éxito al usuario
```
