from wordle.main import Guess
from wordle.wordle import build_word_matches_naive, get_matches_for_guesses, get_next_best_word_log_memoed


class WordleSolver():
    guesses = []

    def __init__(self, gateway, presenter) -> None:
        self.all_words = gateway.get_all_possible_words()
        self.memoed_matches = build_word_matches_naive(self.all_words)
        self.presenter = presenter

    def __call__(self, guess:Guess, limit):
        self.guesses.append(guess)
        get_matches_for_guesses(self.all_words, self.guesses)

        matches = get_matches_for_guesses(self.all_words, self.guesses)
        next_best_words = get_next_best_word_log_memoed(matches, self.memoed_matches, limit)
        self.presenter(matches, next_best_words)
