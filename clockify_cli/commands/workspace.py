import click
from clockify_cli import tools, net
from clockify_cli.controller import workspace as workspace_controller

def debug_printer(ws):
    return f"{ws}"

def nameonly_printer(ws):
    return f'{ws["name"]}'

def default_printer(ws):
    return f'{ws["id"]}:{ws["name"]}'


printer = default_printer



@click.group()
@click.pass_context
def workspace(ctx):
    global printer
    while ctx.parent: ctx = ctx.parent
    if ctx.params['nameonly']:
        printer = nameonly_printer
    elif ctx.params['verbose']:
        printer = debug_printer
    else:
        printer = default_printer

@workspace.command()
def list():
    workspaces = workspace_controller.get_workspaces()
    for ws in workspaces:
        click.echo(printer(ws))

@workspace.command()
@click.argument("name")
def add(name):
    new_ws = workspace_controller.add_workspace(name)
    click.echo(printer(new_ws))