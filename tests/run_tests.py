"""
Pruebas simuladas del git-agent.
Cada test carga los archivos .md del agente como system prompt, envía un mensaje
de usuario con salida de terminal simulada, y valida la respuesta con comprobaciones
de palabras clave.

Uso:
    python tests/run_tests.py
    python tests/run_tests.py --test 01-A
    python tests/run_tests.py --verbose
"""

import os
import sys
import time
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Union

import anthropic

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 2000
AGENT_ROOT = Path(__file__).parent.parent

# Archivos que conforman el system prompt del agente (orden importa)
AGENT_FILES = [
    "SKILL.md",
    "agent.md",
    "flows/01-commit-push.md",
    "flows/02-pull-request.md",
    "flows/03-branch-create.md",
    "flows/04-branch-switch.md",
    "flows/05-pull-update.md",
    "flows/06-edge-cases.md",
    "templates/commit-rules.md",
    "templates/pr-template.md",
]

# Colores de terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ---------------------------------------------------------------------------
# Estructuras de datos
# ---------------------------------------------------------------------------

@dataclass
class Check:
    kind: str          # "contains" | "not_contains" | "min_length"
    value: Union[str, int]
    description: str = ""


@dataclass
class TestCase:
    id: str
    name: str
    user_message: str
    checks: List[Check] = field(default_factory=list)


@dataclass
class TestResult:
    test: "TestCase"
    passed: bool
    response: str = ""
    failures: List[str] = field(default_factory=list)
    error: str = ""
    duration: float = 0.0


# ---------------------------------------------------------------------------
# Escenarios de prueba (16 en total)
# ---------------------------------------------------------------------------

TESTS: list[TestCase] = [

    # ── FLUJO 01: Commit + Push ──────────────────────────────────────────

    TestCase(
        id="01-A",
        name="Flujo 01 — Sin cambios pendientes",
        user_message=(
            "sube mis cambios\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch feature/login-validation\n"
            "nothing to commit, working tree clean\n"
        ),
        checks=[
            Check("contains", "no", "Debe indicar que no hay cambios"),
            Check("contains", "cambio", "Debe mencionar la ausencia de cambios"),
            Check("not_contains", "git add", "No debe mostrar comandos raw"),
            Check("min_length", 50, "Respuesta mínimamente elaborada"),
        ],
    ),

    TestCase(
        id="01-B",
        name="Flujo 01 — Cambios normales, sugerencia de commit",
        user_message=(
            "guarda lo que hice\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch feature/auth\n"
            "Changes not staged for commit:\n"
            "  modified: src/auth/login.js\n"
            "  modified: src/auth/validators.js\n"
            "Untracked files:\n"
            "  src/auth/tests/login.test.js\n\n"
            "$ git diff --stat\n"
            " src/auth/login.js        | 24 ++++++\n"
            " src/auth/validators.js   | 18 ++++\n"
            " src/auth/tests/login.test.js | 35 ++++++++\n"
        ),
        checks=[
            Check("contains", "feat", "Debe sugerir tipo de commit feat"),
            Check("contains", "auth", "Debe detectar scope auth"),
            Check("not_contains", "git add", "No debe mostrar comandos raw en respuesta principal"),
            Check("min_length", 100, "Respuesta detallada"),
        ],
    ),

    TestCase(
        id="01-C",
        name="Flujo 01 — Archivo sensible detectado (.env)",
        user_message=(
            "haz commit de todo\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch feature/config\n"
            "Untracked files:\n"
            "  .env\n"
            "  src/config.js\n"
        ),
        checks=[
            Check("contains", "sensible", "Debe alertar sobre archivo sensible"),
            Check("contains", ".env", "Debe mencionar el archivo .env"),
            Check("contains", "⚠", "Debe mostrar advertencia visual"),
            Check("min_length", 80, "Respuesta con alerta"),
        ],
    ),

    TestCase(
        id="01-D",
        name="Flujo 01 — Alerta al estar en rama main",
        user_message=(
            "commitea mis cambios\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch main\n"
            "Changes not staged for commit:\n"
            "  modified: README.md\n\n"
            "$ git branch --show-current\n"
            "main\n"
        ),
        checks=[
            Check("contains", "main", "Debe mencionar que está en main"),
            Check("contains", "⚠", "Debe mostrar advertencia"),
            Check("contains", "rama", "Debe mencionar la opción de crear rama"),
            Check("min_length", 80, "Respuesta con alerta"),
        ],
    ),

    TestCase(
        id="01-E",
        name="Flujo 01 — Archivos eliminados, preguntar intención",
        user_message=(
            "sube mis cambios\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch feature/cleanup\n"
            "Changes not staged for commit:\n"
            "  modified:  src/app.js\n"
            "  deleted:   src/old-utils.js\n"
            "  deleted:   src/deprecated/legacy.js\n"
        ),
        checks=[
            Check("contains", "eliminado", "Debe preguntar sobre archivos eliminados"),
            Check("contains", "intencional", "Debe preguntar si fue intencional"),
            Check("contains", "old-utils", "Debe listar el archivo eliminado"),
            Check("min_length", 80, "Respuesta con pregunta"),
        ],
    ),

    # ── FLUJO 02: Pull Request ───────────────────────────────────────────

    TestCase(
        id="02-A",
        name="Flujo 02 — Crear PR en GitHub con gh CLI disponible",
        user_message=(
            "quiero hacer un PR\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git branch --show-current\n"
            "feature/login-validation\n\n"
            "$ git remote -v\n"
            "origin  https://github.com/empresa/mi-app.git (fetch)\n"
            "origin  https://github.com/empresa/mi-app.git (push)\n\n"
            "$ git log origin/develop..HEAD --oneline\n"
            "a3f2b1c feat(auth): add login form validation\n"
            "b4e5c2d test(auth): add unit tests for validators\n\n"
            "$ which gh\n"
            "/usr/local/bin/gh\n"
            "$ gh --version\n"
            "gh version 2.40.0\n"
        ),
        checks=[
            Check("contains", "PR", "Debe mencionar la creación del PR"),
            Check("contains", "feature/login-validation", "Debe mencionar la rama actual"),
            Check("contains", "develop", "Debe mencionar la rama base"),
            Check("min_length", 150, "Respuesta con preview del PR"),
        ],
    ),

    TestCase(
        id="02-B",
        name="Flujo 02 — GitHub sin gh CLI (fallback a URL)",
        user_message=(
            "abre un pull request\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git branch --show-current\n"
            "feature/payment-module\n\n"
            "$ git remote -v\n"
            "origin  https://github.com/empresa/shop-app.git (fetch)\n"
            "origin  https://github.com/empresa/shop-app.git (push)\n\n"
            "$ git log origin/develop..HEAD --oneline\n"
            "c1d2e3f feat(payment): integrate Stripe checkout\n\n"
            "$ which gh\n"
            "gh not found\n"
        ),
        checks=[
            Check("contains", "github.com", "Debe incluir URL de GitHub"),
            Check("contains", "feature/payment-module", "Debe incluir la rama en la URL"),
            Check("contains", "develop", "Debe mencionar rama base"),
            Check("min_length", 100, "Respuesta con instrucciones"),
        ],
    ),

    # ── FLUJO 03: Crear Rama ─────────────────────────────────────────────

    TestCase(
        id="03-A",
        name="Flujo 03 — Crear rama feature sin cambios pendientes",
        user_message=(
            "quiero crear una rama nueva para trabajar en el módulo de notificaciones\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch develop\n"
            "nothing to commit, working tree clean\n\n"
            "$ git branch --show-current\n"
            "develop\n"
        ),
        checks=[
            Check("contains", "feature", "Debe sugerir prefijo feature"),
            Check("contains", "notificacion", "Debe incluir el nombre del trabajo"),
            Check("contains", "develop", "Debe sugerir develop como base"),
            Check("min_length", 100, "Respuesta con propuesta de nombre"),
        ],
    ),

    TestCase(
        id="03-B",
        name="Flujo 03 — Crear rama con cambios pendientes",
        user_message=(
            "crea una nueva rama para el dashboard\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch feature/old-work\n"
            "Changes not staged for commit:\n"
            "  modified: src/components/Header.jsx\n"
            "  modified: src/styles/main.css\n"
        ),
        checks=[
            Check("contains", "cambio", "Debe preguntar qué hacer con los cambios"),
            Check("contains", "guardar", "Debe ofrecer opción de guardar"),
            Check("min_length", 80, "Respuesta con pregunta"),
        ],
    ),

    # ── FLUJO 04: Cambiar Rama ───────────────────────────────────────────

    TestCase(
        id="04-A",
        name="Flujo 04 — Cambiar a rama existente sin cambios",
        user_message=(
            "muéveme a la rama develop\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git branch --show-current\n"
            "feature/login-validation\n\n"
            "$ git branch -a\n"
            "* feature/login-validation\n"
            "  develop\n"
            "  main\n"
            "  remotes/origin/develop\n"
            "  remotes/origin/main\n"
            "  remotes/origin/feature/payment-module\n\n"
            "$ git status\n"
            "On branch feature/login-validation\n"
            "nothing to commit, working tree clean\n"
        ),
        checks=[
            Check("contains", "develop", "Debe mencionar rama destino"),
            Check("contains", "confirma", "Debe pedir confirmación (acción crítica)"),
            Check("min_length", 80, "Respuesta con confirmación"),
        ],
    ),

    TestCase(
        id="04-B",
        name="Flujo 04 — Cambiar rama con cambios sin guardar",
        user_message=(
            "switch a main\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git branch --show-current\n"
            "feature/notifications\n\n"
            "$ git status\n"
            "On branch feature/notifications\n"
            "Changes not staged for commit:\n"
            "  modified: src/notifications/service.js\n"
            "  modified: src/notifications/template.html\n"
        ),
        checks=[
            Check("contains", "cambio", "Debe alertar sobre cambios sin guardar"),
            Check("contains", "perder", "Debe advertir sobre posible pérdida"),
            Check("min_length", 80, "Respuesta con opciones"),
        ],
    ),

    # ── FLUJO 05: Pull / Update ──────────────────────────────────────────

    TestCase(
        id="05-A",
        name="Flujo 05 — Pull simple sin conflictos",
        user_message=(
            "trae los últimos cambios\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git branch --show-current\n"
            "feature/dashboard\n\n"
            "$ git status\n"
            "On branch feature/dashboard\n"
            "nothing to commit, working tree clean\n\n"
            "$ git fetch --all\n"
            "Fetching origin\n\n"
            "$ git log HEAD..origin/feature/dashboard --oneline\n"
            "e5f6a7b feat(dashboard): add chart component\n"
            "f6g7h8i fix(dashboard): correct data formatting\n"
        ),
        checks=[
            Check("contains", "2", "Debe mencionar la cantidad de cambios"),
            Check("contains", "feature/dashboard", "Debe mencionar la rama"),
            Check("min_length", 80, "Respuesta informativa"),
        ],
    ),

    TestCase(
        id="05-B",
        name="Flujo 05 — Pull con cambios pendientes (stash automático)",
        user_message=(
            "actualiza mi rama\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git branch --show-current\n"
            "feature/reports\n\n"
            "$ git status\n"
            "On branch feature/reports\n"
            "Changes not staged for commit:\n"
            "  modified: src/reports/generator.js\n\n"
            "$ git fetch --all\n"
            "Fetching origin\n\n"
            "$ git log HEAD..origin/feature/reports --oneline\n"
            "d4e5f6a chore(reports): update dependencies\n"
        ),
        checks=[
            Check("contains", "pausa", "Debe comunicar la pausa de cambios"),
            Check("contains", "momentáneamente", "Debe usar lenguaje natural del stash"),
            Check("not_contains", "stash", "No debe mostrar el término técnico stash"),
            Check("min_length", 100, "Respuesta con comunicación de stash"),
        ],
    ),

    TestCase(
        id="05-C",
        name="Flujo 05 — Pull con conflictos",
        user_message=(
            "haz pull\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git pull origin feature/checkout\n"
            "Auto-merging src/checkout/cart.js\n"
            "CONFLICT (content): Merge conflict in src/checkout/cart.js\n"
            "Auto-merging src/checkout/summary.js\n"
            "CONFLICT (content): Merge conflict in src/checkout/summary.js\n"
            "Automatic merge failed; fix conflicts and then commit the result.\n\n"
            "$ git diff --name-only --diff-filter=U\n"
            "src/checkout/cart.js\n"
            "src/checkout/summary.js\n"
        ),
        checks=[
            Check("contains", "conflicto", "Debe explicar el conflicto"),
            Check("contains", "cart.js", "Debe listar los archivos con conflicto"),
            Check("contains", "opci", "Debe presentar opciones de resolución"),
            Check("min_length", 150, "Respuesta con menú de opciones"),
        ],
    ),

    # ── FLUJO 06: Casos de Borde ─────────────────────────────────────────

    TestCase(
        id="06-A",
        name="Flujo 06 — Rama remota eliminada",
        user_message=(
            "sube mis cambios\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git push origin feature/old-feature\n"
            "error: src refspec feature/old-feature does not match any\n"
            "error: failed to push some refs to 'origin'\n"
            "remote ref does not exist\n"
        ),
        checks=[
            Check("contains", "eliminad", "Debe explicar que la rama fue eliminada"),
            Check("contains", "opci", "Debe presentar opciones al usuario"),
            Check("min_length", 100, "Respuesta con opciones"),
        ],
    ),

    TestCase(
        id="06-B",
        name="Flujo 06 — Rama local y remota divergidas",
        user_message=(
            "sube mis cambios\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git status\n"
            "On branch feature/payments\n"
            "Your branch and 'origin/feature/payments' have diverged,\n"
            "and have 2 and 3 different commits each, respectively.\n"
        ),
        checks=[
            Check("contains", "diverge", "Debe explicar la divergencia o usar sinónimo"),
            Check("contains", "2", "Debe mencionar los commits locales"),
            Check("contains", "3", "Debe mencionar los commits del servidor"),
            Check("min_length", 100, "Respuesta con explicación y opciones"),
        ],
    ),

    TestCase(
        id="06-C",
        name="Flujo 06 — Sin upstream configurado",
        user_message=(
            "push\n\n"
            "--- SALIDA DE TERMINAL ---\n"
            "$ git push\n"
            "fatal: The current branch feature/new-feature has no upstream branch.\n"
            "To push the current branch and set the remote as upstream, use:\n"
            "    git push --set-upstream origin feature/new-feature\n"
        ),
        checks=[
            Check("contains", "servidor", "Debe explicar que la rama no existe en el servidor"),
            Check("contains", "crea", "Debe indicar que se creará la rama"),
            Check("not_contains", "--set-upstream", "No debe mostrar comandos raw"),
            Check("min_length", 80, "Respuesta con explicación"),
        ],
    ),
]


# ---------------------------------------------------------------------------
# Carga del system prompt
# ---------------------------------------------------------------------------

def load_system_prompt() -> str:
    parts = []
    for relative_path in AGENT_FILES:
        full_path = AGENT_ROOT / relative_path
        if full_path.exists():
            content = full_path.read_text(encoding="utf-8")
            parts.append(f"# === {relative_path} ===\n\n{content}")
        else:
            print(f"{YELLOW}⚠ Archivo no encontrado: {relative_path}{RESET}")
    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------
# Validación de checks
# ---------------------------------------------------------------------------

def run_checks(response: str, checks: List[Check]) -> List[str]:
    failures = []
    response_lower = response.lower()

    for check in checks:
        if check.kind == "contains":
            if check.value.lower() not in response_lower:
                desc = check.description or f"debe contener '{check.value}'"
                failures.append(f"FALTA '{check.value}' — {desc}")

        elif check.kind == "not_contains":
            if check.value.lower() in response_lower:
                desc = check.description or f"no debe contener '{check.value}'"
                failures.append(f"NO ESPERADO '{check.value}' — {desc}")

        elif check.kind == "min_length":
            if len(response) < check.value:
                desc = check.description or f"longitud mínima {check.value}"
                failures.append(f"RESPUESTA MUY CORTA ({len(response)} chars, mínimo {check.value}) — {desc}")

    return failures


# ---------------------------------------------------------------------------
# Runner principal
# ---------------------------------------------------------------------------

def run_test(client: anthropic.Anthropic, system_prompt: str, test: TestCase, verbose: bool) -> TestResult:
    start = time.time()
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": test.user_message}],
        )
        response_text = response.content[0].text
        duration = time.time() - start

        failures = run_checks(response_text, test.checks)
        return TestResult(
            test=test,
            passed=len(failures) == 0,
            response=response_text,
            failures=failures,
            duration=duration,
        )

    except anthropic.RateLimitError:
        return TestResult(test=test, passed=False, error="Rate limit — espera un momento y reintenta")
    except anthropic.APIStatusError as e:
        return TestResult(test=test, passed=False, error=f"Error de API: {e.status_code} {e.message}")
    except anthropic.APIConnectionError as e:
        return TestResult(test=test, passed=False, error=f"Error de conexión: {e}")


def print_result(result: TestResult, verbose: bool) -> None:
    icon = f"{GREEN}✅ PASS{RESET}" if result.passed else f"{RED}❌ FAIL{RESET}"
    duration_str = f"{result.duration:.1f}s" if result.duration > 0 else ""

    print(f"  {icon}  [{result.test.id}] {result.test.name}  {CYAN}{duration_str}{RESET}")

    if result.error:
        print(f"       {RED}ERROR: {result.error}{RESET}")

    if not result.passed and result.failures:
        for f in result.failures:
            print(f"       {YELLOW}· {f}{RESET}")

    if verbose and result.response:
        print(f"\n{CYAN}--- Respuesta del agente ---{RESET}")
        print(result.response[:1200])
        if len(result.response) > 1200:
            print(f"  {YELLOW}[... {len(result.response) - 1200} chars más ...]{RESET}")
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Pruebas simuladas del git-agent")
    parser.add_argument("--test", help="Ejecutar solo un test por ID (ej: 01-A)")
    parser.add_argument("--verbose", action="store_true", help="Mostrar respuesta completa del agente")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(f"{RED}Error: variable ANTHROPIC_API_KEY no configurada{RESET}")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\n{BOLD}Cargando system prompt del agente...{RESET}")
    system_prompt = load_system_prompt()
    print(f"  {len(system_prompt):,} caracteres en {len(AGENT_FILES)} archivos\n")

    selected_tests = TESTS
    if args.test:
        selected_tests = [t for t in TESTS if t.id == args.test]
        if not selected_tests:
            print(f"{RED}No se encontró el test con ID '{args.test}'{RESET}")
            sys.exit(1)

    print(f"{BOLD}Ejecutando {len(selected_tests)} prueba(s) con modelo {MODEL}...{RESET}\n")

    results: List[TestResult] = []
    flows_seen: set = set()

    for test in selected_tests:
        flow_prefix = test.id.split("-")[0]
        if flow_prefix not in flows_seen:
            flow_label = {
                "01": "Flujo 01 — Commit + Push",
                "02": "Flujo 02 — Pull Request",
                "03": "Flujo 03 — Crear Rama",
                "04": "Flujo 04 — Cambiar Rama",
                "05": "Flujo 05 — Pull / Update",
                "06": "Flujo 06 — Casos de Borde",
            }.get(flow_prefix, f"Flujo {flow_prefix}")
            print(f"{BOLD}{flow_label}{RESET}")
            flows_seen.add(flow_prefix)

        result = run_test(client, system_prompt, test, args.verbose)
        results.append(result)
        print_result(result, args.verbose)

        # Pausa breve para no saturar la API
        if test != selected_tests[-1]:
            time.sleep(1)

    # ── Resumen final ──────────────────────────────────────────────────────
    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    total_time = sum(r.duration for r in results)

    print(f"\n{BOLD}{'━' * 50}{RESET}")
    print(f"{BOLD}Resultados: {GREEN}{passed} pasaron{RESET}  {RED}{failed} fallaron{RESET}  "
          f"de {len(results)} pruebas  {CYAN}({total_time:.1f}s total){RESET}")

    if failed > 0:
        print(f"\n{BOLD}Pruebas fallidas:{RESET}")
        for r in results:
            if not r.passed:
                print(f"  {RED}· [{r.test.id}] {r.test.name}{RESET}")
        sys.exit(1)
    else:
        print(f"\n{GREEN}{BOLD}¡Todas las pruebas pasaron!{RESET}")


if __name__ == "__main__":
    main()
