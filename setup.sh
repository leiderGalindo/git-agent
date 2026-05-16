#!/usr/bin/env bash
# git-agent installer
# Usage: curl -sSL https://raw.githubusercontent.com/leiderGalindo/git-agent/main/setup.sh | bash

set -euo pipefail

BASE="https://raw.githubusercontent.com/leiderGalindo/git-agent/main"

# Check if already installed
if [ -f ".claude/agents/git-agent.md" ]; then
  echo "git-agent ya está instalado en este proyecto."
  printf "¿Actualizar a la versión más reciente? (s/n): "
  read -r REPLY
  if [[ ! "$REPLY" =~ ^[sS]$ ]]; then
    echo "Instalación cancelada. Se conserva la versión actual."
    exit 0
  fi
fi

echo "Instalando git-agent..."
mkdir -p .claude/agents .claude/git-agent/flows .claude/git-agent/templates

echo "  Descargando agente principal..."
curl -sSL "$BASE/.claude/agents/git-agent.md"   -o .claude/agents/git-agent.md

echo "  Descargando flujos de trabajo..."
curl -sSL "$BASE/flows/01-commit-push.md"        -o .claude/git-agent/flows/01-commit-push.md
curl -sSL "$BASE/flows/02-pull-request.md"       -o .claude/git-agent/flows/02-pull-request.md
curl -sSL "$BASE/flows/03-branch-create.md"      -o .claude/git-agent/flows/03-branch-create.md
curl -sSL "$BASE/flows/04-branch-switch.md"      -o .claude/git-agent/flows/04-branch-switch.md
curl -sSL "$BASE/flows/05-pull-update.md"        -o .claude/git-agent/flows/05-pull-update.md
curl -sSL "$BASE/flows/06-edge-cases.md"         -o .claude/git-agent/flows/06-edge-cases.md

echo "  Descargando plantillas..."
curl -sSL "$BASE/templates/commit-rules.md"      -o .claude/git-agent/templates/commit-rules.md
curl -sSL "$BASE/templates/pr-template.md"       -o .claude/git-agent/templates/pr-template.md

# Verify integrity
if ! head -1 .claude/agents/git-agent.md 2>/dev/null | grep -q "^---"; then
  echo ""
  echo "Error: la descarga parece incompleta. Verifica tu conexión e intenta de nuevo."
  exit 1
fi

FLOW_COUNT=$(ls .claude/git-agent/flows/ 2>/dev/null | wc -l | tr -d ' ')
TMPL_COUNT=$(ls .claude/git-agent/templates/ 2>/dev/null | wc -l | tr -d ' ')

if [ "$FLOW_COUNT" -ne 6 ] || [ "$TMPL_COUNT" -ne 2 ]; then
  echo "Advertencia: se esperaban 6 flujos y 2 plantillas, se encontraron $FLOW_COUNT y $TMPL_COUNT."
fi

echo ""
echo "git-agent instalado correctamente en este proyecto."
echo ""
echo "Archivos instalados:"
echo "  .claude/agents/git-agent.md          (agente)"
echo "  .claude/git-agent/flows/             (6 flujos)"
echo "  .claude/git-agent/templates/         (2 plantillas)"
echo ""
echo "Ahora puedes decirle a Claude:"
echo '  "sube mis cambios"'
echo '  "crea una rama"'
echo '  "haz un PR"'
echo '  "haz pull"'
echo '  "cambia de rama"'
