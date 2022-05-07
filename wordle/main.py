import re
from webbrowser import get
import click
from wordle.wordle import build_word_matches_naive, build_word_matches_processes, build_word_matches_threads, get_matches_for_guesses, get_next_best_word_log_memoed, get_all_possible_words



@click.command()
def find():
    memoed_matches = build_word_matches_processes()
    guesses = []
    while True:
        length = len(guesses)
        message = 'Please enter a guessed word' +  (', leave empty to exit' if length > 0 else '')
        while True:
            guess = click.prompt(message, default='', type=str).lower()
            if len(guess) == 5 or len(guess) == 0:
                break
            click.echo('guess must contain 5 letters')

        if guess == '':
            if length > 0:
                break
            else: continue
        else:
            guesses.append(guess)
            while True:
                match = click.prompt('Please enter a guess\'s matches 2=green, 1=yellow, 0=black', type=str)
                if len(match) == 5 and not re.findall(r'([^012])', match):
                    break
                click.echo('match must contain 5 characters and only 0s, 1s, and 2s')


            guesses.append(match)
            matches = get_matches_for_guesses(get_all_possible_words(), guesses)
            
            num_possibilities = len(matches)
            click.echo(f'{num_possibilities} possibilities')
            if num_possibilities < 1:
                return

            
            next_best_words = get_next_best_word_log_memoed(matches, memoed_matches)
            click.echo(f'next 10 best words {next_best_words}')


@click.command()
def generate_all_matches():
    build_word_matches_naive()
    build_word_matches_threads()
    build_word_matches_processes(2)
    build_word_matches_processes(4)
    build_word_matches_processes(8)
    build_word_matches_processes(16)
