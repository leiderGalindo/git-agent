# Flujo 06: Casos Especiales y Situaciones de Borde

Este archivo documenta cómo manejar situaciones excepcionales que no están cubiertas
en los flujos principales. El agente debe consultar este archivo cuando detecte
uno de estos patrones durante la ejecución de cualquier flujo.

---

## Caso A — Rama remota fue eliminada

### Cuándo ocurre
El usuario intenta hacer push y recibe `error: remote ref does not exist`,
o el agente detecta que `origin/<rama>` ya no aparece en `git fetch --all`.

### Manejo
→ Notificar:
"La rama `<nombre>` ya no existe en el servidor. Es posible que alguien la eliminó
porque el PR ya fue aprobado, cerrado, o como parte de una limpieza del repositorio."

→ Preguntar:
"¿Qué quieres hacer?
1. 🔄 Volver a crearla en el servidor (subir mi versión local)
2. 🔍 Ver si mi trabajo ya está en otra rama (develop o main)
3. 🗑️ Eliminar también mi copia local de esa rama"

- Opción 1 → `git push origin <rama>` (se recreará automáticamente)
- Opción 2 → `git log origin/develop..HEAD --oneline` para buscar los commits
- Opción 3 → `git branch -d <rama>` — advertir si tiene commits sin mergear:
  "⚠️ Esta rama tiene commits que aún no están en ninguna otra rama. Si la eliminas, perderías ese trabajo. ¿Estás seguro?"

---

## Caso B — Muchos commits sin push

### Cuándo ocurre
`git log origin/<rama>..HEAD --oneline` retorna más de 10 commits.

### Manejo
→ Notificar antes de hacer push:
"⚠️ Tienes [X] commits locales que no han sido subidos al servidor.
Es bastante trabajo acumulado. Antes de subir:

[mostrar lista con git log origin/<rama>..HEAD --oneline]

¿Seguimos con el push de todos estos commits?"

- Si confirma → push normal
- Si quiere revisar → ofrecer mostrar el diff de algún commit específico:
  "¿Quieres que te muestre los cambios de alguno de ellos?"

---

## Caso C — Archivos eliminados sin stagear

### Cuándo ocurre
`git status` muestra archivos en estado `deleted` pero no staged.
Se detecta en el PASO 1 del Flujo 01.

### Manejo
→ Mostrar la lista de eliminaciones por separado y preguntar:
"🗑️ Detecté que se eliminaron estos archivos:
- [lista]

¿Fue intencional?"

- Si fue intencional → `git add -A` o `git rm <archivos>` para stagear las eliminaciones
- Si fue accidental → `git checkout -- <archivo>` para restaurar cada uno, con mensaje:
  "Restauré [archivo] como estaba antes."

---

## Caso D — Rama local divergida del remoto

### Cuándo ocurre
`git status` muestra `"Your branch and 'origin/<rama>' have diverged"` o
`git log --oneline origin/<rama>...HEAD` muestra commits en ambas direcciones.

### Manejo
→ Notificar:
"⚠️ Tu rama local y la del servidor divergen — tienen cambios diferentes y separados.
Esto ocurre cuando alguien más subió cambios a la misma rama mientras tú también trabajabas.

• Tu rama tiene [X] commits que el servidor no tiene.
• El servidor tiene [Y] commits que tú no tienes.

¿Cómo quieres resolver esto?
1. 🔄 Mezclar ambas versiones (recomendado — preserva todo el trabajo)
2. ⬇️ Traer lo del servidor primero y poner mis cambios encima (más ordenado)
3. ⬆️ Subir mis cambios y reemplazar lo del servidor (solo si estás seguro)"

- Opción 1 → `git pull origin <rama>` (merge)
- Opción 2 → `git fetch origin && git rebase origin/<rama>`
  — Advertir: "Este proceso reorganiza tus commits. Si hay conflictos, los resolveremos uno a uno."
- Opción 3 → `git push --force-with-lease` (nunca `--force`)
  — Advertencia doble: "⚠️ Esto reemplazará lo que hay en el servidor. Los cambios subidos por otros se perderán. ¿Estás completamente seguro?"
  — Pedir confirmación explícita antes de ejecutar.

---

## Caso E — No hay upstream configurado

### Cuándo ocurre
`git push` falla con: `fatal: The current branch has no upstream branch`

### Manejo
→ Explicar:
"Esta rama existe en tu máquina pero aún no en el servidor.
Al subirla por primera vez, se creará automáticamente."

→ Ejecutar:
```bash
git push --set-upstream origin <rama>
```

→ Notificar: "✅ La rama `<rama>` fue creada en el servidor y tus cambios fueron subidos."

Si la plataforma devuelve un link para crear PR en el output → mostrárselo al usuario:
"También puedes crear un PR directamente desde aquí: [link]"
