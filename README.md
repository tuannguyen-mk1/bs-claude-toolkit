# bs-claude-toolkit

Standardized AI coding workflow skill for Claude Code.
Auto-loads project context, detects stack, enforces workflow, generates review checklists.

> 🇻🇳 [Đọc bằng tiếng Việt](README.vi.md)

---

## Setup (one-time per machine)

### Step 1 — Clone the toolkit

```bash
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/bs-claude-toolkit
```

Claude Code auto-discovers the skill. Use `/bs-claude-toolkit` from any project.

---

### Step 2 — Install into your project

Run from your project root:

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py
```

This creates:
- `CLAUDE.md` — project context template
- `.bs-toolkit.json` — team config

---

### Step 3 — Fill in your Tech Stack

Open `CLAUDE.md` and fill in the **Tech Stack** table:

```markdown
| Backend language  | Python          |
| Backend framework | FastAPI         |
| Frontend language | TypeScript      |
| Frontend framework| Next.js         |
| Architecture      | layered         |
| Async / Queue     | Celery          |
| Database          | PostgreSQL      |
```

Also replace `[BE_DIR]` and `[FE_DIR]` with your actual directory names.

---

### Step 4 — Cache the stack profile

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --setup-stack
```

This saves the stack into `.bs-toolkit.json` so the skill doesn't re-read `CLAUDE.md` on every run (~90% token savings).

---

## Usage

```
/bs-claude-toolkit                    ← load full context + action brief
/bs-claude-toolkit be                 ← focus on backend only
/bs-claude-toolkit fe                 ← focus on frontend only
/bs-claude-toolkit fix login bug      ← context + task classification
```

---

## Split team (2 developers)

```bash
# Project lead — run once, commit .bs-toolkit.json
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py \
  --mode split --modules be:myapp-be,fe:myapp-fe

# Each developer — set personal scope (not committed)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope be
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope fe
```

---

## Other tools (optional)

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool cursor
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool windsurf
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --lang vi   # Vietnamese templates
```

---

## Requirements

- Python 3.8+ (stdlib only)
- Claude Code CLI
