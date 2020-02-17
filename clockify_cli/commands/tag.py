import click
from clockify_cli.controller import workspace as workspace_controller
from clockify_cli.controller import tag as tag_controller

def debug_printer(c):
    return f"{c}"

def nameonly_printer(c):
    return f'{c["name"]}'

def default_printer(c):
    return f'{c["id"]}:{c["name"]}'

printer = default_printer

@click.group()
@click.pass_context
def tag(ctx):
    global printer
    while ctx.parent: ctx = ctx.parent
    if ctx.params['nameonly']:
        printer = nameonly_printer
    elif ctx.params['verbose']:
        printer = debug_printer
    else:
        printer = default_printer


@tag.command()
@click.option("--name", default=None)
@click.option("--archived", is_flag=True, default=False)
@click.option("--page", type=int, default=1)
#@click.option("--page-size", type=int, default=50)
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
def find(archived, name, page, workspace):
    workspaceID = workspace_controller.find_workspace(workspace)["id"]
    tags = tag_controller.find_tags(workspaceID, archived, name, page)
    for tag in tags:
        click.echo(printer(tag))

@tag.command()
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.argument("name")
def add(name, workspace):
    workspaceID = workspace_controller.find_workspace(workspace)["id"]
    new_tag = tag_controller.add_tag(workspaceID, name)
    click.echo(printer(new_tag))