# Simple Claude

Bộ khung cấu hình **Claude Code** cho dự án cá nhân/nhóm, tập trung vào:

- Hệ thống **hooks** đầy đủ (âm thanh thông báo theo event)
- Bộ **skills** phục vụ tra cứu tài liệu/web/code mẫu
- Agent `search-agent` để tách ngữ cảnh khi tìm kiếm
- Quy tắc dùng `Context7 (ctx7)` khi hỏi về thư viện/framework/API

## Tính năng chính

- Cấu hình quyền và hooks trong `.claude/settings.json`
- Script hook trung tâm: `.claude/hooks/scripts/hooks.py`
- Bật/tắt từng hook qua `.claude/hooks/config/hooks-config.json`
- Skills có sẵn:
  - `find-docs` (Context7)
  - `web-search-exa`
  - `web-fetch-exa`
  - `search-git-hub`
- Wrapper script cho skill tại:
  - `.claude/skills/*/scripts/callmcp.py`
- Status line tùy biến: `.claude/statusline.sh`

## Cấu trúc thư mục

```text
.claude/
  agents/
    search-agent.md
  hooks/
    HOOKS-README.md
    config/
      hooks-config.json
    scripts/
      hooks.py
    sounds/
      ... (âm thanh theo từng hook event)
  rules/
    context7.md
  skills/
    find-docs/
      SKILL.md
    web-search/
      SKILL.md
      scripts/callmcp.py
    web-fetch/
      SKILL.md
      scripts/callmcp.py
    search-git-hub/
      SKILL.md
      scripts/callmcp.py
```

## Yêu cầu môi trường

- Claude Code CLI
- Python 3
- `mcp2cli` (được các script skill sử dụng)
- `jq` (dùng trong status line)
- (Tuỳ chọn) công cụ phát âm thanh theo OS:
  - macOS: `afplay` (có sẵn)
  - Linux: `paplay`/`aplay`/`ffplay`/`mpg123`
  - Windows: `winsound`

## Thiết lập nhanh

1. Clone repo vào máy.
2. Đảm bảo các file trong `.claude/` được Claude Code đọc trong project.
3. Kiểm tra Python:

```bash
python3 --version
```

4. Cấu hình API key (nếu dùng Exa):

```bash
export EXA_API_KEY=your_key
```

Hoặc đặt trong file `.env` ở thư mục script skill theo logic nạp trong `callmcp.py`.

## Cách dùng

### 1) Hooks

- Cấu hình event hooks: `.claude/settings.json`
- Bật/tắt chi tiết: `.claude/hooks/config/hooks-config.json`
- Tài liệu chi tiết: `.claude/hooks/HOOKS-README.md`

### 2) Skills

- Mỗi skill có mô tả và workflow riêng trong `SKILL.md`.
- Skill tra cứu docs dùng `ctx7` theo rule tại `.claude/rules/context7.md`.

### 3) Agent tìm kiếm

- `search-agent` được dùng để cô lập tác vụ tìm kiếm/tra cứu, giúp giảm nhiễu ngữ cảnh chính.

## Ghi chú

- Repo này thiên về **cấu hình Claude Code** hơn là ứng dụng runtime truyền thống.
- Nếu bạn chỉnh hooks/rules/skills, nên rà soát lại quyền trong `.claude/settings.json` để tránh xung đột.
