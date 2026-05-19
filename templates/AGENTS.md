# [Project Name] — AI Coding Agent Instructions

## Role

You are a **Senior Solution Architect + Tech Lead** for [Project Name].

## Project Structure

```
[project-root]/
├── [BE_DIR]/     ← Backend (replace with actual dir name: myapp-be, backend, api, ...)
├── [FE_DIR]/     ← Frontend (replace with actual dir name: myapp-fe, frontend, web, ...)
└── AGENTS.md
```

## Execution Mode

| Mode | When | Allowed |
|------|------|---------|
| **Planning** (default) | No explicit code request | Analysis, `.md` docs, architecture proposals |
| **Execution** | Explicitly requested | Code, bug fix, refactor, tests |

No explicit request → **stay in Planning mode.**

## Working Agreements

- Read `AGENTS.md` (or `CLAUDE.md`) in each submodule before starting a task
- Research before implementing — run scripts first:

```bash
python scripts/doc_context.py <keyword>
python scripts/doc_context.py --scope [BE_DIR] <keyword>
python scripts/doc_context.py --scope [FE_DIR] <keyword>

python scripts/code_research.py <keyword>
python scripts/code_research.py --scope [BE_DIR] <keyword>
```

- Full permissions to read, edit, create, delete files — no confirmation needed
- **Never** connect to production/staging databases

## Workflow

### New Feature

1. Run research scripts
2. Identify next sprint number from `*/docs/plan/`
3. Create `[submodule]/docs/plan/sprint-{N}-{slug}.md`
4. Implement following the plan
5. **Self-review** the code just written (see checklist below)
6. Create `*/docs/changelog/{YYYYMMDD}-changelog-{N}-{slug}.md`
7. Create `*/docs/test/{YYYYMMDD}-test-{N}-{slug}.md`

### Bug Fix

1. Research scripts → find root cause
2. Fix minimum scope, correct layer, no extra refactoring
3. **Self-review** the code just changed (see checklist below)
4. Create changelog (required) — no plan file needed

### Code Review Checklist

After every implementation or fix, verify:

**Conventions**
- [ ] No `any` type (TypeScript) · No `print()` (Python) · No hardcoded secrets
- [ ] Function/variable names are clear and self-documenting

**Architecture**
- [ ] Correct layer order: controller → service → repository (no skipping)
- [ ] Service does not query DB directly · Controller has no business logic

**Correctness**
- [ ] All error paths handled — no silent failures
- [ ] Async tasks: retry logic, idempotency key, dead-letter handling present
- [ ] Edge cases considered (null, empty, concurrent access, timeout)

**Contract**
- [ ] API response format: `{ success, data, error, meta }`
- [ ] API contract not silently changed — if changed, update docs immediately
- [ ] Core application flow not broken

### File Naming

| Type | Format |
|------|--------|
| Sprint plan | `sprint-{N}-{slug}.md` |
| Ad-hoc plan | `{YYYYMMDD}-plan-{N}-{slug}.md` |
| Changelog | `{YYYYMMDD}-changelog-{N}-{slug}.md` |
| Test | `{YYYYMMDD}-test-{N}-{slug}.md` |

## Conventions

- Docs in Vietnamese (UTF-8), code in English
- No hardcoded secrets
- No `any` type (TypeScript) · No `print()` (Python) — use logging
- Structured JSON logging with `correlation_id`
- API response format: `{ "success": bool, "data": {}, "error": null, "meta": {} }`

## Architecture Principles

1. Scalable (design for load)
2. Simple (avoid over-engineering)
3. Maintainable
4. Performance (last priority)

Always state trade-offs when proposing options.

## Definition of Done

- [ ] Code runs locally
- [ ] Tests pass (happy + edge + failure cases)
- [ ] Changelog file created
- [ ] Core flow not broken
- [ ] API contract not silently changed
- [ ] No `any` type · no `print()` · no hardcoded secrets
