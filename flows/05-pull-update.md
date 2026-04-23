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

**Por defecto:** traer cambios de `origin/<rama-actual>` — sincronizar tu rama con lo que otros subieron.

→ Informar: "Voy a traer los cambios más recientes de `<rama-actual>` del servidor."

→ Preguntar opcionalmente:
"¿También quieres integrar cambios de otra rama como `develop` o `main`?
Si no, escribe 'no' o continúa."

- Si especifica otra rama → aplicar `git pull origin <otra-rama>` **después** del pull principal
- Si dice 'no' o no responde → continuar solo con `origin/<rama-actual>`

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
- Si NO → Continuar al PASO 4 (pull con pausa automática)

---

### PASO 4 — Pull con cambios sin commit (pausa automática)

→ **Antes de ejecutar**, notificar al usuario:
"Voy a poner en pausa momentáneamente tus cambios para poder traer lo del servidor sin conflictos. Los recuperaré automáticamente al terminar."

```bash
git stash push -m "auto-stash antes de pull <fecha>"
git pull origin <rama-actual>
git stash pop
```

→ **Si todo sale bien:**
"✅ Restauré tus cambios. Tu rama está actualizada y tu trabajo sigue intacto. Revisa que todo esté bien."

→ **Si el restore falla:**
"⚠️ Ocurrió un problema al restaurar tus cambios. No los perdiste — están guardados de forma segura.
Avísame y lo resolvemos juntos — no hagas nada más hasta que te indique."

---

### PASO 5 — Ejecutar el pull
```bash
git pull origin <rama-actual>
```

**Si también se eligió otra rama en PASO 2:**
```bash
git pull origin <otra-rama>
```

**Si el pull es exitoso:**
→ Mostrar:
"✅ ¡Listo! Tu rama `<rama-actual>` está actualizada con los últimos cambios.
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

**PASO C2 — Presentar opciones al usuario:**
```
⚠️  HAY CONFLICTOS EN TU CÓDIGO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Los siguientes archivos tienen cambios que chocan:
  • [lista de archivos en conflicto]

Esto ocurre cuando tú y alguien más editaron las mismas
líneas de código. Git necesita que decidas cuál versión conservar.

¿Cómo quieres resolverlos?

1. 🔵 Conservar MIS cambios (los que yo tenía localmente)
2. 🟢 Conservar los cambios del SERVIDOR (los que llegaron del remoto)
3. ✏️  Revisar archivo por archivo y decidir en cada uno
4. 🤝 Necesito ayuda de alguien del equipo
```

**PASO C3 — Ejecutar según opción elegida:**

**Opción 1 — Conservar mis cambios:**
```bash
# Para cada archivo con conflicto:
git checkout --ours <archivo>
git add <archivo>
```
→ Notificar: "Listo. Conservé tus versiones. Los cambios del servidor en esos archivos fueron descartados."
→ Ir al PASO C4.

**Opción 2 — Conservar cambios del servidor:**
```bash
# Para cada archivo con conflicto:
git checkout --theirs <archivo>
git add <archivo>
```
→ Notificar: "Listo. Quedaron las versiones del servidor. Tus cambios locales en esos archivos fueron descartados."
→ Ir al PASO C4.

**Opción 3 — Revisar archivo por archivo:**
→ Para cada archivo con conflicto, mostrar:
```
Archivo: <nombre>

TU VERSIÓN (lo que tenías tú):
<mostrar líneas marcadas con <<<<<<< HEAD>

VERSIÓN DEL SERVIDOR:
<mostrar líneas marcadas con >>>>>>> origin/...>

¿Qué hacemos con este archivo?
1. Conservar mi versión  2. Conservar la del servidor  3. Abrir en editor
```
→ Aplicar elección con `git checkout --ours` o `--theirs` según corresponda.
→ Cuando todos estén resueltos → ir al PASO C4.

**Opción 4 — Necesito ayuda del equipo:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🤝 CONTACTA A TU EQUIPO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comparte los archivos en conflicto con un desarrollador
de tu equipo para resolverlos juntos.

Cuando estén listos, dime "los conflictos están resueltos".

¿Quieres cancelar el merge y volver al estado anterior?
→ Di "abortar" y lo haré sin perder tu trabajo.
```
→ Si el usuario dice "abortar": `git merge --abort` + notificar: "Cancelé el merge. Tu rama volvió al estado anterior sin ninguna pérdida."
→ Si dice "resueltos": ir al PASO C4.

**PASO C4 — Commit de resolución:**
```bash
git add .
git commit -m "resolve: merge conflicts with <rama-fuente>"
```
→ Confirmar: "✅ Conflictos resueltos y guardados. Tu rama está actualizada."

---

## Diagrama de decisión

```
Fetch → informar cuántos cambios hay por bajar
→ ¿Rama de pull? (default: rama actual, opcional: otra rama)
→ ¿Hay cambios sin commit?
    SÍ → ¿Hacer commit primero?
           SÍ → Flujo 01 hasta commit
           NO → Notificar al usuario → git stash → pull → stash pop
                ¿Stash pop exitoso?
                  SÍ → ✅ Informar restauración
                  NO → ⚠️ Avisar, no ejecutar nada más
    NO → git pull directamente

→ ¿Pull exitoso?
    SÍ → ✅ Informar cambios bajados
    NO (conflictos) → ⚠️ Identificar archivos → Presentar 4 opciones
                       Opción 1: ours → add → C4 commit
                       Opción 2: theirs → add → C4 commit
                       Opción 3: archivo por archivo → add → C4 commit
                       Opción 4: equipo / abortar
```
