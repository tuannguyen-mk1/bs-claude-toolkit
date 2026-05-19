---
description: Load project context, detect task type, compute next sprint number, suggest research commands, and output a full action brief before starting any task.
arguments: [submodule-name | task-description]
---

Execute the following phases in order.

---

## PHASE 0 — Config & Stack Cache

### 0a. Read project config
Check `.bs-toolkit.json` at the project root:
- If found → read `modules` (optional name mapping), `shared_files`, **`stack_profile`**
- If not found → continue with defaults

### 0b. Check Stack Profile Cache

This step determines **how many tokens** this run will consume.

**If `stack_profile` exists in `.bs-toolkit.json` with at least `lang_be` or `lang_fe`:**
→ **⚡ FAST PATH** — use cache, **skip Phase 1 entirely**
  - Load: `lang_be`, `lang_fe`, `framework_be`, `framework_fe`, `arch`, `async_tech`, `database`, `custom_rules`, `main_flow`, `api_format`
  - Token cost: ~100 tokens
  - Jump to Phase 2

**If `stack_profile` is missing or empty:**
→ **🔍 FULL PATH** — run all of Phase 1
  - Token cost: ~1500–3000 tokens

### 0c. Resolve scope

- If `$ARGUMENTS` matches a submodule name or alias → load only that submodule
- Otherwise → load all submodules

---

## PHASE 1 — Load Context  *(FULL PATH only)*

### 1a. Root context
- Read `./CLAUDE.md`
- Read `./Agents.md` if it exists

### 1b. Detect submodules

Find all immediate subdirectories that contain `CLAUDE.md`, `Agents.md`, or a `docs/` folder.

If `.bs-toolkit.json` has a `modules` mapping (e.g. `{"be": "myapp-be"}`), use it to resolve non-standard names. Otherwise rely on content-based detection.

Apply scope filter: if a scope was set in Phase 0c, load only the matching submodule.

### 1c. Load submodule files
- Read `{subdir}/CLAUDE.md`
- Read `{subdir}/Agents.md` if it exists

### 1d. Auto-detect stack profile

Detect from **two sources**, in priority order:

#### Source 1 — Project files (most accurate)

Scan files in each submodule root:

| File | Language | Framework hints |
|------|----------|-----------------|
| `requirements.txt` / `pyproject.toml` / `Pipfile` | Python | flask→Flask · fastapi→FastAPI · django→Django · celery→async:Celery · rq→async:RQ |
| `package.json` | TypeScript/JS | next→Next.js · nuxt→Nuxt · react→React · vue→Vue · @angular→Angular · @nestjs→NestJS · express→Express · bull/bullmq→async:BullMQ |
| `go.mod` | Go | gin-gonic→Gin · labstack/echo→Echo · gofiber→Fiber |
| `pom.xml` / `build.gradle` / `build.gradle.kts` | Java/Kotlin | spring-boot→Spring Boot · quarkus→Quarkus |
| `composer.json` | PHP | laravel/framework→Laravel · symfony→Symfony |
| `Gemfile` | Ruby | rails→Rails |
| `pubspec.yaml` | Dart | flutter→Flutter |
| `Cargo.toml` | Rust | axum→Axum · actix-web→Actix |
| `*.csproj` / `*.sln` | C# | Microsoft.AspNetCore→ASP.NET Core |

**Database detection** (from deps):
`pymongo`/`motor` → MongoDB · `sqlalchemy`/`psycopg2` → PostgreSQL · `mysql2`/`pg` → MySQL · `redis`/`ioredis` → Redis

**Architecture detection** (from directory structure):
- `controller(s)/` + `service(s)/` + `repositor*/` → `layered`
- `models/` + `views/` + `controllers/` → `MVC`
- `domain/` + `ports/` + `adapters/` → `hexagonal`
- `commands/` + `queries/` → `CQRS`
- Multiple independent service directories → `microservices`

**TypeScript detection**: `tsconfig.json` or `typescript` in devDependencies.

#### Source 2 — CLAUDE.md / Agents.md (fallback)

Read "Tech Stack", "Coding Conventions", "Architecture", "Worker" / "Queue" sections.

#### After detection — auto-cache

If at least `lang_be` or `lang_fe` was detected:
- Read `.bs-toolkit.json` (or create it)
- Add/update `stack_profile` with detected values, preserve other keys
- Write back

Display in brief:
```
✓ Stack detected & cached → future runs will use the cache.
```

---

## PHASE 2 — Sprint Intelligence

Scan `*/docs/plan/` in the scoped submodule(s):
1. List files matching `sprint-{N}-*.md`
2. Extract the highest N
3. next = N_max + 1 (no files → next = 1)
4. Remember the 3 most recent sprints for context

If multiple submodules are in scope, show next sprint per submodule.

---

## PHASE 3 — Task Analysis

Only runs if a task description is present in `$ARGUMENTS`.

### 3a. Classify task type
| Type | Keywords |
|------|---------|
| **new-feature** | implement, add, create, build |
| **bug-fix** | fix, bug, broken, not working, error |
| **refactor** | refactor, optimize, clean, restructure |
| **question** | why, how, explain, what is, mechanism |
| **architecture** | design, plan, architecture, approach, strategy |

### 3b. Extract research keywords
Take noun/domain keywords, drop stop words.
Example: "fix video retry not triggering" → `video`, `retry`, `trigger`

---

## PHASE 4 — Resolve Script Path

1. `./scripts/doc_context.py` exists → `SCRIPT_CMD = "python scripts/"`
2. Not found → `SCRIPT_CMD = "python ~/.claude/skills/bs-claude-toolkit/scripts/"`

---

## PHASE 5 — Output Action Brief

```
╔══════════════════════════════════════════════════════════════╗
  PROJECT BRIEF  [scope: all | submodule-name]
╚══════════════════════════════════════════════════════════════╝

  Mode:        [Planning | Execution]
  Scope:       [loaded submodule(s)]
  Stack:       [BE: framework_be/lang_be] · [FE: framework_fe/lang_fe]
               [arch] · async: [async_tech] · db: [database]
  Stack src:   [⚡ cached | 🔍 detected from project files]
  Next Sprint: [N]  (last: sprint-[N-1]-[name])

──────────────────────────────────────────────────────────────
  RESEARCH — run before starting
──────────────────────────────────────────────────────────────

  [SCRIPT_CMD]doc_context.py [keywords]
  [SCRIPT_CMD]doc_context.py --scope [submodule] [keywords]
  [SCRIPT_CMD]code_research.py [keywords]

──────────────────────────────────────────────────────────────
  WORKFLOW  [task-type]
──────────────────────────────────────────────────────────────

  new-feature:
    [Claude — Planning]
    1. Research (doc + code)
    2. Create [submodule]/docs/plan/sprint-[N]-[slug].md

    [Codex — Implementation]
    3. Implement following the plan

    [Claude — Review]
    4. Code review (see CODE REVIEW below)

    [Codex — Documentation]
    5. Create [submodule]/docs/changelog/[YYYYMMDD]-[HHMM]-changelog-[slug].md
    6. Create [submodule]/docs/test/[YYYYMMDD]-[HHMM]-test-[slug].md
    7. Create [submodule]/docs/test/[YYYYMMDD]-[HHMM]-testlog-[slug].md

  bug-fix:
    [Claude — Planning]
    1. Research → trace root cause
    2. Describe fix scope and approach in brief

    [Codex — Implementation]
    3. Fix minimum scope, correct layer

    [Claude — Review]
    4. Code review (see CODE REVIEW below)

    [Codex — Documentation]
    5. Create [submodule]/docs/changelog/[YYYYMMDD]-[HHMM]-changelog-[slug].md

  question / architecture:
    1. Research → analyze → answer  (no files needed)

──────────────────────────────────────────────────────────────
  CODE REVIEW  (after every implement/fix)
──────────────────────────────────────────────────────────────

  ── Universal ──
  [ ] No hardcoded secrets, credentials, or magic numbers
  [ ] Clear, self-documenting names
  [ ] All error paths handled — no silent failures
  [ ] API contract not silently changed → update docs if it is
  [ ] Core application flow not broken

  ── Language: [lang_be] · [lang_fe] ──
  Python     → [ ] No print() · Full type hints · f-strings
  TypeScript → [ ] No `any` · No unsafe `!` · strict mode
  Go         → [ ] Check all errors (no `_`) · No panic() in lib · Context propagation
  Java/Kotlin → [ ] No System.out · Checked exceptions · try-with-resources
  PHP        → [ ] No var_dump() · PSR logging · Declare types
  Ruby       → [ ] No puts/p · Exception handling · frozen_string_literal
  Node/JS    → [ ] No console.log · Proper async/await

  ── Architecture: [arch] ──
  layered     → [ ] No layer skipping · Controller delegates · Service owns logic · Repo = data only
  MVC         → [ ] Thin controller · Fat model · No logic in views
  hexagonal   → [ ] Domain ≠ infra imports · Ports = interfaces · Adapters implement ports
  microservices → [ ] No cross-service DB calls · Communicate via API/events
  CQRS        → [ ] Commands ≠ Queries · Read/write models independent

  ── Async/Queue: [async_tech] ──  (skip if none)
  [ ] Idempotency key · max_retries + exponential backoff · Dead-letter handling
  [ ] Status: pending → running → done/failed
  [ ] FE: loading/error states · Polling race conditions · Cleanup on unmount

──────────────────────────────────────────────────────────────
  FILE NAMING  (today: [YYYYMMDD], now: [HHMM])
──────────────────────────────────────────────────────────────

  Plan:      [submodule]/docs/plan/sprint-[N]-[slug].md
  Changelog: [submodule]/docs/changelog/[YYYYMMDD]-[HHMM]-changelog-[slug].md
  Test doc:  [submodule]/docs/test/[YYYYMMDD]-[HHMM]-test-[slug].md
  Test log:  [submodule]/docs/test/[YYYYMMDD]-[HHMM]-testlog-[slug].md

  [HHMM] = current local time when creating the file (24h, e.g. 1430)
  Time in the filename makes ordering self-evident and prevents merge conflicts.

──────────────────────────────────────────────────────────────
  DEFINITION OF DONE
──────────────────────────────────────────────────────────────

  [ ] Code runs locally
  [ ] Tests pass: happy + edge + failure cases
  [ ] Changelog created (by Codex)
  [ ] Test doc + test log created (by Codex)
  [ ] Core flow not broken
  [ ] API contract not silently changed
  [ ] No language rule violations · No hardcoded secrets

══════════════════════════════════════════════════════════════
```

---

## PHASE 6 — Proactive Warnings

- **Missing `.bs-toolkit.json`** → auto-created with `stack_profile` after first detection
- **`stack_profile` may be stale** → "💡 Stack changed recently? Run `install.py --setup-stack` to refresh."
- **Task touches `shared_files`** → "⚠️ This file is shared — coordinate with teammates before editing."
- **Task touches API contract** → "⚠️ API contract change — update docs and notify all consumers."
- **Missing `docs/plan/`** in submodule → "⚠️ Create docs/plan/ before writing a sprint plan."
- **Task looks like Execution but no explicit request** → confirm with user before writing code.

---

## Notes

- After printing the brief → **stop and wait for the user** — do not start implementing
- Use the actual system date for `[YYYYMMDD]`
- `.bs-toolkit.json` should be committed; it's shared config for the whole team
