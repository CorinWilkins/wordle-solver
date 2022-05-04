from unittest import TestCase
from wordle.wordle import check_wordle, get_matches_for_guess, get_matches_for_guesses


class CheckWordle(TestCase):
    def test_chars_in_correct_place_returns_2s(self):
        self.assertEqual(check_wordle("words", "force"), "02200") 

    def test_chars_in_wrong_place_returns_1s(self):
        self.assertEqual(check_wordle("words", "paved"), "00010")

    def test_chars_in_wrong_and_correct_place_returns_one_2(self):
        self.assertEqual(check_wordle("saves", "words"), "00002") 

    def test_chars_in_wrong_and_correct_place(self):
        self.assertEqual(check_wordle("aaazz", "xxaaa"), "11200") 
    
    def test_multiple_chars_in_wrong_place(self):
        self.assertEqual(check_wordle("aaazz", "xxxaa"), "11000") 


class GetMatchesForGuess(TestCase):
    def test_exact_match(self):
        result = get_matches_for_guess(["axxxx", "ayyyy", "xxxxx", "yyyyy", "zzzzz"], "about", "20000")
        self.assertEqual(result, ["axxxx", "ayyyy"])
    
    def test_exact_matches(self):
        result = get_matches_for_guess(["axxxx", "ayyyy", "xxxxx", "yyyyy", "zzzzz"], "heyyy", "00222")
        self.assertEqual(result, ["ayyyy", "yyyyy"])

    def test_fuzzy_matches(self):
        result = get_matches_for_guess(["axxxx", "daddd"], "abccc", "10000")
        self.assertEqual(result, ["daddd"])
    
    def test_multiple_fuzzy_matches(self):
        result = get_matches_for_guess(["axxax", "daddd"], "aaacc", "21000")
        self.assertEqual(result, ["axxax"])

    def test_negative_matches(self):
        result = get_matches_for_guess(["aaaaz", "bbbbz", "ccccz", "ddddz", "eeeez"], "abcdz", "00002")
        self.assertEqual(result, ["eeeez"])


class GetMatchesForGuesses(TestCase):
    def test_exact_match(self):
        result = get_matches_for_guesses(["axxxx", "ayyyy", "xxxxx", "yyyyy", "zzzzz"], ["about", "20000", "agony", "20002"])
        self.assertEqual(result, ["ayyyy"])
