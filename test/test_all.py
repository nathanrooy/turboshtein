import random
import unittest

from turboshtein import levenshtein

from .utils import ascii_chars, create_strings, levenshtein_reference


class TestLevenshtein(unittest.TestCase):
    def test_original_ascii(self) -> None:
        """Test in-place substitutions."""
        for s_len in range(1, 64):
            for edit_dist in range(s_len + 1):
                s1, s2 = create_strings(s_len, edit_dist)
                self.assertEqual(edit_dist, levenshtein(s1, s2))

    def test_known_pairs(self) -> None:
        """Test against known reference pairs and edge cases."""
        known_cases = [
            ("", "", 0),
            ("a", "", 1),
            ("", "a", 1),
            ("abc", "", 3),
            ("", "abc", 3),
            ("abc", "abc", 0),
            ("saturday", "sunday", 3),
            ("kitten", "sitting", 3),
            ("rosettacode", "raisethysword", 8),
            ("book", "back", 2),
            ("distance", "editing", 5),
            ("abcdef", "azced", 3),
            ("a", "b", 1),
            ("ab", "ba", 2),
            ("industry", "interest", 6),
            ("algorithm", "altruistic", 6),
        ]
        for s1, s2, expected in known_cases:
            with self.subTest(s1=s1, s2=s2):
                self.assertEqual(levenshtein(s1, s2), expected)
                self.assertEqual(levenshtein(s2, s1), expected)

    def test_random_differential_fuzzing(self) -> None:
        """Test random pairs against the reference implementation."""
        rng = random.Random(42)
        for _ in range(500):
            len1 = rng.randint(0, 63)
            len2 = rng.randint(0, 63)
            s1 = "".join(rng.choices(ascii_chars, k=len1))
            s2 = "".join(rng.choices(ascii_chars, k=len2))

            expected = levenshtein_reference(s1, s2)
            actual = levenshtein(s1, s2)
            symmetry = levenshtein(s2, s1)

            msg = f"Mismatch for {s1!r} and {s2!r}: got {actual}, expected {expected}"
            self.assertEqual(actual, expected, msg)
            sym_msg = f"Symmetry broken for {s1!r} and {s2!r}: {actual} != {symmetry}"
            self.assertEqual(symmetry, actual, sym_msg)

    def test_triangle_inequality(self) -> None:
        """Verify metric property: d(x, z) <= d(x, y) + d(y, z)."""
        rng = random.Random(1337)
        for _ in range(100):
            s1 = "".join(rng.choices("abcdef", k=rng.randint(0, 40)))
            s2 = "".join(rng.choices("abcdef", k=rng.randint(0, 40)))
            s3 = "".join(rng.choices("abcdef", k=rng.randint(0, 40)))

            d_13 = levenshtein(s1, s3)
            d_12 = levenshtein(s1, s2)
            d_23 = levenshtein(s2, s3)

            self.assertLessEqual(d_13, d_12 + d_23)

    def test_length_boundaries_and_exceptions(self) -> None:
        """Verify boundary lengths and exceptions."""
        # 63 characters is valid
        self.assertEqual(levenshtein("a" * 63, "a" * 63), 0)
        self.assertEqual(levenshtein("a" * 63, "b" * 63), 63)

        # > 63 characters must raise ValueError
        with self.assertRaises(ValueError):
            levenshtein("a" * 64, "b")
        with self.assertRaises(ValueError):
            levenshtein("a", "b" * 64)
        with self.assertRaises(ValueError):
            levenshtein("a" * 64, "b" * 64)

    def test_type_and_argument_errors(self) -> None:
        """Verify invalid argument types and counts raise TypeError."""
        with self.assertRaises(TypeError):
            levenshtein(123, "abc")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            levenshtein("abc", None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            levenshtein("abc")  # type: ignore[call-arg]
        with self.assertRaises(TypeError):
            levenshtein("a", "b", "c")  # type: ignore[call-arg]


if __name__ == "__main__":
    unittest.main()
