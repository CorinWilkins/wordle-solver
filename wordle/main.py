from typing import Any, TypedDict
from tabulate import tabulate
import click
import re
from wordle.wordle import build_word_matches_naive, get_matches_for_guesses, get_next_best_word_log_memoed, get_all_possible_words


def validate_guess(ctx, param, value):
    if isinstance(value, tuple):
        return value

    try:
        rolls, _, dice = value.partition("d")
        return int(dice), int(rolls)
    except ValueError:
        raise click.BadParameter("format must be 'NdM'")


@click.command()
def find():
    all_words = get_all_possible_words()
    memoed_matches = build_word_matches_naive(all_words)
    guesses = []
    while True:
        length = len(guesses)
        guess = Guess()
        message = 'Please enter a guessed word' +  (', leave empty to exit' if length > 0 else '')
        while True:
            guess.word = click.prompt(message, default='', type=str).lower()
            if len(guess.word) == 5 or len(guess.word) == 0:
                break
            click.echo('guess must contain 5 letters')

        if guess.word == '' or guess.word == 'exit':
            if length > 0:
                break
            else: continue
        else:
            
            while True:
                guess.pattern = click.prompt('Please enter a guess\'s matches 2=green, 1=yellow, 0=black', type=str)
                if guess.pattern == '11111':
                    click.echo("Congratulations!")
                    return    
                if len(guess.pattern) == 5 and not re.findall(r'([^012])', guess.pattern):
                    break
                click.echo('pattern must contain 5 characters and only 0s, 1s, and 2s')


            guesses.append(guess)
            matches = get_matches_for_guesses(all_words, guesses)
            present(matches, memoed_matches)


def present(matches, memoed_matches):
    num_possibilities = len(matches)
    click.echo(f'{num_possibilities} possibilities')
    if num_possibilities < 1:
        click.echo('No remaining possiblities')
    elif num_possibilities == 1:
        click.echo(tabulate([(matches[0], 1)], headers=['Word', 'Mean Remaining Possiblities'], tablefmt="github"))
    else:    
        limit = 10
        next_best_words = get_next_best_word_log_memoed(matches, memoed_matches, limit)
        click.echo(tabulate(next_best_words, headers=['Word', 'Mean Remaining Possiblities'], tablefmt="github"))



            guesses.append(match)
            matches = get_matches_for_guesses(get_all_possible_words(), guesses)
            
            num_possibilities = len(matches)
            click.echo(f'{num_possibilities} possibilities')
            if num_possibilities < 1:
                return
            limit = 10
            next_best_words = get_next_best_word_log_memoed(matches, memoed_matches, limit)
            click.echo(tabulate(next_best_words, headers=['Word', 'Mean Remaining Possiblities'], tablefmt="github"))
