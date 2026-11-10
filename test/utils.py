from random import choices, sample

ascii_chars = (
    "0123456789"
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
)


def create_strings(s_len: int, edit_dist: int) -> list[str]:
    s1 = choices(ascii_chars, k=s_len)
    s2 = s1[:]
    for idx in sample(range(len(s1)), edit_dist):
        s2[idx] = choices([c for c in ascii_chars if c not in s1], k=1)[0]
    return ["".join(s1), "".join(s2)]


def levenshtein_reference(s1: str, s2: str) -> int:
    """Textbook Levenshtein distance reference implementation."""
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + cost)
            prev = temp
    return dp[n]
