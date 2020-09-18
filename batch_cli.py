"""Интерфейс командной строки для добавления задач в очереди

Запускать из корня проекта (там где лежать docker-compose файлы)

Примеры:

    Список всех команд:

        $ pipenv run python src/batch_cli.py

    Помощь по конкретной команде:

        $ pipenv run python src/batch_cli.py <COMMAND_NAME> --help

"""
import click

from batch_cli_commands.AllMoviesCommand import AllMoviesCommand
from batch_cli_commands.AllMoviesInCategoryCommand import AllMoviesInCategoryCommand
from batch_cli_commands.MoviesInAllCategoriesCommand import MoviesInAllCategoriesCommand


@click.group()
def cli():
    """CLI to batch tasks creating"""
    pass


@cli.command()
def all_movies_short_info():
    """Extract movies short info from all category pages"""
    MoviesInAllCategoriesCommand().execute()


@cli.command()
@click.argument('relative_url', nargs=1, type=str)
def all_movies_in_category_short_info(relative_url):
    """Extract movies short info from one category pages"""
    AllMoviesInCategoryCommand(relative_url).execute()


@cli.command()
def all_movies():
    """Create tasks to get full info about all movies"""

    click.confirm('It will take a lot of time to process tasks. Do you want to continue?', abort=True)

    AllMoviesCommand().execute()


if __name__ == '__main__':
    cli()
