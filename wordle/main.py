import click
import re
from wordle.entity import Guess
from wordle.gateway import Gateway
from wordle.presenter import Presenter
from wordle.usecase import WordleSolver


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