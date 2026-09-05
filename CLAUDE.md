# Hackathon AI Lab

Learning project for gstack workflows: AI-assisted engineering, project rules, persistent
memory, verification, code review, QA, security review, shipping.

## Subject Project

Password Strength Checker (CLI tool).

- Input: a password string
- Output: strength score (0-5) + list of reasons for the score
- Rules checked: length >= 8, has uppercase, has lowercase, has digit, has special char
- Explicitly OUT of scope: GUI, breach-database lookup, password generation, network
  calls, storage/database

## Working Rules

1. Keep the application intentionally small.
2. Do not introduce unnecessary technologies.
3. Prefer small, understandable changes.
4. Explain important architectural decisions before implementation.
5. Do not claim a task is complete without verification.
6. Keep project decisions documented in memory.json.

## Memory

Every stage appends one entry to `memory.json`:

```json
{"stage": "<name>", "decision": "<what was decided>", "timestamp": "<ISO8601>"}
```

## Verification

Verification means `verify.py` passes with exit code 0. A model saying "looks good" is
NOT verification.

## Testing

- Framework: none (stdlib only, no external deps). Test files run directly with `python`.
- `python test_strength.py` -- unit tests against the `PasswordResult` dataclass.
- `python verify.py` -- integration test, runs `cli.py` as a subprocess.

## gstack workflow -- fixed order, no skipping

/office-hours -> /plan-ceo-review -> /plan-eng-review -> BUILD -> verify.py -> /review ->
/qa -> /cso -> /ship
