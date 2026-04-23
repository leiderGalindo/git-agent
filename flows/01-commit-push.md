# Flujo 01: Guardar y Subir Cambios (add + commit + push)

## Cuándo se activa
El usuario dice algo como:
- "sube mis cambios", "guarda lo que hice", "haz commit", "manda esto al repo"
- "quiero subir mi trabajo", "push", "commitea esto"

---

## Pasos del flujo

### PASO 1 — Revisar estado actual
```bash
git status
git diff --stat
```

**Si no hay cambios:**
→ Decirle al usuario: "No encontré cambios pendientes en tu proyecto. ¿Estás seguro de que guardaste los archivos en tu editor?"
→ Fin del flujo.

**Si hay cambios:**
→ Mostrar al usuario un resumen en lenguaje natural:
"Encontré cambios en X archivos:
- 📝 Modificados: [lista]
- ➕ Nuevos: [lista]
- 🗑️ Eliminados: [lista]"

---

### PASO 2 — Validar la rama actual
```bash
git branch --show-current
```

⚠️ **Si la rama actual es `main` o `master`:**
→ Alertar al usuario: "⚠️ Estás en la rama `main`. Normalmente no se sube directamente a esta rama. ¿Estás seguro de que quieres continuar aquí?"
→ Esperar confirmación antes de continuar.

---

### PASO 3 — Generar mensaje de commit
1. Ejecutar `git diff` para analizar los cambios
2. Leer `templates/commit-rules.md` para aplicar el estándar
3. Verificar si existe `.commitlintrc` o `commitlint.config.js` en el proyecto
4. Generar un mensaje de commit siguiendo Conventional Commits en **inglés**

→ Mostrar al usuario:
"Generé este mensaje de commit:
`feat(auth): add login form validation`
¿Lo dejamos así o quieres cambiarlo?"

→ Esperar respuesta del usuario (confirmar o editar).
→ **Esta es una acción de baja criticidad: si el usuario confirma, continuar.**

---

### PASO 4 — Ejecutar add + commit
```bash
git add .
git commit -m "<mensaje confirmado>"
```

→ Mostrar confirmación: "✅ Cambios guardados localmente con el mensaje: `<mensaje>`"

---

### PASO 5 — Confirmar push (ACCIÓN CRÍTICA)
→ Preguntar al usuario:
"¿Quieres subir estos cambios al repositorio remoto ahora?
📤 Esto subirá tus cambios a la rama `<rama-actual>`"

**Si confirma:**
```bash
git push origin <rama-actual>
```

**Si la rama no existe en remoto:**
```bash
git push --set-upstream origin <rama-actual>
```

→ Mostrar: "✅ Cambios subidos correctamente a `<rama-actual>`"

**Si el push falla:**
→ Capturar el error y explicarlo en lenguaje simple:
- "rejected" → "Hay cambios en el servidor que no tienes localmente. Necesitamos hacer un pull primero."
- "Authentication failed" → "Hay un problema con tus credenciales. Verifica tu acceso al repositorio."

---

### PASO 6 — Ofrecer crear PR (opcional)
→ Preguntar: "¿Quieres crear un Pull Request para estos cambios?"

**Si sí:** → Activar Flujo 02 (pull-request.md)
**Si no:** → Fin del flujo.

---

## Diagrama de decisión

```
¿Hay cambios? 
  NO → Avisar y terminar
  SÍ → ¿Estás en main?
         SÍ → ⚠️ Advertir y pedir confirmación
         NO → Continuar
              → Generar commit message → Confirmar con usuario
              → git add + git commit
              → ¿Hacer push? (CONFIRMAR)
                SÍ → git push
                     → ¿Crear PR?
                NO → Fin
```
