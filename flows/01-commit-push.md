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

**Si hay archivos eliminados (🗑️):**
→ Preguntar antes de continuar:
"Veo que se eliminaron estos archivos: [lista]. ¿Fue intencional o fue un accidente?"
- Si fue **accidental** → `git checkout -- <archivo>` para cada uno, con mensaje: "Restauré [archivo] como estaba antes."
- Si fue **intencional** → continuar normalmente.

**Verificación de archivos sensibles:**
→ Revisar si algún archivo nuevo o modificado podría ser sensible.
  Patrones de riesgo: `.env`, `*.env`, `.env.*`, `*.key`, `*.pem`, `*.p12`, archivos con `credentials`, `secrets` o `token` en el nombre.

Si detecta alguno → Alertar:
"⚠️ Detecté un archivo que podría contener información sensible: `[archivo]`.
Generalmente estos archivos no deben subirse al repositorio. ¿Lo incluimos de todas formas?"
- Si confirma incluirlo → continuar
- Si no → `git rm --cached <archivo>` para excluirlo, y preguntar si desea agregarlo al `.gitignore`

---

### PASO 2 — Validar la rama actual
```bash
git branch --show-current
```

⚠️ **Si la rama actual es `main` o `master`:**
→ Alertar al usuario:
"⚠️ Estás en la rama `main`. Normalmente no se trabaja directamente aquí.

¿Qué prefieres hacer?
1. 🌿 Crear una rama nueva para estos cambios (recomendado)
2. ⚠️ Continuar en `main` de todas formas (confirmar)"

- Si elige **opción 1** → Ejecutar Flujo 03 para crear la rama → continuar este flujo desde PASO 3
- Si elige **opción 2** → Esperar confirmación explícita → continuar al PASO 3

---

### PASO 3 — Generar mensaje de commit
1. Ejecutar `git diff --cached --stat` y `git diff --cached` para ver exactamente qué está staged
2. Si nada está staged aún, ejecutar `git diff --stat` para ver cambios sin stagear
3. Aplicar el razonamiento de los **4 pasos** definidos en `templates/commit-rules.md` → sección "Prompt de generación"
4. Verificar si existe `.commitlintrc` o `commitlint.config.js` — si existe, leerlo y ajustar el resultado

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
  SÍ → ¿Hay archivos eliminados? → Preguntar si fue intencional
       ¿Hay archivos sensibles? → Alertar y confirmar
       → ¿Estás en main?
           SÍ → ¿Crear rama nueva o continuar en main?
                Crear rama → Flujo 03 → continuar
                Continuar → Confirmar explícitamente
           NO → Continuar
                → Generar commit message (4 pasos) → Confirmar con usuario
                → git add + git commit
                → ¿Hacer push? (CONFIRMAR)
                  SÍ → git push
                       → ¿Crear PR?
                  NO → Fin
```
