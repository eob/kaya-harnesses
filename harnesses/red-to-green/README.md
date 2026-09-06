# `red-to-green` (Reference Challenger)

Reference challenger harness package for the Kaya agent runtime. Implements an opinionated TDD verification ratchet.

---

## Evaluation Role

In the **HarnessBench** matrix, `red-to-green` represents the **compiler/test verification ratchet**:
- **Workflow**: Two-phase TDD discipline (Reproduce $\to$ Repair $\to$ Gate).
- **Model**: `google/gemini-2.5-pro` (0.0 temperature).
- **Tooling**: `exec:bash`, `fs:read`, `fs:write`.
- **Termination**: Blocked by deterministic harness gates until `repro.sh` exits with 0.
- **LoC**: Under 35 lines of clean `.kaya` code.

### The Mechanism

1. **Phase 1 (Red Probe Gate)**:
   - The agent is forbidden from editing application source files until it authors a reproduction script (`repro.sh`).
   - The harness invokes `bash repro.sh` out-of-band and confirms it **fails** (non-zero exit code). If it passes, the harness forces another turn to write a real failing probe.
2. **Phase 2 (Implementation)**:
   - The agent makes surgical edits to the codebase.
3. **Phase 3 (Green Verification Ratchet Gate)**:
   - When the agent attempts to complete the turn, the harness independently re-runs `bash repro.sh`.
   - If the script fails, the completion event is rejected, and the failure stderr is injected back into the conversation for self-repair.
   - The agent can only exit when the reproduction script passes cleanly.

### Expected Benchmark Delta

On **Terminal-Bench** tasks:
- `naive-react` baseline typically plateaus around **35%–45%** due to unverified exits and untested syntax errors.
- `red-to-green` forces closure of the feedback loop, raising pass rates to **75%–85%** on identical foundation model weights (`gemini-2.5-pro`).

---

## Usage

```bash
# Harbor evaluation run
harbor run -d "terminal-bench@2.0" \
  --agent kaya_harbor:KayaHarborAgent \
  --ak harness=red-to-green \
  --ak model=google/gemini-2.5-pro

# Direct Kaya CLI run
kaya run --harness red-to-green --input '{"instruction": "Fix memory leak in buffer pool"}'
```
