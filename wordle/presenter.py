from tabulate import tabulate
import click

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
