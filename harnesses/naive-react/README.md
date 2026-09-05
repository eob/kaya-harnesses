# `naive-react` (Reference Baseline)

> **FIRST DRAFT / ARCHITECTURAL PSEUDOCODE — NOT A FINAL CONTRACT**  
> This harness illustrates the idiomatic Kaya specification for standard ReAct agent choreographies.

---

## Evaluation Role

In the **HarnessBench** matrix, `naive-react` represents the **unconstrained status quo**:
- **Workflow**: Standard Thought $\to$ Action $\to$ Observation.
- **Model**: `google/gemini-2.5-pro` (0.0 temperature).
- **Tooling**: `exec:bash`, `fs:read`, `fs:write`.
- **Termination**: Model-directed exit (no compiler, linter, or test gates enforced by the harness).

### Why Include It?
Most modern agent benchmarks (and commercial developer tools) deploy variants of this loop. When evaluated on Terminal-Bench, it reveals the characteristic pathology of unconstrained LLMs:
1. **Premature Victory**: The model makes an edit, assumes the syntax is valid, and completes the turn without running tests.
2. **Silent Breakage**: Unintended regressions in adjacent modules go undetected because no test suite execution was mandated.

By comparing `naive-react` side-by-side with `red-to-green` (holding Gemini 2.5 Pro constant), HarnessBench isolates the exact value of deterministic scaffolding ratchets.

---

## Usage

```bash
# Harbor evaluation run
harbor run -d "terminal-bench@2.0" \
  --agent kaya_harbor:KayaHarborAgent \
  --ak harness=naive-react \
  --ak model=google/gemini-2.5-pro

# Direct Kaya CLI run
kaya run --harness naive-react --input '{"instruction": "Fix bug in auth.ts"}'
```
