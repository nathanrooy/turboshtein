import unittest
from random import choices, sample
from turboshtein import levenshtein


ascii = '''0123456789\
abcdefghijklmnopqrstuvwxyz\
ABCDEFGHIJKLMNOPQRSTUVWXYZ\
!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''


class TestLevenshtein(unittest.TestCase):
    def test_ascii(self):
        for s_len in range(1, 64):
            for edit_dist in range(0, s_len + 1):
                s1 = choices(ascii, k=s_len)
                s2 = s1[:]
                for idx in sample([i for i in range(len(s1))], edit_dist):
                    s2[idx] = choices([c for c in ascii if c not in s1], k=1)[0]
                self.assertEqual(
                    edit_dist,
                    levenshtein(''.join(s1), ''.join(s2))
                )


if __name__ == '__main__':
    unittest.main()
