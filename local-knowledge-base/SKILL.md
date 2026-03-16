---
name: local-knowledge-base
description: >-
  智能知识库管理。支持文档收录、Markdown转换、Excel复杂度分析、FAQ/BADCASE维护和基于本地知识库的问答。
  适用于“知识库”“收录”“归档”“入库”“基于知识库回答”等场景。首次使用需要指定知识库目录。
  建议知识问答优先通过 subagent 调用，避免检索过程占用主对话上下文。
---

# Local Knowledge Base Skill

## When To Use

- 用户要把文件收录进本地知识库
- 用户要基于知识库内容提问
- 用户要查看、迁移或初始化知识库

## Step 1: Environment Check

Always run first:

```bash
python scripts/ensure_deps.py
```

If this fails, stop and report the exact dependency error.

## Step 2: Resolve KB Path

Run:

```bash
python scripts/kb_config.py --check
```

- If `configured` is `false`, ask the user for a target folder, then run:

```bash
python scripts/kb_config.py --set <path>
python scripts/kb_init.py <path>
```

- If `configured` is `true`, use the returned `kb_path`.

## Step 3: Identify Intent

### Ingestion Intent

Typical signals:

- 用户提到“收录”“入库”“归档”
- 用户附带文件并要求放入知识库

Action:

- Follow [references/INGESTION_WORKFLOW.md](./references/INGESTION_WORKFLOW.md)

### Q&A Intent

Typical signals:

- 用户基于知识库内容提问
- 没有新文件需要收录

Action:

- Follow [references/QA_WORKFLOW.md](./references/QA_WORKFLOW.md)

### Management Intent

Typical signals:

- 查看当前知识库位置或结构
- 初始化新库
- 迁移知识库

Actions:

- 查看位置: `python scripts/kb_config.py --get`
- 迁移目录: `python scripts/kb_config.py --migrate <new_path>`
- 初始化目录: `python scripts/kb_init.py <path>`

## Ingestion Rules

- 对 DOCX / DOC / PDF / PPTX / PPT 使用 `scripts/smart_convert.py`
- 对 Excel 先使用 `scripts/complexity_analyzer.py` 判断路由
- 扫描版 PDF 若返回 `needs_ocr: true`，优先调用 OCR Skill；若环境中没有 OCR Skill，明确告诉用户这是阻塞点
- 冲突检测必须按语义进行，不能只看文件名
- 更新 `README.md` 时，优先维护导航质量

## Q&A Rules

- 优先 FAQ
- 再看 README 导航
- 再做目标文件阅读
- 最后才做关键词搜索
- 回答必须给来源
- 无结果要写入 `BADCASE.md`

## File Update Safety

When changing `FAQ.md`, `BADCASE.md`, or `README.md`, never partially overwrite the file. Prepare the full new content and replace atomically. See [references/FAQ_OPERATIONS.md](./references/FAQ_OPERATIONS.md).
