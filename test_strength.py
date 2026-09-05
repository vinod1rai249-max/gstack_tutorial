"""Table-driven unit tests for strength.check()."""
import unittest

from strength import check


class CheckTests(unittest.TestCase):
    def test_table(self):
        # label, password, has_length, has_upper, has_lower, has_digit, has_special
        cases = [
            ("empty string", "", False, False, False, False, False),
            ("short password", "Ab1!", False, True, True, True, True),
            ("all lowercase", "abcdefgh", True, False, True, False, False),
            ("mixed missing special", "Abcdefg1", True, True, True, True, False),
            ("fully compliant", "T3st!ng1", True, True, True, True, True),
            ("unicode lowercase", "café1234", True, False, True, True, False),
            ("unicode uppercase", "CAFÉ1234", True, True, False, True, False),
            ("whitespace only", "        ", True, False, False, False, False),
            ("interior spaces", "my password", True, False, True, False, False),
            ("boundary 8 chars", "aaaaaaaa", True, False, True, False, False),
            ("boundary 7 chars", "aaaaaaa", False, False, True, False, False),
            ("non-ascii not special", "Abcdefg€", True, True, True, False, False),
        ]

        for label, password, has_length, has_upper, has_lower, has_digit, has_special in cases:
            with self.subTest(label=label, password=password):
                result = check(password)
                self.assertEqual(result.has_length, has_length)
                self.assertEqual(result.has_upper, has_upper)
                self.assertEqual(result.has_lower, has_lower)
                self.assertEqual(result.has_digit, has_digit)
                self.assertEqual(result.has_special, has_special)

                expected_score = sum(
                    (has_length, has_upper, has_lower, has_digit, has_special)
                )
                self.assertEqual(result.score, expected_score)
                self.assertEqual(len(result.reasons), 5 - expected_score)


if __name__ == "__main__":
    unittest.main()
