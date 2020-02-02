import click

@click.group()
def task():
    click.echo("Tag group called")

@task.command()
@click.option("--name", default=None)
@click.option("--active", is_flag=True, default=False)
@click.option("--page", type=int, default=1)
@click.option("--page-size", type=int, default=50)
@click.option("--workspace", required=True)
@click.option("--project", required=True)
def find(active, name, page, page_size, workspace, project):
    click.echo(f"Find task on workspace {workspace} with following attributes: active? {active}. name? {name}. On page {page}, where page-size: {page_size}")

@task.command()
@click.option("--workspace", required=True)
@click.option("--project", required=True)
@click.option("--asigne", multiple=True)
@click.option("--estimate")
@click.option("--status")
@click.argument("name")
def add(name, workspace):
    click.echo(f"Add new task with name {name} on workspace {workspace}")