# bs-claude-toolkit

Skill workflow AI coding chuẩn hóa cho Claude Code.
Tự động load context, detect stack, enforce workflow, sinh review checklist.

> 🇬🇧 [Read in English](README.md)

---

## Cài đặt (một lần mỗi máy)

### Bước 1 — Clone toolkit

```bash
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/bs-claude-toolkit
```

Claude Code tự nhận diện skill. Dùng `/bs-claude-toolkit` từ bất kỳ project nào.

---

### Bước 2 — Cài vào project

Chạy từ thư mục gốc project:

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py
```

Tạo ra:
- `CLAUDE.md` — template context cho project
- `.bs-toolkit.json` — config team

---

### Bước 3 — Điền Tech Stack

Mở `CLAUDE.md` và điền bảng **Tech Stack**:

```markdown
| Backend language  | Python          |
| Backend framework | FastAPI         |
| Frontend language | TypeScript      |
| Frontend framework| Next.js         |
| Architecture      | layered         |
| Async / Queue     | Celery          |
| Database          | PostgreSQL      |
```

Đồng thời thay `[BE_DIR]` và `[FE_DIR]` bằng tên thư mục thực tế.

---

### Bước 4 — Cache stack profile

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --setup-stack
```

Lưu stack vào `.bs-toolkit.json` để skill không cần đọc lại `CLAUDE.md` mỗi lần chạy (~90% tiết kiệm token).

---

## Sử dụng

```
/bs-claude-toolkit                    ← load full context + action brief
/bs-claude-toolkit be                 ← chỉ tập trung backend
/bs-claude-toolkit fe                 ← chỉ tập trung frontend
/bs-claude-toolkit fix login bug      ← context + phân loại task
```

---

## Split team (2 developers)

```bash
# Project lead — chạy 1 lần, commit .bs-toolkit.json
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py \
  --mode split --modules be:myapp-be,fe:myapp-fe

# Mỗi developer — set personal scope (không commit)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope be
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope fe
```

---

## Các tool khác (tuỳ chọn)

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool cursor
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool windsurf
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --lang vi   # template tiếng Việt
```

---

## Yêu cầu

- Python 3.8+ (stdlib only)
- Claude Code CLI
