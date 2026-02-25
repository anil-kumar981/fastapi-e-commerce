import re


def validate_password(v: str) -> str:
    """
    Common password validator used across multiple schemas.
    Ensures the password meets complexity requirements:
    - At least one lowercase letter
    - At least one uppercase letter
    - At least one digit
    - At least one special character (@$!%*?&)
    - Minimum length is handled by Field(min_length=8) in the schema
    """
    if not re.search(r"[a-z]", v):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain at least one digit")
    if not re.search(r"[@$!%*?&]", v):
        raise ValueError(
            "Password must contain at least one special character (@$!%*?&)"
        )
    return v
