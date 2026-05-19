---
description: Load project context, detect task type, compute next sprint number, suggest research commands, and output a full action brief before starting any task.
arguments: [scope | task-description]
---

Đây là skill khởi động toàn diện. Thực hiện tuần tự các phase sau.

---

## PHASE 1 — Load Context

### 1a. Root context (luôn luôn)
- Read `./CLAUDE.md`
- Read `./Agents.md` nếu tồn tại

### 1b. Phát hiện submodule
Scan tất cả immediate subdirectories. Một subdir là **submodule** nếu chứa ít nhất một trong: `CLAUDE.md`, `Agents.md`, `docs/`.

Không phụ thuộc tên — hoạt động với: `backend/`, `frontend/`, `myapp-be/`, `myapp-fe/`, `api/`, `web/`, v.v.

### 1c. Xử lý `$ARGUMENTS`
Nếu `$ARGUMENTS` không trống:
- Nếu là 1–2 từ ngắn khớp tên submodule → dùng làm **scope filter** (chỉ load submodule khớp)
- Ngược lại → dùng làm **task description** để phân tích ở Phase 3
- Cả hai không loại trừ nhau: "be video retry" → scope=be, task="video retry"

### 1d. Load submodule context
Với mỗi submodule (đã filter nếu có scope):
- Read `{subdir}/CLAUDE.md`
- Read `{subdir}/Agents.md` nếu tồn tại

### 1e. Extract thông tin từ CLAUDE.md đã đọc
Ghi nhớ (không cần in ra lúc này):
- **Execution mode** mặc định (Planning / Execution)
- **Tech stack** của từng submodule (ngôn ngữ, framework chính)
- **Coding conventions** cốt lõi (naming, layer structure)
- **Flow chính** không được phá vỡ
- **API contract format** nếu có
- **DB/secrets restrictions**

---

## PHASE 2 — Sprint Intelligence

Scan tất cả `*/docs/plan/` directories tìm được:

1. Liệt kê tất cả files khớp pattern `sprint-{N}-*.md`
2. Tìm **N_max** = số sprint lớn nhất hiện có
3. **Next sprint = N_max + 1**
4. Ghi nhớ tên 3 sprint gần nhất để có context

Nếu không có sprint nào → next sprint = 1.

---

## PHASE 3 — Task Analysis

Chỉ thực hiện nếu có task description từ `$ARGUMENTS` hoặc từ message của user.

### 3a. Phân loại task
Xác định loại task:

| Loại | Dấu hiệu |
|------|---------|
| **new-feature** | "implement", "add", "create", "build", "tạo", "thêm" |
| **bug-fix** | "fix", "bug", "lỗi", "sửa", "broken", "không hoạt động" |
| **refactor** | "refactor", "optimize", "clean", "tái cấu trúc" |
| **question** | "tại sao", "how", "explain", "giải thích", "cơ chế" |
| **architecture** | "design", "plan", "kiến trúc", "approach", "strategy" |

### 3b. Trích xuất keywords
Từ task description, trích các **noun/domain keywords** quan trọng nhất (bỏ stop words).

Ví dụ: "implement video generation retry with backoff" → `video`, `generation`, `retry`, `backoff`

### 3c. Xác định scope cho research
Nếu task rõ ràng thuộc FE hoặc BE → đề xuất `--scope` tương ứng.
Nếu cả hai → không dùng `--scope`.

---

## PHASE 4 — Resolve Script Path

Kiểm tra theo thứ tự:
1. `./scripts/doc_context.py` tồn tại trong CWD → dùng `python scripts/`
2. Không có → dùng từ toolkit: `python ~/.claude/skills/bs-claude-toolkit/scripts/`

Ghi nhớ `SCRIPT_CMD` = prefix đúng để dùng ở Phase 5.

---

## PHASE 5 — Output Action Brief

In ra một brief có cấu trúc sau. Ngắn gọn, scannable, không thêm gì không cần thiết.

```
╔══════════════════════════════════════════════════════════════╗
  PROJECT BRIEF
╚══════════════════════════════════════════════════════════════╝

  Mode:        [Planning | Execution]
  Submodules:  [danh sách tên submodule đã load]
  Stack:       [BE: framework/lang] · [FE: framework/lang]
  Next Sprint: [N]  (last: sprint-[N-1]-[tên])

──────────────────────────────────────────────────────────────
  RESEARCH — chạy trước khi bắt đầu
──────────────────────────────────────────────────────────────

  [SCRIPT_CMD]doc_context.py [keywords]
  [SCRIPT_CMD]doc_context.py --scope [submodule] [keywords]
  [SCRIPT_CMD]code_research.py [keywords]

  (Thay [keywords] bằng domain keywords của task)

──────────────────────────────────────────────────────────────
  WORKFLOW — [task-type: new-feature | bug-fix | refactor | ...]
──────────────────────────────────────────────────────────────

  [Hiển thị đúng luồng theo task type:]

  new-feature:
    1. Research (doc + code)
    2. Tạo docs/plan/sprint-[N]-[slug].md
    3. Implement theo plan
    4. Tạo docs/changelog/[DATE]-changelog-1-[slug].md
    5. Tạo docs/test/[DATE]-test-1-[slug].md

  bug-fix:
    1. Research → trace root cause
    2. Fix minimum scope, đúng layer
    3. Tạo docs/changelog/[DATE]-changelog-1-[slug].md
    (không cần plan file)

  question / architecture:
    1. Research scripts
    2. Phân tích → trả lời / đề xuất
    (không cần changelog)

──────────────────────────────────────────────────────────────
  FILE NAMING (today: [YYYYMMDD])
──────────────────────────────────────────────────────────────

  Plan:      sprint-[N]-[slug].md
  Changelog: [YYYYMMDD]-changelog-[seq]-[slug].md
  Test:      [YYYYMMDD]-test-[seq]-[slug].md

  [seq] = số thứ tự file trong ngày hôm nay. Đọc thư mục trước!

──────────────────────────────────────────────────────────────
  DEFINITION OF DONE
──────────────────────────────────────────────────────────────

  [ ] Code chạy được local
  [ ] Test pass: happy + edge + failure case
  [ ] Changelog file tạo xong
  [ ] Flow chính không bị phá
  [ ] API contract không thay đổi ngầm
  [ ] Không any (TS) · không print() (BE) · không hardcode secrets

══════════════════════════════════════════════════════════════
```

---

## PHASE 6 — Proactive Warnings

Sau brief, kiểm tra và cảnh báo nếu phát hiện:

- **Chưa có CLAUDE.md** trong submodule → "⚠️ {subdir}/ thiếu CLAUDE.md — conventions chưa được định nghĩa"
- **Không tìm thấy docs/plan/** → "⚠️ Chưa có docs/plan/ — sprint tracking chưa được setup"
- **Task là Execution nhưng mode mặc định là Planning** → nhắc user xác nhận muốn switch mode
- **Từ khóa task liên quan đến DB/secrets/production** → nhắc luật không kết nối DB thật

---

## Notes

- Luôn dùng ngày thực tế từ system date cho `[YYYYMMDD]` trong file naming
- Nếu không đọc được 1 file → bỏ qua, không dừng
- Brief phải in đầy đủ dù không có `$ARGUMENTS`
- Sau khi in brief → dừng, chờ user chỉ định task cụ thể (không tự bắt đầu implement)
