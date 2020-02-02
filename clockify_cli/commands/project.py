import click

@click.group()
def project():
    click.echo("Tag group called")

@project.command()
@click.option("--archived", is_flag=True, default=False)
@click.option("--name", default=None)
@click.option("--page", type=int, default=1)
@click.option("--page-size", type=int, default=50)
@click.option("--workspace", required=True)
def find(archived, name, page, page_size, workspace):
    click.echo(f"Find project on workspace {workspace} with following attributes: archived? {archived}. name? {name}. On page {page}, where page-size: {page_size}")

@project.command()
@click.option("--workspace", required=True)
@click.argument("name")
@click.option("--client")
@click.option("--public", is_flag=True, default=True)
#@click.option("--estimate")
@click.option("--color")
@click.option("--note")
@click.option("--billable", is_flag=True, default=False)
@click.option("--rate-amount", type=int)
@click.option("--rate-currency")
def add(name, workspace, client, public, color, note, billable, rate_amount, rate_currency):
    click.echo(f"Add new project with name {name} on workspace {workspace}")

@project.command()
@click.option("--workspace", required=True)
@click.argument("project")
def delete(project, workspace):
    click.echo(f"Delete {project} from {workspace}")