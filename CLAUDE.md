## Workflow Rules
- For non-trivial work (3+ steps, multi-file edits, or anything needing progress tracking), always use `TaskCreate` + `TaskUpdate`.
- For simple one-step edits, execute directly without creating unnecessary tasks.
- Do not commit or push unless the user explicitly asks.
- Read existing files before editing and merge configuration changes instead of blindly replacing arrays/objects.
- Keep CLAUDE.md under 200 lines per file for reliable adherence
- Use human-gated task list workflow for multi-step tasks

## Git Rules
- Never commit or push on your own; only do so when the user explicitly asks.