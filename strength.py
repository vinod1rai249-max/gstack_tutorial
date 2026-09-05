"""Password strength scoring."""
from dataclasses import dataclass
import string


@dataclass
class PasswordResult:
    score: int
    reasons: list[str]
    has_length: bool
    has_upper: bool
    has_lower: bool
    has_digit: bool
    has_special: bool


def check(password: str) -> PasswordResult:
    """Score a password against five character-class rules."""
    has_length = len(password) >= 8
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)

    reasons = []
    if not has_length:
        reasons.append("Use at least 8 characters")
    if not has_upper:
        reasons.append("Add an uppercase letter")
    if not has_lower:
        reasons.append("Add a lowercase letter")
    if not has_digit:
        reasons.append("Add a digit")
    if not has_special:
        reasons.append("Add a special character")

    score = sum((has_length, has_upper, has_lower, has_digit, has_special))

    return PasswordResult(
        score=score,
        reasons=reasons,
        has_length=has_length,
        has_upper=has_upper,
        has_lower=has_lower,
        has_digit=has_digit,
        has_special=has_special,
    )
