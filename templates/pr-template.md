# Plantilla de Pull Request

> Esta es la plantilla por defecto. Si el proyecto tiene una plantilla propia
> en `.github/pull_request_template.md`, `docs/pull_request_template.md` o
> `bitbucket/pull_request_template.md`, usar esa en su lugar.

---

## Estructura del PR

### Título
Debe ser claro, conciso y describir el cambio principal.
Formato recomendado: `[TIPO] Descripción breve del cambio`

Ejemplos:
- `[FEATURE] Agregar autenticación con Google`
- `[FIX] Corregir error de duplicación en el carrito`
- `[HOTFIX] Resolver fallo crítico en proceso de pago`
- `[REFACTOR] Reorganizar módulo de usuarios`

---

### Cuerpo del PR (en español)

```markdown
## 📋 Descripción
<!-- Resumen breve de qué se hizo y por qué -->

## ✅ Cambios realizados
<!-- Lista de los cambios principales -->
- 
- 
- 

## 🖼️ Evidencias visuales
<!-- Opcional: capturas de pantalla, videos o GIFs que muestren el cambio -->
<!-- Si no aplica, escribir: "No aplica para este tipo de cambio" -->

## 🚫 Bloqueantes
<!-- ¿Hay algo que impida hacer merge? Dependencias, otros PRs, configuraciones -->
<!-- Si no hay, escribir: "Ninguno" -->

## 💬 Comentarios adicionales
<!-- Notas para el revisor, decisiones técnicas, deudas técnicas, etc. -->
<!-- Si no hay, escribir: "Ninguno" -->
```

---

## Reglas de rama base por tipo de rama

| Rama origen | Rama destino |
|---|---|
| `feature/*` | `develop` |
| `fix/*` | `develop` |
| `hotfix/*` | `main` + `develop` |
| `release/*` | `main` + `develop` |
| `chore/*` | `develop` |
| `docs/*` | `develop` |

---

## Evidencias visuales — Criterio de cuándo pedirlas

| Tipo de cambio | ¿Pedir evidencia? |
|---|---|
| Cambios de UI / frontend visible | ✅ Sí, recomendado |
| Corrección de bug visible en pantalla | ✅ Sí, recomendado |
| Cambios de lógica / backend | ⚪ Opcional |
| Refactor sin cambio visual | ❌ No necesario |
| Solo documentación | ❌ No necesario |
| Cambios de configuración / CI | ❌ No necesario |

---

## Detección automática de plantilla del proyecto

El agente debe buscar en este orden:
1. `.github/pull_request_template.md`
2. `.github/PULL_REQUEST_TEMPLATE.md`
3. `docs/pull_request_template.md`
4. `bitbucket/pull_request_template.md`
5. `PULL_REQUEST_TEMPLATE.md` (raíz)

Si encuentra alguna → usar esa plantilla y respetar su estructura.
Si no encuentra ninguna → usar esta plantilla por defecto.
