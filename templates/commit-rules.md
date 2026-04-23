# Commit Rules

## Default Standard: Conventional Commits (English)

All commit messages must be written in **English** and follow this format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

---

## Types

| Type | Use when... |
|---|---|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug |
| `chore` | Maintenance tasks, dependencies, config |
| `docs` | Documentation changes only |
| `style` | Formatting, missing semicolons, no logic change |
| `refactor` | Code restructuring without fixing bugs or adding features |
| `test` | Adding or updating tests |
| `perf` | Performance improvements |
| `ci` | CI/CD configuration changes |
| `revert` | Reverting a previous commit |
| `hotfix` | Urgent fix for production |

---

## Rules

1. **Subject line max 72 characters**
2. **Use imperative mood**: "add feature" not "added feature"
3. **No period at the end of subject**
4. **Scope is optional** but recommended: `feat(auth): add login validation`
5. **Breaking changes**: Add `!` after type: `feat!: change API response format`

---

## Auto-detection

Before generating a commit message, the agent should:
1. Run `git diff --cached --stat` to see changed files
2. Run `git diff --cached` to understand what changed
3. Infer the type from the nature of changes
4. Infer the scope from the folder/module affected
5. Generate a meaningful description

---

## Examples

```
feat(auth): add JWT token refresh logic
fix(cart): resolve item duplication on reload
chore(deps): update react to v18.2
docs(api): update endpoint documentation for /users
refactor(components): extract Button into shared module
hotfix(payment): fix null reference on checkout
```

---

## Project Override

If the project has a `.commitlintrc`, `commitlint.config.js`, or `CONTRIBUTING.md`,
those rules take **priority** over this default standard.
The agent must read and apply them instead.
