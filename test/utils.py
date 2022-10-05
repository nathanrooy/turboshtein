from random import choices, sample


ascii_chars = '''0123456789\
abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ\
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''


def create_strings(s_len, edit_dist):
    s1 = choices(ascii_chars, k=s_len)
    s2 = s1[:]
    for idx in sample([i for i in range(len(s1))], edit_dist):
        s2[idx] = choices([c for c in ascii_chars if c not in s1], k=1)[0]
    return [''.join(s1), ''.join(s2)]