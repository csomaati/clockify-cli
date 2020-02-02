import click

@click.group()
def tag():
    click.echo("Tag group called")

@tag.command()
@click.option("--name", default=None)
@click.option("--archived", is_flag=True, default=False)
@click.option("--page", type=int, default=1)
@click.option("--page-size", type=int, default=50)
@click.option("--workspace", required=True)
def find(archived, name, page, page_size, workspace):
    click.echo(f"Find tag on workspace {workspace} with following attributes: archived? {archived}. name? {name}. On page {page}, where page-size: {page_size}")

@tag.command()
@click.option("--workspace", required=True)
@click.argument("name")
def add(name, workspace):
    click.echo(f"Add new tag with name {name} on workspace {workspace}")