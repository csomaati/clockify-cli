import click

@click.group()
def client():
    click.echo("Client group called")

## stable api
@client.command()
@click.option("--archived", is_flag=True, default=False)
@click.option("--name", default=None)
@click.option("--page", type=int, default=1)
@click.option("--page-size", type=int, default=50)
@click.option("--workspace", required=True)
def find(archived, name, page, page_size, workspace):
    click.echo(f"Find clients on workspace {workspace} with following attributes: archived? {archived}. name? {name}. On page {page}, where page-size: {page_size}")

## working api
@client.command()
@click.option("--workspace", required=True)
def list(workspace):
    click.echo(f"List all clients in {workspace}")

## stable and working api
@client.command()
@click.option("--workspace", required=True)
@click.argument("name")
def add(name, workspace):
    click.echo(f"Add new client with name {name} on workspace {workspace}")

## working api
@client.command()
@click.option("--workspace", required=True)
@click.argument("id")
def details(workspace, id):
    click.echo(f"Find client in {workspace} with id {id}")

## working api
@client.command()
@click.option("--workspace", required=True)
@click.argument("name")
def delete(workspace, name):
    click.echo(f"Delete {name} client from {workspace}")

## working api
@client.command()
@click.option("--workspace", required=True)
@click.argument("old-name")
@click.argument("new-name")
def update(workspace, old_name, new_name):
    click.echo(f"Update client {old_name} at {workspace} to {new_name}")