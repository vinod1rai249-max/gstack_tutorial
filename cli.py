"""CLI entry point for the password strength checker."""
import sys

from strength import check


def main() -> int:
    if len(sys.argv) > 1:
        password = sys.argv[1]
    elif not sys.stdin.isatty():
        password = sys.stdin.read().removesuffix("\n")
    else:
        print("Usage: python cli.py <password>  (or pipe via stdin)", file=sys.stderr)
        return 1

    result = check(password)
    print(f"Score: {result.score}/5")
    for reason in result.reasons:
        print(f"- {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
