import click
from clockify_cli.controller import workspace as workspace_controller
from clockify_cli.controller import user as user_controller

def debug_printer(c):
    return f"{c}"

def nameonly_printer(c):
    return f'{c["name"]}'

def default_printer(c):
    return f'{c["id"]}:{c["name"]}({c["email"]})'

printer = default_printer

@click.group()
@click.pass_context
def user(ctx):
    global printer
    while ctx.parent: ctx = ctx.parent
    if ctx.params['nameonly']:
        printer = nameonly_printer
    elif ctx.params['verbose']:
        printer = debug_printer
    else:
        printer = default_printer

@user.command()
def current():
    current = user_controller.current_user()
    click.echo(printer(current))

@user.command()
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.option("--page", default=0, type=int)
def list(workspace, page):
    workspace_id = workspace_controller.find_workspace(workspace)["id"]
    users = user_controller.find_users(workspace_id, page)
    for user in users:
        click.echo(printer(user))