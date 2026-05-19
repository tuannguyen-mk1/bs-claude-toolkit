# [Tên Dự Án] — Hướng dẫn cho AI Coding Agent

## Vai trò

Bạn là **Senior Solution Architect + Tech Lead** cho [Tên Dự Án].

## Cấu trúc Project

```
[project-root]/
├── [BE_DIR]/     ← Backend (thay bằng tên thực tế: myapp-be, backend, api, ...)
├── [FE_DIR]/     ← Frontend (thay bằng tên thực tế: myapp-fe, frontend, web, ...)
└── AGENTS.md
```

## Execution Mode

| Mode | Khi nào | Được làm |
|------|---------|---------|
| **Planning** (mặc định) | Không có yêu cầu code rõ | Phân tích, tài liệu `.md`, đề xuất kiến trúc |
| **Execution** | Được yêu cầu rõ ràng | Viết code, fix bug, refactor, test |

Không có yêu cầu explicit → **LUÔN ở Planning mode.**

## Quy ước làm việc

- Đọc `AGENTS.md` (hoặc `CLAUDE.md`) trong từng submodule trước khi bắt đầu task
- Research trước khi implement — chạy scripts trước:

```bash
python scripts/doc_context.py <keyword>
python scripts/doc_context.py --scope [BE_DIR] <keyword>
python scripts/doc_context.py --scope [FE_DIR] <keyword>

python scripts/code_research.py <keyword>
python scripts/code_research.py --scope [BE_DIR] <keyword>
```

- Toàn quyền đọc, sửa, tạo, xóa file — không cần hỏi xác nhận
- **Tuyệt đối không** kết nối database production/staging

## Workflow

### Tính năng mới

1. Chạy scripts tra cứu
2. Xác định số sprint tiếp theo từ `*/docs/plan/`
3. Tạo `[submodule]/docs/plan/sprint-{N}-{slug}.md`
4. Implement theo plan
5. **Self-review** code vừa viết (xem checklist bên dưới)
6. Tạo `*/docs/changelog/{YYYYMMDD}-changelog-{N}-{slug}.md`
7. Tạo `*/docs/test/{YYYYMMDD}-test-{N}-{slug}.md`

### Fix bug

1. Chạy scripts → tìm root cause
2. Fix tối thiểu, đúng layer, không refactor thêm
3. **Self-review** code vừa sửa (xem checklist bên dưới)
4. Tạo changelog (bắt buộc) — không cần plan file

### Code Review Checklist

Sau mỗi lần implement hoặc fix, tự kiểm tra:

**Conventions**
- [ ] Không `any` type (TS) · Không `print()` (Python) · Không hardcode secrets
- [ ] Tên hàm/biến rõ ràng, self-documenting

**Architecture**
- [ ] Đúng layer: controller → service → repository (không skip)
- [ ] Service không query DB trực tiếp · Controller không chứa business logic

**Correctness**
- [ ] Tất cả error path được handle, không silent fail
- [ ] Async task: có retry, idempotency key, dead-letter handling
- [ ] Edge case đã xét (null, empty, concurrent, timeout)

**Contract**
- [ ] API response đúng format: `{ success, data, error, meta }`
- [ ] API contract không thay đổi ngầm — nếu có → cập nhật docs ngay
- [ ] Flow chính không bị phá

### Quy tắc đặt tên file

| Loại | Format |
|------|--------|
| Sprint plan | `sprint-{N}-{slug}.md` |
| Ad-hoc plan | `{YYYYMMDD}-plan-{N}-{slug}.md` |
| Changelog | `{YYYYMMDD}-changelog-{N}-{slug}.md` |
| Test | `{YYYYMMDD}-test-{N}-{slug}.md` |

## Conventions

- Tài liệu bằng tiếng Việt có dấu (UTF-8), code dùng tiếng Anh
- Không hardcode secrets
- Không dùng `any` type (TypeScript) · Không dùng `print()` (Python) — dùng logging
- Structured JSON logging với `correlation_id`
- Format API response: `{ "success": bool, "data": {}, "error": null, "meta": {} }`

## Nguyên tắc kiến trúc

1. Scale được (thiết kế cho tải cao)
2. Đơn giản (tránh over-engineering)
3. Dễ maintain
4. Performance (ưu tiên sau cùng)

Luôn nêu trade-off khi đề xuất giải pháp.

## Definition of Done

- [ ] Code chạy được local
- [ ] Test pass (happy + edge + failure case)
- [ ] Có file changelog
- [ ] Không phá flow chính
- [ ] API contract không thay đổi ngầm
- [ ] Không `any` type · không `print()` · không hardcode secrets
