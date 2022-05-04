import re
import click
from wordle.wordle import get_matches_for_guesses
import requests

target_url = 'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words'
word_list = requests.get(target_url).text.split("\n")
word_list.sort()

@click.command()
def find():
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
            matches = get_matches_for_guesses(word_list, guesses)
            
            click.echo(matches.join('\n'))
            click.echo(f'{len(matches)} possibilities')