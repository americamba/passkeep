from string import ascii_uppercase, ascii_lowercase, digits, punctuation


def test_complexity(pw: str) -> bool:
    """
    Test password to see if it meets complexity requirements
    :param pw: str password
    :return: bool
    """

    if len(pw) < 8:
        return False

    has_upper = False
    has_lower = False
    has_digit = False
    has_punc = False

    for c in pw:
        if not has_upper:
            if c in ascii_uppercase:
                has_upper = True
                continue

        if not has_lower:
            if c in ascii_lowercase:
                has_lower = True
                continue

        if not has_digit:
            if c in digits:
                has_digit = True
                continue

        if not has_punc:
            if c in punctuation and c not in ["\"", "`"]:
                has_punc = True
                continue

        if has_upper and has_lower and has_digit and has_punc:
            return True

    return False
