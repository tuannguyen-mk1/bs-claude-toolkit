# bs-claude-toolkit — Quy tắc Workflow AI Coding

## Load Context

Trước khi bắt đầu bất kỳ task nào, đọc các file theo thứ tự:
1. `CLAUDE.md` ở thư mục gốc (luôn luôn)
2. `CLAUDE.md` và `Agents.md` bên trong các thư mục con trực tiếp có chứa `docs/` hoặc `CLAUDE.md` riêng — hoạt động với mọi quy ước đặt tên (`backend/`, `myapp-be/`, `api/`, `web/`, v.v.)

## Research trước khi implement

Chạy scripts này trước khi fix bug hoặc implement tính năng:

```bash
python scripts/doc_context.py <keyword>
python scripts/doc_context.py --scope <submodule-name> <keyword>
python scripts/code_research.py <keyword>
python scripts/code_research.py --scope <submodule-name> <keyword>
```

Nếu scripts chưa có local, dùng toolkit path:
```bash
python ~/.claude/skills/bs-claude-toolkit/scripts/doc_context.py <keyword>
```

## Execution Mode

- **Planning (mặc định):** Không có yêu cầu code rõ → phân tích, tài liệu `.md`, đề xuất kiến trúc
- **Execution:** Chỉ khi được yêu cầu rõ ràng → viết code, fix bug, refactor, test

## Workflow

**Tính năng mới:** research → `docs/plan/sprint-{N}-{slug}.md` → implement → changelog → test doc

**Fix bug:** research → trace root cause → fix tối thiểu → changelog (không cần plan file)

## Quy tắc bắt buộc

- Tài liệu bằng tiếng Việt có dấu (UTF-8), code dùng tiếng Anh
- Không kết nối DB thật (production/staging)
- Không hardcode secrets · Không `any` type (TS) · Không `print()` (Python)
- Thay đổi API contract phải cập nhật docs ngay lập tức
