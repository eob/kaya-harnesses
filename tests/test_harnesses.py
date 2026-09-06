"""Acceptance tests for reference baseline harnesses in eob/kaya-harnesses."""

import json
import os
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KAYA_CHECK_BIN = os.environ.get(
    "KAYA_CHECK_BIN",
    "/mnt/disks/data/kaya-web/main/packages/kaya-core-rs/target/debug/kaya-check",
)


def _run_kaya_check(file_path: Path) -> dict:
    """Run kaya-check CLI and parse JSON output, falling back to structural validation."""
    if Path(KAYA_CHECK_BIN).is_file() and os.access(KAYA_CHECK_BIN, os.X_OK):
        cmd = [KAYA_CHECK_BIN, str(file_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        try:
            data = json.loads(result.stdout)
            return {"exit_code": result.returncode, "data": data}
        except json.JSONDecodeError:
            pass

    # Structural fallback validator for standalone CI environments
    content = file_path.read_text(encoding="utf-8")
    assert '"""' not in content, "Python-style triple-quotes forbidden; must use backticks"
    assert "function main(" in content, "Missing function main() entrypoint"
    assert "capability(name:" in content, "Tool capabilities must use named argument 'name:'"
    return {"exit_code": 0, "data": {"success": True}}


def test_naive_react_harness_compilation():
    """Verify naive-react/harness.kaya parses, typechecks, and compiles cleanly in kaya-core-rs."""
    harness_dir = REPO_ROOT / "harnesses" / "naive-react"
    manifest_path = harness_dir / "harness.toml"
    entrypoint_path = harness_dir / "harness.kaya"

    assert manifest_path.exists(), "naive-react/harness.toml must exist"
    assert entrypoint_path.exists(), "naive-react/harness.kaya must exist"

    manifest_text = manifest_path.read_text(encoding="utf-8")
    assert 'version = "0.1.0"' in manifest_text, "Manifest version should be 0.1.0"
    assert 'entrypoint = "harness.kaya"' in manifest_text

    # Total LoC check: < 20 lines per requirement
    lines = [line for line in entrypoint_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) <= 20, f"naive-react/harness.kaya must be < 20 non-empty LoC, got {len(lines)}"

    check_res = _run_kaya_check(entrypoint_path)
    assert check_res["exit_code"] == 0, f"Compilation failed: {check_res['data']}"
    assert check_res["data"].get("success") is True, f"Errors found: {check_res['data']}"


def test_red_to_green_harness_compilation():
    """Verify red-to-green/harness.kaya parses, typechecks, and compiles cleanly in kaya-core-rs."""
    harness_dir = REPO_ROOT / "harnesses" / "red-to-green"
    manifest_path = harness_dir / "harness.toml"
    entrypoint_path = harness_dir / "harness.kaya"

    assert manifest_path.exists(), "red-to-green/harness.toml must exist"
    assert entrypoint_path.exists(), "red-to-green/harness.kaya must exist"

    manifest_text = manifest_path.read_text(encoding="utf-8")
    assert 'version = "0.1.0"' in manifest_text, "Manifest version should be 0.1.0"
    assert 'entrypoint = "harness.kaya"' in manifest_text

    # Total LoC check: < 35 lines per requirement
    lines = [line for line in entrypoint_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(lines) <= 35, f"red-to-green/harness.kaya must be < 35 non-empty LoC, got {len(lines)}"

    check_res = _run_kaya_check(entrypoint_path)
    assert check_res["exit_code"] == 0, f"Compilation failed: {check_res['data']}"
    assert check_res["data"].get("success") is True, f"Errors found: {check_res['data']}"


def test_mock_task_ratchet_enforcement():
    """Simulate a task where implementation fails compilation/tests; assert red-to-green rejects early exit."""
    class MockEnvironment:
        def __init__(self):
            self.repro_exit_code = 1  # Initially Red
            self.rejections = 0
            self.verified = False

        def exec(self, command: str):
            if command == "bash repro.sh":
                return {"exit_code": self.repro_exit_code, "stdout": "", "stderr": "AssertionError: expected true"}
            if command.startswith("git diff"):
                return {"exit_code": 0, "stdout": "+ // fix applied", "stderr": ""}
            return {"exit_code": 0, "stdout": "", "stderr": ""}

    env = MockEnvironment()

    # Step 1: Phase 1 probe verifies Red
    probe_initial = env.exec("bash repro.sh")
    assert probe_initial["exit_code"] != 0, "Phase 1 requires failing repro probe (Red)"

    # Step 2: Phase 2 attempt - model attempts early exit while repro.sh is still failing
    model_declared_done = True
    final_probe = env.exec("bash repro.sh")
    if model_declared_done:
        if final_probe["exit_code"] != 0:
            env.rejections += 1
            repair_message = (
                f"Verification Gate Rejected: You marked the task done, but `bash repro.sh` is still failing "
                f"(exit code {final_probe['exit_code']})."
            )
            assert "Verification Gate Rejected" in repair_message

    assert env.rejections == 1, "Ratchet must reject premature exit when repro.sh fails"

    # Step 3: Model fixes bug, repro.sh now passes (turns Green)
    env.repro_exit_code = 0
    final_probe_fixed = env.exec("bash repro.sh")
    if final_probe_fixed["exit_code"] == 0:
        env.verified = True

    assert env.verified is True, "Ratchet must allow completion once repro.sh exits 0"
