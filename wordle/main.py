from typing import Any, TypedDict
from tabulate import tabulate
import click
import re
from wordle.wordle import build_word_matches_naive, get_matches_for_guesses, get_next_best_word_log_memoed, get_all_possible_words


@click.command()
def find():
    
    usecase = WordleSolver(Gateway(),Presenter())
    while True:
        guess = Guess()
        while True:
            guess.word = click.prompt('Please enter a guessed word', default='', type=str).lower()
            if len(guess.word) == 5:
                break
            click.echo('guess must contain 5 letters')

        while True:
            guess.pattern = click.prompt('Please enter a guess\'s matches 2=green, 1=yellow, 0=black', type=str)
            if guess.pattern == '11111':
                click.echo("Congratulations!")
                return    
            if len(guess.pattern) == 5 and not re.findall(r'([^012])', guess.pattern):
                break
            click.echo('pattern must contain 5 characters and only 0s, 1s, and 2s')

        result = usecase(guess, 10)

class Guess:
    word: str
    pattern: str

class WordleSolver():
    guesses = []

    def __init__(self, gateway, presenter) -> None:
        self.all_words = gateway.get_all_possible_words()
        self.memoed_matches = build_word_matches_naive(self.all_words)
        self.presenter = presenter

    def __call__(self, guess:Guess, limit) -> Any:
        self.guesses.append(guess)
        get_matches_for_guesses(self.all_words, self.guesses)

        matches = get_matches_for_guesses(self.all_words, self.guesses)
        next_best_words = get_next_best_word_log_memoed(matches, self.memoed_matches, limit)
        self.presenter(matches, next_best_words)

class Presenter:
    def __call__(self, matches, next_best_words):
        num_possibilities = len(matches)
        click.echo(f'{num_possibilities} possibilities')
        if num_possibilities < 1:
            click.echo('No remaining possiblities')
        elif num_possibilities == 1:
            click.echo(tabulate(next_best_words, headers=['Word', 'Mean Remaining Possiblities'], tablefmt="github"))
        else:    
            click.echo(tabulate(next_best_words, headers=['Word', 'Mean Remaining Possiblities'], tablefmt="github"))

class Gateway:
    def get_all_possible_words(self):
        return get_all_possible_words()