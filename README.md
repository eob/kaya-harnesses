# `kaya-harnesses`

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

The official registry and reference catalog of reusable agent harness packages for the [Kaya](https://github.com/eob/kaya) autonomous agent runtime.

Kaya harnesses encapsulate multi-agent choreographies, prompt workflows, verification loops, and capability bindings into modular, versioned packages—enabling clean reproduction across benchmarks (such as **Terminal-Bench** and **SWE-bench**) and production environments.

---

## The HarnessBench Evaluation Thesis

**HarnessBench** evaluates *agent scaffolding and execution choreographies*, not LLM weights. 

- **Primary Evaluation LLM**: **Google Gemini** (`google/gemini-2.5-pro` and `google/gemini-2.5-flash`). By standardizing on Gemini models backed by Google Cloud credits, we run exhaustive, statistically robust evaluation sweeps at scale.
- **Official Comparative Baseline**: **Google Antigravity (`agy`)**. We evaluate Kaya harnesses side-by-side with `agy` (Google's first-party agent CLI) running the identical Gemini models, demonstrating exactly how agent scaffolding, tool binding, and verification loops impact solve rates and cost efficiency.
- **Standardized Trajectories & Cost**: Evaluated via Harbor; emits standard **ATIF v1.8** (`trajectory.json`) with token-to-dollar cost conversion via `kaya-utils`.

---

## Shorthand Resolution

When running workflows with the Kaya CLI or the Harbor framework adapter (`kaya-harbor`), harnesses can be referenced directly by shorthand name:

```bash
# Harbor evaluation run
harbor run -d "terminal-bench@2.0" --agent kaya_harbor:KayaHarborAgent --ak harness=experimental/react

# Direct Kaya CLI execution
kaya run --harness experimental/react
```

### Resolution Order

1. **Local Filesystem**: If the path begins with `.`, `/`, or exists directly on disk, it is loaded immediately.
2. **Local Registry Override**: If the environment variable `KAYA_HARNESSES_DIR` is set (e.g. `export KAYA_HARNESSES_DIR=/path/to/kaya-harnesses`), the loader looks under `$KAYA_HARNESSES_DIR/harnesses/<name>/` for zero-latency local development.
3. **Local Cache**: Checks `~/.cache/kaya/harnesses/<name>/`.
4. **Remote Registry**: Fetches or shallow-clones the package from `https://github.com/eob/kaya-harnesses` under `harnesses/<name>/`.

---

## Harness Package Structure

Each harness package is self-contained in its own directory:

```text
harnesses/
└── {namespace}/{name}/       # e.g. experimental/react, naive-react, red-to-green
    ├── harness.toml          # Declarative package manifest
    ├── harness.kaya          # Entrypoint choreography workflow
    └── README.md             # Documentation, strategy rationale, and benchmark metrics
```

### Manifest Specification (`harness.toml`)

```toml
[harness]
name = "red-to-green"
version = "0.1.0"
description = "Enforces test-reproduction before patching with compiler-guided repair."
author = "eob"
license = "Apache-2.0"
entrypoint = "harness.kaya"

[requirements]
capabilities = ["exec:bash", "fs:read", "fs:write"]

[models]
default = "google/gemini-2.5-pro"
temperature = 0.0
```

---

## Catalog

| Harness | Namespace | Strategy | Primary Model |
| :--- | :--- | :--- | :--- |
| **`naive-react`** | core | Unconstrained Thought $\to$ Action $\to$ Observation loop | `google/gemini-2.5-pro` |
| **`red-to-green`** | core | Mandatory test reproduction probe before code edits | `google/gemini-2.5-pro` |
| **`opencode-base`** | experimental | Standard phased coding agent baseline with self-repair | `google/gemini-2.5-pro` |
| **`minimal-harness`** | experimental | Connectivity & plumbing smoke test | `google/gemini-2.5-flash` |

---

## License

Apache 2.0.
