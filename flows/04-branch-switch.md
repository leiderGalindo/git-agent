# Flujo 04: Cambiar de Rama (git switch / checkout)

## Cuándo se activa
El usuario dice algo como:
- "cambia de rama", "quiero ir a la rama X", "muéveme a develop"
- "switch a main", "ve a la rama de producción"
- "quiero revisar la versión de..."

---

## Pasos del flujo

### PASO 1 — Obtener rama actual y listar ramas disponibles
```bash
git branch --show-current          # Rama actual
git branch -a                      # Todas las ramas (locales y remotas)
```

→ Mostrar al usuario la lista de ramas disponibles de forma limpia:
"Estas son las ramas disponibles:

📍 Estás aquí: `feature/login-validation`

Ramas locales:
  • develop
  • main
  • feature/login-validation (actual)

Ramas remotas disponibles:
  • feature/payment-module
  • hotfix/checkout-error

¿A cuál quieres ir?"

---

### PASO 2 — Verificar cambios pendientes
```bash
git status
```

**Si hay cambios sin commit:**
→ Notificar y preguntar:
"Tienes cambios sin guardar en `<rama-actual>`. Si cambias de rama ahora, esos cambios podrían perderse.

¿Qué hacemos?
💾 Guardar los cambios (commit) antes de cambiar
🚀 Guardar y subir (commit + push) antes de cambiar
⏭️ Cambiar de todas formas (los cambios se moverán con nosotros si no hay conflicto)"

- Opción 1 → Ejecutar Flujo 01 hasta commit → continuar
- Opción 2 → Ejecutar Flujo 01 completo → continuar
- Opción 3 → Continuar directamente al PASO 3

**Si no hay cambios:**
→ Continuar al PASO 3.

---

### PASO 3 — Ejecutar el cambio de rama (ACCIÓN CRÍTICA)
→ Confirmar antes de ejecutar:
"Vas a pasar de `<rama-origen>` → `<rama-destino>`. ¿Confirmamos?"

```bash
git checkout <rama-destino>
# Si es una rama remota que no existe en local:
git checkout -b <rama-destino> origin/<rama-destino>
```

---

### PASO 4 — Mostrar mensaje de cambio exitoso + alerta de versión

→ Mostrar siempre este mensaje al cambiar:

```
✅ Cambiaste de rama exitosamente

  📤 Origen:  feature/login-validation
  📥 Destino: develop

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  ANTES DE HACER CAMBIOS EN ESTA RAMA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Si quieres experimentar sin afectar `develop`,
te recomiendo guardar una versión del estado actual.

¿Quieres que cree una rama de respaldo desde aquí?
```

---

### PASO 5 — Manejo de la respuesta a la alerta

**Si el usuario dice SÍ (quiere dejar una versión / respaldo):**

→ Preguntar: "¿Cómo quieres llamar a esta versión? Puedes describirlo brevemente o dejarme sugerirla."

→ Generar nombre sugerido: `backup/<rama-destino>-<fecha>` 
   Ejemplo: `backup/develop-2025-01-15`

→ Ejecutar:
```bash
git checkout -b <nombre-backup>    # Crear rama de respaldo desde aquí
git checkout <rama-destino>        # Volver a la rama destino
```

→ Notificar al usuario:
"✅ ¡Listo! Dejé una copia del estado actual en la rama `backup/develop-2025-01-15`.
Ahora estás trabajando en `develop` y tienes ese respaldo si lo necesitas.

Cuando quieras retomar desde ese punto, dime 'cambia a backup/develop-2025-01-15'."

**Si el usuario dice NO:**
→ Fin del flujo. Confirmar en qué rama está.

---

## Diagrama de decisión

```
Listar ramas → Usuario elige destino
→ ¿Hay cambios sin commit?
    SÍ → ¿Qué hacemos? → commit / commit+push / ignorar
    NO → Continuar

→ Confirmar cambio (CRÍTICO)
→ git checkout <destino>
→ Mostrar mensaje origen → destino + alerta
→ ¿Quieres crear un respaldo?
    SÍ → Crear rama backup → volver a destino → notificar
    NO → Fin
```
