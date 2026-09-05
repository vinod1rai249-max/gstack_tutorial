"""Integration test: exercises cli.py end-to-end via subprocess.

Owns only the CLI I/O contract (argv/stdin/TTY/exit codes/output parsing).
Rule-logic coverage lives in test_strength.py, not here.
"""
import os
import subprocess
import sys

CLI_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cli.py")


def run(args, stdin_text=None):
    kwargs = {
        "args": [sys.executable, CLI_PATH, *args],
        "capture_output": True,
        "text": True,
    }
    if stdin_text is not None:
        kwargs["input"] = stdin_text
    return subprocess.run(**kwargs)


def parse_output(stdout):
    lines = stdout.splitlines()
    score_line = next((line for line in lines if line.startswith("Score: ")), None)
    reason_count = sum(1 for line in lines if line.startswith("- "))
    return score_line, reason_count


def check_case(label, proc, expected_exit, expected_score_line=None, expected_reason_count=None):
    ok = proc.returncode == expected_exit
    if expected_score_line is not None or expected_reason_count is not None:
        score_line, reason_count = parse_output(proc.stdout)
        if expected_score_line is not None:
            ok = ok and score_line == expected_score_line
        if expected_reason_count is not None:
            ok = ok and reason_count == expected_reason_count
    print(f"[{'PASS' if ok else 'FAIL'}] {label}")
    if not ok:
        print(f"  exit={proc.returncode} stdout={proc.stdout!r} stderr={proc.stderr!r}")
    return ok


def check_tty_case():
    """No argv, stdin is a real TTY: usage message + exit 1. POSIX only (needs a pty)."""
    try:
        import pty
    except ImportError:
        print("[SKIP] no argv + TTY stdin (usage, exit 1) -- no pty support on this platform")
        return None

    controller_fd, worker_fd = pty.openpty()
    try:
        proc = subprocess.run(
            [sys.executable, CLI_PATH],
            stdin=worker_fd,
            capture_output=True,
            text=True,
        )
    finally:
        os.close(worker_fd)
        os.close(controller_fd)

    ok = proc.returncode == 1 and "Usage:" in proc.stderr
    print(f"[{'PASS' if ok else 'FAIL'}] no argv + TTY stdin (usage, exit 1)")
    if not ok:
        print(f"  exit={proc.returncode} stdout={proc.stdout!r} stderr={proc.stderr!r}")
    return ok


def main() -> int:
    results = []

    results.append(check_case("argv input", run(["test"]), 0, "Score: 1/5", 4))
    results.append(
        check_case("fully compliant argv", run(["T3st!ng1"]), 0, "Score: 5/5", 0)
    )
    results.append(
        check_case("empty-string argv (valid zero-length password)", run([""]), 0, "Score: 0/5", 5)
    )
    results.append(
        check_case("stdin input", run([], stdin_text="test"), 0, "Score: 1/5", 4)
    )
    results.append(
        check_case(
            "stdin trailing newline stripped",
            run([], stdin_text="T3st!ng1\n"),
            0,
            "Score: 5/5",
            0,
        )
    )
    results.append(
        check_case("extra argv ignored", run(["test", "extra", "args"]), 0, "Score: 1/5", 4)
    )
    results.append(
        check_case(
            "no argv + non-tty stdin (EOF)",
            run([], stdin_text=""),
            0,
            "Score: 0/5",
            5,
        )
    )

    tty_result = check_tty_case()
    if tty_result is not None:
        results.append(tty_result)

    passed = sum(results)
    total = len(results)
    print(f"\n{passed}/{total} checks passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
