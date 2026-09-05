# Password Strength Checker

A small CLI tool that scores password strength (0-5) against five character-class
rules. Built as a learning project for gstack's AI-assisted engineering workflow
(office-hours, plan review, build, verify, review, QA, security review, ship).

## Usage

Prefer piping the password via stdin -- an argument passed on the command line
(the second example below) can leak into shell history and process listings
(`ps`, `/proc/[pid]/cmdline`) on shared machines.

```bash
echo "password" | python cli.py
# Score: 2/5
# - Add an uppercase letter
# - Add a digit
# - Add a special character

python cli.py "T3st!ng1"
# Score: 5/5
```

If no password is given via argument or stdin (interactive TTY), the tool prints
usage to stderr and exits 1.

## Rules

One point each for:

- Length >= 8 characters
- Contains an uppercase letter
- Contains a lowercase letter
- Contains a digit
- Contains a special character (`string.punctuation`)

Letter-case checks are unicode-aware (per-character, so mixed-case unicode text
scores correctly). Special-character detection is ASCII-only by design.

## Files

- `strength.py` -- `PasswordResult` dataclass + `check()` pure scoring function
- `cli.py` -- entry point (argv/stdin input, plain-text output)
- `test_strength.py` -- table-driven unit tests against `check()`
- `verify.py` -- subprocess integration test against the CLI's I/O contract

## Development

```bash
python test_strength.py   # unit tests
python verify.py          # integration test
```

`verify.py` runs 8 checks on Linux/macOS (7 base checks plus a no-argv +
real-TTY check that needs a pty). On Windows there's no `pty` module in the
standard library, so that check is skipped -- expect "8/8" on Linux/macOS but
"7/7 checks passed" (with a `[SKIP]` line above it) on Windows, not a failure.

No external dependencies -- Python standard library only.

See `CLAUDE.md` for project rules and the gstack workflow this project was built
through.

## How This Was Built

This project exists to exercise gstack's full AI-assisted engineering pipeline
end to end, in the fixed order: `/office-hours -> /plan-eng-review -> BUILD ->
verify.py -> /review -> /qa -> /cso -> /ship`. The domain (a password checker)
is intentionally trivial so the workflow itself is the thing being tested. A
stage-by-stage decision log lives in `memory.json`; this section is the
narrative version.

**office-hours -- design.** Chose "Test-First with Dataclass Output" (three
files: `strength.py`, `cli.py`, `test_strength.py`) over the recommended
simpler split, for the more expressive `PasswordResult` dataclass output. Five
rules exactly, per-character unicode-aware upper/lowercase checks (not
whole-string -- `str.isupper()` on a mixed-case string returns `False`, which
would have silently broken scoring).

**plan-eng-review -- architecture review.** A 4-section internal review
(architecture, code quality, tests, performance) found and resolved 2 issues:
how `verify.py` should assert against a subprocess (parse the `Score:` line
and count reason lines -- it can't reach into a `PasswordResult`), and a
missing stdin-trailing-newline test case. An outside-voice pass (Codex was
unreachable -- expired auth, no OpenRouter credits -- so a Claude subagent
stood in) surfaced 7 further spec gaps, all resolved directly: special-char
detection is ASCII-only by design even though letter-case checks are
unicode-aware (an intentional asymmetry, not a bug); `score` is always
computed as `sum()` of the five booleans, never independently settable; an
empty string passed via `argv[1]` is a valid zero-length password, not
"missing input"; and `test_strength.py` / `verify.py` have a clean ownership
split (unit-level rule logic vs. CLI I/O contract) so nothing is tested twice.

**BUILD.** Implemented all four files exactly per the design and review
decisions -- no extra features, no extra abstractions. Both suites passed on
the first run. One environment-specific discovery along the way:
`subprocess.DEVNULL` reports `isatty() == True` in this Windows/Git-Bash
environment, so `verify.py`'s "non-tty EOF" case uses an empty piped string
instead -- a real pipe is reliably non-tty everywhere, `DEVNULL` isn't, here.

**review.** `/code-review` found 2 issues, both fixed: a `memory.json`
timestamp that had been invented out of chronological order, and a manual
`raw[:-1] if raw.endswith("\n") else raw` in `cli.py` replaced with the
equivalent, clearer `str.removesuffix("\n")`.

**qa.** `/qa` is built entirely around browser-driven web-app testing --
no URL, no browser here. Adapted it: ran 12 real-user and adversarial inputs
straight through `cli.py` (a common weak password, a password containing
shell metacharacters -- confirmed no injection risk since argv is never
shell-interpreted, a 10,000-character password for a perf sanity check, CRLF
and multi-line stdin, an emoji password, invalid UTF-8 bytes on stdin,
`--help` treated as a literal password since there's no argparse). Zero
issues found.

**cso.** A full daily-mode security audit across all 15 phases. The attack
surface is minimal by design -- no network, no auth, no dependencies, no
CI/CD, and the password itself is never persisted anywhere. Secrets
archaeology across git history came back clean. One candidate finding
survived to the confidence gate: `cli.py` accepts the password via
`sys.argv[1]`, a textbook CWE-214 pattern (visible via `ps` / process
listings / shell history). An independent verifier subagent scored it 3/10 --
not actionable for a single-user, no-persistence local CLI where stdin is
already offered as the safer path -- so it was filtered, not reported.
Verdict: 0 findings. One hygiene note did land: `.gstack/` (this project's
own tool-output directory) wasn't yet in `.gitignore`; fixed.

**ship.** Bumped to `v0.0.1.0`, wrote `CHANGELOG.md`, and ran the full
pre-landing + adversarial review pipeline against the docs-only diff. The
adversarial pass caught two real issues in this very README before it
shipped: the usage examples originally led with the argv form (the CWE-214
pattern `cso` had just reasoned about) with no caveat, and a later
documentation-sync pass caught that the Windows-vs-Linux/macOS check-count
claim in the Development section was stated backwards. Both were fixed and
re-verified before the branch was pushed. Codex's outside-voice and
adversarial passes were unavailable throughout this entire project (expired
auth, no OpenRouter credits) -- every cross-model review step fell back to a
same-family Claude subagent instead, which is weighed as a weaker signal than
a genuinely different model, and is noted as such at each step above.
