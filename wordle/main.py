import click
from wordle.wordle import get_matches_for_guesses
import requests

target_url = 'https://raw.githubusercontent.com/tabatkins/wordle-list/main/words'
word_list = requests.get(target_url).text.split("\n")

@click.command()
def find():
    guesses = []
    while True:
        length = len(guesses)
        message = 'Please enter a guessed word' +  (', leave empty to return results' if length > 0 else '')
        guess = click.prompt(message, default='', type=str)
        if guess == '':
            if length > 0:
                break
            else: continue


        guesses.append(guess)
        guesses.append(click.prompt('Please enter a guess\'s matches', type=str))

    click.echo(get_matches_for_guesses(word_list, guesses))