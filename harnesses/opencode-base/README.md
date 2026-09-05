# `opencode-base` (Reference Baseline)

> **FIRST DRAFT / ARCHITECTURAL PSEUDOCODE — NOT A FINAL CONTRACT**  
> This harness illustrates the idiomatic Kaya specification for standard SWE-agent / OpenCode phased prompt architectures.

---

## Evaluation Role

In the **HarnessBench** matrix, `opencode-base` represents the **structured prompt & phased guidance approach**:
- **Workflow**: Phased orientation (Explore $\to$ Reproduce $\to$ Edit $\to$ Verify), standard in many popular open-source coding agents.
- **Model**: `google/gemini-2.5-pro` (0.0 temperature).
- **Tooling**: `exec:bash`, `fs:read`, `fs:write`.
- **Termination**: Soft heuristic guidelines in the system prompt rather than hard deterministic compiler gates.

### Comparison Point

Unlike `red-to-green` (which physically halts the agent at the harness runtime if `repro.sh` does not fail or pass), `opencode-base` relies on **prompt-level self-discipline**. This comparison tests the central question:  
*Does detailed prompt engineering match the reliability of declarative runtime verification gates?*

---

## Usage

```bash
# Harbor evaluation run
harbor run -d "terminal-bench@2.0" \
  --agent kaya_harbor:KayaHarborAgent \
  --ak harness=opencode-base \
  --ak model=google/gemini-2.5-pro

# Direct Kaya CLI run
kaya run --harness opencode-base --input '{"instruction": "Add missing validation check to User model"}'
```
