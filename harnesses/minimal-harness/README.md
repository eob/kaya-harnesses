# `minimal-harness` (Smoke Test)

> **FIRST DRAFT / ARCHITECTURAL PSEUDOCODE — NOT A FINAL CONTRACT**  
> This harness provides a one-shot connectivity smoke test for evaluation setups.

---

## Evaluation Role

In the **HarnessBench** matrix, `minimal-harness` is used to:
1. Verify end-to-end socket plumbing between `kayad` (host) and `kaya-satellite` (container).
2. Validate fast LLM inference over `google/gemini-2.5-flash` with zero looping overhead.
3. Validate ATIF trajectory export and JSON output serialization before initiating multi-turn runs.

---

## Usage

```bash
# Harbor smoke run
harbor run -d "terminal-bench@2.0" \
  --agent kaya_harbor:KayaHarborAgent \
  --ak harness=minimal-harness \
  --ak model=google/gemini-2.5-flash
```
