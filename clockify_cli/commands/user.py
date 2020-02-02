import click


@click.group()
def user():
    click.echo("User group called")

@user.command()
def current():
    click.echo("Current user called")

@user.command()
@click.option("--page", default=0, type=int)
@click.option("--page-size", default=50, type=int)
def list(page, page_size):
    click.echo(f"List all user on page {page} (page size {page_size} called")