import unittest
from turboshtein import levenshtein
from .utils import create_strings


class TestLevenshtein(unittest.TestCase):
    def test_ascii(self):
        for s_len in range(1, 64):
            for edit_dist in range(0, s_len + 1):
                s1, s2 = create_strings(s_len, edit_dist)
                self.assertEqual(
                    edit_dist,
                    levenshtein(s1, s2)
                )


if __name__ == '__main__':
    unittest.main()