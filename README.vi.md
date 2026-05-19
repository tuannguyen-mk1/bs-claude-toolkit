# bs-claude-toolkit

Bộ công cụ workflow AI coding chuẩn hóa cho dự án fullstack.
Hỗ trợ **Claude Code · Cursor · Codex · Windsurf**.

> 🇬🇧 [Read in English](README.md)

---

## Mục lục

- [Cài đặt nhanh](#cài-đặt-nhanh)
- [Hỗ trợ công cụ](#hỗ-trợ-công-cụ)
- [Solo vs Split Team](#solo-vs-split-team)
- [Scripts tra cứu](#scripts-tra-cứu)
- [Cài đặt đầy đủ cho máy mới](#cài-đặt-đầy-đủ-cho-máy-mới)
- [Cấu trúc repo](#cấu-trúc-repo)
- [Quy ước đặt tên](#quy-ước-đặt-tên)
- [Yêu cầu](#yêu-cầu)

---

## Cài đặt nhanh

### Bước 1 — Clone toolkit (một lần mỗi máy)

```bash
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/bs-claude-toolkit
```

> Claude Code tự nhận diện `/bs-claude-toolkit` sau khi clone — không cần cấu hình thêm.

Muốn dùng tên lệnh ngắn hơn:
```bash
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/ctx
# → dùng /ctx thay thế
```

### Bước 2 — Cài vào project (chạy từ thư mục gốc project)

```bash
# Tất cả tools
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py

# Chỉ cài tool cụ thể
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool cursor
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool windsurf
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool scripts

# Chọn ngôn ngữ tài liệu (mặc định: en)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --lang vi
```

---

## Hỗ trợ công cụ

### Claude Code

| | |
|-|-|
| Cài đặt | Clone vào `~/.claude/skills/bs-claude-toolkit/` |
| Gọi | `/bs-claude-toolkit` trong chat |
| Lọc scope | `/bs-claude-toolkit be` · `/bs-claude-toolkit fe` |
| Mô tả task | `/bs-claude-toolkit fix video retry bug` |

Skill tự phát hiện submodule theo nội dung (có `CLAUDE.md` / `Agents.md` / `docs/`), không phụ thuộc tên thư mục.

---

### Codex (OpenAI)

| Phạm vi | File | Cách cài |
|---------|------|----------|
| Global | `~/.codex/AGENTS.md` | `install.py --tool codex --global` |
| Per-project | `[project]/AGENTS.md` | `install.py --tool codex` |
| Per-submodule | `[subdir]/AGENTS.md` | Copy thủ công |

Codex đọc theo thứ tự: `~/.codex/AGENTS.md` → root `AGENTS.md` → subdirectory `AGENTS.md`.

```bash
# Cài global (áp dụng cho mọi project trên máy này)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex --global
```

---

### Cursor

| Phạm vi | File | Cách cài |
|---------|------|----------|
| Per-project | `.cursor/rules/bs-claude-toolkit.mdc` | `install.py --tool cursor` |
| Global | Settings UI → Rules | Paste nội dung từ `adapters/cursor.mdc` |

Rule dùng `alwaysApply: true` — tự động áp dụng cho mọi session trong project.

---

### Windsurf

| Phạm vi | File | Cách cài |
|---------|------|----------|
| Per-project | `.windsurf/rules/bs-claude-toolkit.md` | `install.py --tool windsurf` |

---

## Solo vs Split Team

### Solo — một developer code cả BE + FE

```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --mode solo
```

`/bs-claude-toolkit` load toàn bộ context; số sprint dùng chung cho cả project.

---

### Split — hai developer làm việc độc lập

```bash
# Project lead chạy một lần, commit .bs-toolkit.json
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py \
  --mode split --modules be:myapp-be,fe:myapp-fe
```

**Mỗi developer** sau đó set personal scope (không commit vào git):

```bash
# Dev BE
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope be

# Dev FE
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --scope fe
```

Sau bước này, `/bs-claude-toolkit` tự load đúng scope — không cần truyền argument.

#### Phòng tránh conflict trong split mode

| Zone | Files | Quy tắc |
|------|-------|---------|
| ✏️ **Zone của bạn** | `{module}/` code + `{module}/docs/` | Tự do sửa |
| 🤝 **Shared zone** | `CLAUDE.md`, `docs/api-contract.md` | Sync với team trước |

- Số sprint **độc lập theo submodule** — BE đang sprint-15, FE đang sprint-12 là bình thường
- Changelog/test file nằm trong `{module}/docs/` — không conflict
- Thay đổi API contract cần cả hai bên đồng thuận

#### Khi chưa set `default_scope`

Skill sẽ hỏi:
```
⚠️  Split team mode detected. Bạn đang làm việc ở module nào?
    /bs-claude-toolkit be
    /bs-claude-toolkit fe
    /bs-claude-toolkit all   ← fullstack session

Tip: Tạo .bs-toolkit.local.json với {"default_scope": "be"} để không cần gõ mỗi lần.
```

---

## Scripts tra cứu

Chạy trực tiếp từ toolkit (không cần copy vào project):

```bash
# Tìm trong plan, changelog, test đã có
python ~/.claude/skills/bs-claude-toolkit/scripts/doc_context.py <keyword>
python ~/.claude/skills/bs-claude-toolkit/scripts/doc_context.py --scope be <keyword>
python ~/.claude/skills/bs-claude-toolkit/scripts/doc_context.py --scope fe <keyword>

# Tìm trong code
python ~/.claude/skills/bs-claude-toolkit/scripts/code_research.py <keyword>
python ~/.claude/skills/bs-claude-toolkit/scripts/code_research.py --scope be <keyword>
```

Scripts dùng `CWD` để tìm project root — hoạt động từ bất kỳ thư mục con nào.

Copy scripts vào project (cho đồng đội chưa cài toolkit):
```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool scripts
```

---

## Cài đặt đầy đủ cho máy mới

```bash
# 1. Clone một lần
git clone https://github.com/tuannguyen-mk1/bs-claude-toolkit.git ~/.claude/skills/bs-claude-toolkit

# 2. Tùy chọn: Codex global (áp dụng cho mọi project)
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py --tool codex --global

# 3. Cho mỗi project mới (chạy từ thư mục gốc project)
cd /path/to/your-project
python ~/.claude/skills/bs-claude-toolkit/scripts/install.py
```

Cập nhật per-project files sau khi toolkit có phiên bản mới:
```bash
cd ~/.claude/skills/bs-claude-toolkit && git pull
# sau đó chạy lại install.py trong từng project
```

---

## Cấu trúc repo

```
bs-claude-toolkit/
├── SKILL.md                           ← Claude Code global skill
├── adapters/
│   ├── cursor.mdc                     ← Cursor rule (EN, alwaysApply)
│   ├── cursor.vi.mdc                  ← Cursor rule (VI)
│   ├── windsurf.md                    ← Windsurf rule (EN)
│   └── windsurf.vi.md                 ← Windsurf rule (VI)
├── scripts/
│   ├── doc_context.py                 ← Tìm docs (auto-detect, --scope)
│   ├── code_research.py               ← Tìm code (auto-detect, --scope)
│   └── install.py                     ← Installer (--tool, --mode, --lang)
└── templates/
    ├── CLAUDE.md                      ← Template cho Claude Code (EN)
    ├── CLAUDE.vi.md                   ← Template cho Claude Code (VI)
    ├── AGENTS.md                      ← Template cho Codex (EN)
    ├── AGENTS.vi.md                   ← Template cho Codex (VI)
    ├── .bs-toolkit.json               ← Config template solo
    ├── .bs-toolkit.split.json         ← Config template split team
    └── .bs-toolkit.local.json.example ← Ví dụ personal scope
```

---

## Quy ước đặt tên

Toolkit phát hiện submodule theo **nội dung** (có `CLAUDE.md` / `Agents.md` / `docs/`), không theo tên thư mục.

| Quy ước | Thư mục BE | Thư mục FE |
|---------|-----------|-----------|
| Chuẩn | `backend/` | `frontend/` |
| Theo tên project | `myapp-be/` | `myapp-fe/` |
| Ngắn | `be/` | `fe/` |
| Theo role | `api/` | `web/` |
| Theo role | `server/` | `client/` |

`--scope` dùng partial case-insensitive matching: `--scope be` khớp với `backend`, `myapp-be`, `be`, `server`.

---

## Yêu cầu

- Python 3.8+ (chỉ dùng stdlib — không cần cài thêm package)
- Claude Code CLI (để dùng `/bs-claude-toolkit`)
