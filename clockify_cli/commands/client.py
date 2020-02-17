import click
from clockify_cli import net
from clockify_cli.controller import workspace as workspace_controller
from clockify_cli.controller import client as client_controller

def debug_printer(c):
    return f"{c}"

def nameonly_printer(c):
    return f'{c["name"]}'

def default_printer(c):
    return f'{c["id"]}:{c["name"]}'

printer = default_printer

@click.group()
@click.pass_context
def client(ctx):
    global printer
    while ctx.parent: ctx = ctx.parent
    if ctx.params['nameonly']:
        printer = nameonly_printer
    elif ctx.params['verbose']:
        printer = debug_printer
    else:
        printer = default_printer

## stable api
@client.command()
@click.option("--archived", is_flag=True, default=False)
@click.option("--name", default=None)
@click.option("--page", type=int, default=1)
#@click.option("--page-size", type=int, default=50)
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
def find(archived, name, page, workspace):
    workspace_id = workspace_controller.find_workspace(workspace)['id'] 
    clients = client_controller.find_clients(workspace_id, archived, name, page)
    for client in clients:
        click.echo(printer(client))


## stable and working api
@client.command()
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.argument("name")
def add(name, workspace):
    workspace_id = workspace_controller.find_workspace(workspace)['id']
    new_client = client_controller.add_client(workspace_id, name)
    click.echo(printer(new_client))

# ## working api
# @client.command()
# @click.option("--workspace", required=True)
# def list(workspace):
#     click.echo(f"List all clients in {workspace}")


# ## working api
# @client.command()
# @click.option("--workspace", required=True)
# @click.argument("id")
# def details(workspace, id):
#     click.echo(f"Find client in {workspace} with id {id}")

# ## working api
# @client.command()
# @click.option("--workspace", required=True)
# @click.argument("name")
# def delete(workspace, name):
#     click.echo(f"Delete {name} client from {workspace}")

# ## working api
# @client.command()
# @click.option("--workspace", required=True)
# @click.argument("old-name")
# @click.argument("new-name")
# def update(workspace, old_name, new_name):
#     click.echo(f"Update client {old_name} at {workspace} to {new_name}")