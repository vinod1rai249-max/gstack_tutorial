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

On Windows, `verify.py` skips one of its seven checks (the no-argv + real-TTY
case) because Windows has no `pty` module in the standard library -- expect
"7/7" on Linux/macOS but a documented skip on Windows, not a failure.

No external dependencies -- Python standard library only.

See `CLAUDE.md` for project rules and the gstack workflow this project was built
through.
