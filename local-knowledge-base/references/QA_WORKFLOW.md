# Question Answering Workflow

## First Principles

- Fast answers should come from already validated knowledge, not from rereading the whole KB every time.
- README is navigation, not decoration. If README is bad, retrieval quality collapses.
- Fallback search is necessary, but it is later in the chain because blind grep is noisy.

## Stage 1: FAQ Fast Path

1. Read `FAQ.md`.
2. Look for direct or near-direct matches.
3. If a reliable FAQ match exists, answer from it and cite `FAQ.md`.

## Stage 2: README Navigation

1. Read `README.md` and any relevant subdirectory README files.
2. Identify the most likely category or file.
3. If a large-file overview exists, read that before opening the full document.

## Stage 3: Targeted File Reading

1. Open the most likely files first.
2. Read only the sections required to answer the question.
3. Preserve source references with file path and line anchors when possible.

## Stage 4: Keyword Search Fallback

1. If targeted reading fails, grep the KB for high-signal keywords.
2. Use the search results to choose the next files to read.
3. Do not answer from grep hits alone. Read the underlying file.

## Stage 5: Answer Generation

Build the answer from the narrowest verified sources available:

- answer
- cited sources
- limits or ambiguity, when the KB is incomplete

## Stage 6: No-Result Handling

If nothing reliable is found:

1. Say the KB does not currently contain a verified answer.
2. Record the question in `BADCASE.md`.
3. If the user later confirms a good answer, add it to FAQ per [FAQ_OPERATIONS.md](./FAQ_OPERATIONS.md).

## Satisfaction Feedback

- Satisfied with a knowledge-file answer: promote it into FAQ.
- Unsatisfied answer: record or update BADCASE.
- Satisfied FAQ answer: increment usage count.
- Unsatisfied FAQ answer: correct or remove it.
