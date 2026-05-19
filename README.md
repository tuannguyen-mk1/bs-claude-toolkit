# bs-claude-toolkit

Standardized AI coding workflow toolkit for fullstack projects.
Supports **Claude Code · Cursor · Codex · Windsurf**.

> 🇻🇳 [Đọc bằng tiếng Việt](README.vi.md)

---

## Table of Contents

- [Quick Install](#quick-install)
- [Tool Support](#tool-support)
- [Solo vs Split Team](#solo-vs-split-team)
- [Research Scripts](#research-scripts)
- [Full Setup for a New Machine](#full-setup-for-a-new-machine)
- [Repo Structure](#repo-structure)
- [Naming Conventions](#naming-conventions)
- [Requirements](#requirements)

---

## Quick Install

### Step 1 — Clone toolkit (once per machine)

```bash
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/bs-claude-toolkit
```

> Claude Code automatically recognizes `/bs-claude-toolkit` after cloning — no extra steps needed.

Prefer a shorter command name:
```bash
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/ctx
# → use /ctx instead
```

### Step 2 — Install into project (run from project root)

```bash
# All tools
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py

# Specific tool only
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool cursor
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool windsurf
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool scripts

# Choose doc language (default: en)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --lang vi
```

---

## Tool Support

### Claude Code

| | |
|-|-|
| Install | Clone to `~/.claude/skills/bs-claude-toolkit/` |
| Invoke | `/bs-claude-toolkit` in chat |
| Scope filter | `/bs-claude-toolkit be` · `/bs-claude-toolkit fe` |
| Task briefing | `/bs-claude-toolkit fix video retry bug` |

The skill auto-detects submodules by content (presence of `CLAUDE.md` / `Agents.md` / `docs/`), regardless of directory name.

---

### Codex (OpenAI)

| Scope | File | How to install |
|-------|------|----------------|
| Global | `~/.codex/AGENTS.md` | `install.py --tool codex --global` |
| Per-project | `[project]/AGENTS.md` | `install.py --tool codex` |
| Per-submodule | `[subdir]/AGENTS.md` | Copy manually |

Codex reads in order: `~/.codex/AGENTS.md` → root `AGENTS.md` → subdirectory `AGENTS.md`.

```bash
# Install global (applies to all projects on this machine)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex --global
```

---

### Cursor

| Scope | File | How to install |
|-------|------|----------------|
| Per-project | `.cursor/rules/bs-claude-toolkit.mdc` | `install.py --tool cursor` |
| Global | Settings UI → Rules | Paste content from `adapters/cursor.mdc` |

Rule uses `alwaysApply: true` — automatically applies to every session in the project.

---

### Windsurf

| Scope | File | How to install |
|-------|------|----------------|
| Per-project | `.windsurf/rules/bs-claude-toolkit.md` | `install.py --tool windsurf` |

---

## Solo vs Split Team

### Solo — one developer for both BE + FE

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --mode solo
```

`/bs-claude-toolkit` loads all context; sprint numbers are shared across the project.

---

### Split — two developers working independently

```bash
# Project lead runs once, commits .bs-toolkit.json
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py \
  --mode split --modules be:myapp-be,fe:myapp-fe
```

**Each developer** then sets their personal scope (not committed to git):

```bash
# BE developer
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope be

# FE developer
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope fe
```

After this, `/bs-claude-toolkit` automatically loads the correct scope — no arguments needed.

#### Conflict prevention in split mode

| Zone | Files | Rule |
|------|-------|------|
| ✏️ **Your zone** | `{module}/` code + `{module}/docs/` | Edit freely |
| 🤝 **Shared zone** | `CLAUDE.md`, `docs/api-contract.md` | Sync with team first |

- Sprint numbers are **independent per submodule** — BE on sprint-15, FE on sprint-12 is normal
- Changelog/test files live in `{module}/docs/` — no conflicts
- API contract changes require both sides to agree

#### When no `default_scope` is set

The skill will prompt:
```
⚠️  Split team mode detected. Which module are you working on?
    /bs-claude-toolkit be
    /bs-claude-toolkit fe
    /bs-claude-toolkit all   ← fullstack session

Tip: Create .bs-toolkit.local.json with {"default_scope": "be"} to skip this prompt.
```

---

## Research Scripts

Run directly from the toolkit (no need to copy into project):

```bash
# Search past plans, changelogs, tests
python ~/.claude/skills/bs-claude-toolkit/scripts/doc_context.py <keyword>
python ~/.claude/skills/bs-claude-toolkit/scripts/doc_context.py --scope be <keyword>
python ~/.claude/skills/bs-claude-toolkit/scripts/doc_context.py --scope fe <keyword>

# Search code
python ~/.claude/skills/bs-claude-toolkit/scripts/code_research.py <keyword>
python ~/.claude/skills/bs-claude-toolkit/scripts/code_research.py --scope be <keyword>
```

Scripts use `CWD` to find the project root — works from any subdirectory.

Copy scripts into the project (for teammates without the toolkit):
```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool scripts
```

---

## Full Setup for a New Machine

```bash
# 1. Clone once
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/bs-claude-toolkit

# 2. Optional: Codex global (applies to all projects)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex --global

# 3. For each new project (run from project root)
cd /path/to/your-project
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py
```

Update per-project files after toolkit updates:
```bash
cd ~/.claude/skills/bs-claude-toolkit && git pull
# then re-run install.py in each project
```

---

## Repo Structure

```
bs-claude-toolkit/
├── SKILL.md                           ← Claude Code global skill
├── adapters/
│   ├── cursor.mdc                     ← Cursor rule (EN, alwaysApply)
│   ├── cursor.vi.mdc                  ← Cursor rule (VI)
│   ├── windsurf.md                    ← Windsurf rule (EN)
│   └── windsurf.vi.md                 ← Windsurf rule (VI)
├── scripts/
│   ├── doc_context.py                 ← Search docs (auto-detect, --scope)
│   ├── code_research.py               ← Search code (auto-detect, --scope)
│   └── install.py                     ← Installer (--tool, --mode, --lang)
└── templates/
    ├── CLAUDE.md                      ← Claude Code project template (EN)
    ├── CLAUDE.vi.md                   ← Claude Code project template (VI)
    ├── AGENTS.md                      ← Codex project template (EN)
    ├── AGENTS.vi.md                   ← Codex project template (VI)
    ├── .bs-toolkit.json               ← Solo config template
    ├── .bs-toolkit.split.json         ← Split team config template
    └── .bs-toolkit.local.json.example ← Personal scope example
```

---

## Naming Conventions

The toolkit detects submodules by **content** (has `CLAUDE.md` / `Agents.md` / `docs/`), not by name.

| Convention | BE dir | FE dir |
|------------|--------|--------|
| Standard | `backend/` | `frontend/` |
| Project-named | `myapp-be/` | `myapp-fe/` |
| Short | `be/` | `fe/` |
| By role | `api/` | `web/` |
| By role | `server/` | `client/` |

`--scope` does partial case-insensitive matching: `--scope be` matches `backend`, `myapp-be`, `be`, `server`.

---

## Requirements

- Python 3.8+ (stdlib only — no extra packages)
- Claude Code CLI (for `/bs-claude-toolkit`)
