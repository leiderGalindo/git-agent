"""
Genera .claude/agents/git-agent.md — versión ligera del agente.

El archivo consolidado contiene solo las reglas de comportamiento (agent.md)
más una tabla de rutas a los archivos de flujo. Claude lee cada flujo bajo
demanda usando la herramienta Read, reduciendo el system prompt de ~45 KB a ~9 KB.

Los flujos y plantillas se distribuyen en:
  .claude/git-agent/flows/      ← instalados por install-git-agent.md
  .claude/git-agent/templates/  ← instalados por install-git-agent.md

Uso:
    python scripts/build.py
"""

from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent

FRONTMATTER = """\
---
name: git-agent
description: >
  Agente de automatización de Git en lenguaje natural. Úsalo cuando el usuario quiera
  realizar cualquier operación de Git sin escribir comandos: subir cambios, hacer commit,
  crear o cambiar ramas, abrir Pull Requests, traer actualizaciones o resolver conflictos.
  Frases de activación: "sube mis cambios", "haz commit", "crea una rama", "haz pull",
  "quiero hacer un PR", "cambia de rama", "actualiza mi código", "manda esto a revisión".
model: claude-sonnet-4-6
tools: Bash, Read, Write
color: green
---"""

FLOWS_TABLE = """\
## Cómo usar los flujos

Los archivos de flujo están en `.claude/git-agent/flows/` dentro del proyecto actual.
Cuando identifiques la intención del usuario, **lee primero el flujo correspondiente**
con la herramienta `Read` y síguelo paso a paso.

| El usuario dice... | Archivo a leer |
|---|---|
| "sube mis cambios", "haz commit", "guarda lo que hice", "push" | `.claude/git-agent/flows/01-commit-push.md` |
| "crea un PR", "abre pull request", "manda a revisión" | `.claude/git-agent/flows/02-pull-request.md` |
| "crea una rama", "nueva rama", "voy a empezar algo nuevo" | `.claude/git-agent/flows/03-branch-create.md` |
| "cambia de rama", "ir a develop", "switch", "muéveme a..." | `.claude/git-agent/flows/04-branch-switch.md` |
| "actualiza mi rama", "haz pull", "trae los cambios", "sincroniza" | `.claude/git-agent/flows/05-pull-update.md` |
| Errores inesperados, rama eliminada, divergencia, sin upstream | `.claude/git-agent/flows/06-edge-cases.md` |
| Intención mixta o ambigua | Preguntar clarificación al usuario |

## Cómo usar las plantillas

Cuando el flujo indique consultar una plantilla, léela con `Read`:

| Plantilla | Archivo |
|---|---|
| Estándar de commits (Conventional Commits) | `.claude/git-agent/templates/commit-rules.md` |
| Estructura de Pull Request | `.claude/git-agent/templates/pr-template.md` |"""

SOURCES = {
    "agent": "agent.md",
    "flows": [
        "flows/01-commit-push.md",
        "flows/02-pull-request.md",
        "flows/03-branch-create.md",
        "flows/04-branch-switch.md",
        "flows/05-pull-update.md",
        "flows/06-edge-cases.md",
    ],
    "templates": [
        "templates/commit-rules.md",
        "templates/pr-template.md",
    ],
}

OUTPUT = ".claude/agents/git-agent.md"


def check_sources() -> bool:
    all_sources = [SOURCES["agent"]] + SOURCES["flows"] + SOURCES["templates"]
    missing = [s for s in all_sources if not (ROOT / s).exists()]
    if missing:
        for m in missing:
            print(f"  ERROR: Archivo fuente no encontrado: {m}", file=sys.stderr)
        return False
    return True


def build() -> None:
    print("Verificando archivos fuente...")
    if not check_sources():
        sys.exit(1)

    output_path = ROOT / OUTPUT
    output_path.parent.mkdir(parents=True, exist_ok=True)

    agent_content = (ROOT / SOURCES["agent"]).read_text(encoding="utf-8").strip()

    sections = [FRONTMATTER, agent_content, FLOWS_TABLE]
    output_content = "\n\n---\n\n".join(sections) + "\n"

    output_path.write_text(output_content, encoding="utf-8")

    lines = output_content.count("\n")
    size_kb = len(output_content.encode("utf-8")) / 1024

    flow_sizes = [(f, (ROOT / f).stat().st_size / 1024) for f in SOURCES["flows"]]
    tmpl_sizes = [(t, (ROOT / t).stat().st_size / 1024) for t in SOURCES["templates"]]

    print(f"\n✅ Agente ligero generado: {OUTPUT}")
    print(f"   Tamaño del agente: {lines:,} líneas · {size_kb:.1f} KB")
    print(f"\n   Flujos (se instalan en .claude/git-agent/flows/):")
    for path, kb in flow_sizes:
        print(f"     {Path(path).name:<30} {kb:.1f} KB")
    print(f"\n   Plantillas (se instalan en .claude/git-agent/templates/):")
    for path, kb in tmpl_sizes:
        print(f"     {Path(path).name:<30} {kb:.1f} KB")

    total_distributed = size_kb + sum(kb for _, kb in flow_sizes + tmpl_sizes)
    print(f"\n   Total distribuido: {total_distributed:.1f} KB "
          f"(vs {size_kb:.1f} KB cargados en system prompt)")


if __name__ == "__main__":
    build()
