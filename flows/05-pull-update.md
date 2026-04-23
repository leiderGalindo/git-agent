# Flujo 05: Actualizar Rama (git pull)

## Cuándo se activa
El usuario dice algo como:
- "actualiza mi rama", "trae los últimos cambios", "haz pull"
- "quiero bajar los cambios de...", "sincroniza con develop / main"
- "hay cambios nuevos que necesito"

---

## Pasos del flujo

### PASO 1 — Verificar estado actual
```bash
git branch --show-current
git status
git fetch --all    # Trae info del remoto sin aplicar cambios
git log HEAD..origin/<rama-actual> --oneline  # Commits por bajar
```

→ Informar al usuario cuántos cambios hay por bajar:
"En el servidor hay 3 cambios nuevos que aún no tienes en tu máquina."

---

### PASO 2 — Determinar desde qué rama hacer pull
Preguntar al usuario:
"¿De dónde quieres traer los cambios?

📍 De mi rama actual (`<rama-actual>`) — trae lo que subieron otros
🏠 De `main` (producción) — integra los últimos cambios de producción
🌿 De `develop` — integra los últimos cambios del equipo
🔀 De otra rama (dime cuál)"

---

### PASO 3 — Verificar cambios pendientes
```bash
git status
```

**Si NO hay cambios pendientes:**
→ Ir directamente al PASO 5 (hacer pull).

**Si HAY cambios sin commit:**
→ Informar al usuario:
"Tienes cambios en tu código que aún no guardaste. Si traemos los cambios del servidor ahora podría haber conflictos.

Lo más seguro es guardarlos primero. ¿Los guardamos con un commit antes de continuar?"

- Si SÍ → Ejecutar Flujo 01 hasta commit (sin push) → continuar al PASO 5
- Si NO → Continuar al PASO 4 (pull con stash automático)

---

### PASO 4 — Pull con cambios sin commit (stash automático)
```bash
git stash push -m "auto-stash antes de pull <fecha>"
# Luego hacer pull
# Luego restaurar:
git stash pop
```

→ Notificar: "Guardé tus cambios temporalmente, traje lo nuevo del servidor y restauré tu trabajo. Revisa que todo esté bien."

---

### PASO 5 — Ejecutar el pull
```bash
git pull origin <rama-elegida>
```

**Si el pull es exitoso:**
→ Mostrar:
"✅ ¡Listo! Tu rama `<rama-actual>` está actualizada con los últimos cambios de `<rama-elegida>`.
Se trajeron X commits nuevos."

**Si el pull genera CONFLICTOS:**
→ Ejecutar Flujo de Conflictos (ver abajo).

---

## Sub-flujo: Manejo de Conflictos

### Cuando ocurre
`git pull` termina con el mensaje "CONFLICT" o "Automatic merge failed".

### Pasos

**PASO C1 — Identificar archivos con conflicto:**
```bash
git diff --name-only --diff-filter=U
```

**PASO C2 — Notificar al usuario de forma clara:**
```
⚠️  HAY CONFLICTOS EN TU CÓDIGO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Los siguientes archivos tienen cambios que chocan
entre tu código y el del servidor:

  • src/components/Login.jsx
  • src/utils/validators.js

Esto significa que tú y otro desarrollador
modificaron las mismas partes del código
y Git no sabe cuál versión conservar.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤝 NECESITAS AYUDA DE TU EQUIPO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Por favor contacta a un desarrollador de tu equipo
para resolver estos conflictos juntos.

Ellos pueden ayudarte a decidir qué cambios conservar
sin perder trabajo importante.

Cuando los conflictos estén resueltos, dime
"los conflictos están resueltos" para continuar.
```

**PASO C3 — Si el usuario dice que ya están resueltos:**
```bash
git add .
git commit -m "resolve: merge conflicts with <rama-elegida>"
```

→ Confirmar: "✅ Conflictos resueltos y guardados. Tu rama está actualizada."

---

## Diagrama de decisión

```
Fetch → informar cuántos cambios hay por bajar
→ ¿De qué rama traer cambios?
→ ¿Hay cambios sin commit?
    SÍ → ¿Hacer commit primero?
           SÍ → Flujo 01 hasta commit
           NO → git stash → pull → stash pop
    NO → git pull directamente

→ ¿Pull exitoso?
    SÍ → ✅ Informar cambios bajados
    NO (conflictos) → ⚠️ Identificar archivos → Notificar → Contactar equipo
```
