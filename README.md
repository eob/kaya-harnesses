# kaya-harnesses

The official registry and reference catalog of reusable agent harness packages for the [Kaya](https://github.com/eob/kaya) autonomous agent runtime.

Kaya harnesses encapsulate multi-agent choreographies, prompt workflows, verification loops, and capability bindings into modular, versioned packages—enabling clean reproduction across benchmarks (such as Terminal-Bench and SWE-bench) and production environments.

---

## Shorthand Resolution

When running workflows with the Kaya CLI or the Harbor framework adapter (`kaya-harbor`), harnesses can be referenced directly by shorthand name:

```bash
# Harbor evaluation run
harbor run -d "terminal-bench@2.0" --agent kaya --ak harness=experimental/react

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
license = "MIT"
entrypoint = "harness.kaya"

[requirements]
capabilities = ["exec:bash", "fs:read", "fs:write"]

[models]
default = "anthropic/claude-3-7-sonnet"
temperature = 0.0
```

---

## Canonical Reference Harnesses

| Harness | Namespace | Description | Status |
| :--- | :--- | :--- | :--- |
| **`naive-react`** | `harnesses/naive-react` | Standard unconstrained baseline ReAct agent loop. | Planned ([HARNESSBENCH-006](https://github.com/eob/kaya-web)) |
| **`red-to-green`** | `harnesses/red-to-green` | Strict TDD ratchet requiring failure reproduction probe before repair and verification before completion. | Planned ([HARNESSBENCH-006](https://github.com/eob/kaya-web)) |

---

## Contributing

New harnesses can be contributed via pull request:
1. Create a directory under `harnesses/{name}` or `harnesses/{namespace}/{name}`.
2. Provide a valid `harness.toml` and executable `harness.kaya`.
3. Include a `README.md` documenting performance, token usage, and design rationale.
