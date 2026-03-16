# FAQ and BADCASE Operations

## Core Rule

Do not write `FAQ.md` or `BADCASE.md` in place. Read the current file, prepare the full new content, write to a temporary file, then atomically replace the original file. This is the minimum safe approach when the skill may be called from subagents.

## Atomic Write Pattern

```python
from pathlib import Path

target = Path("FAQ.md")
temp = target.with_suffix(".tmp")
temp.write_text(updated_content, encoding="utf-8")
temp.replace(target)
```

## Scenario 1: Answer Came From FAQ

### User Is Satisfied

- Find the matching FAQ row.
- Increment `Usage Count`.
- Rewrite `FAQ.md` with atomic replace.

### User Is Not Satisfied And Gives A Better Answer

- Replace the old answer content.
- Keep the existing question.
- Rewrite `FAQ.md` with atomic replace.

### User Is Not Satisfied Without A Useful Correction

- Remove the FAQ row.
- Append the case to `BADCASE.md`.
- Use atomic replace for both files.

## Scenario 2: Answer Came From A Knowledge File

### User Is Satisfied

- Append a new FAQ row with initial usage count `1`.
- If FAQ is already too large, remove the least-used entry first.
- Rewrite `FAQ.md` with atomic replace.

### User Is Not Satisfied

- Append a record to `BADCASE.md`.
- Record the question, given answer, source file, and timestamp.
- Rewrite `BADCASE.md` with atomic replace.

## FAQ.md Format

```markdown
# FAQ - Frequently Asked Questions

| Question | Answer | Usage Count |
| --- | --- | --- |
| How do I apply for annual leave? | Log in to OA and submit the request three days ahead. | 15 |
```

## BADCASE.md Format

```markdown
# BADCASE - Gaps To Improve

## 2026-03-16 14:30

**Question**: How do I apply for salary adjustment?
**Given answer**: No relevant information found in the knowledge base.
**User feedback**: Unsatisfied
**Source file**: None

---
```
