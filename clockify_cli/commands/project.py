import click
from clockify_cli import net 
from clockify_cli.controller import workspace as workspace_controller
from clockify_cli.controller import client as client_controller
from clockify_cli.controller import project as project_controller

def debug_printer(c):
    return f"{c}"

def nameonly_printer(c):
    return f'{c["name"]}'

def default_printer(c):
    return f'{c["id"]}:{c["name"]}'

printer = default_printer

@click.group()
@click.pass_context
def project(ctx):
    global printer
    while ctx.parent: ctx = ctx.parent
    if ctx.params['nameonly']:
        printer = nameonly_printer
    elif ctx.params['verbose']:
        printer = debug_printer
    else:
        printer = default_printer

@project.command()
@click.option("--archived", is_flag=True, default=False)
@click.option("--name", default=None)
@click.option("--page", type=int, default=1)
@click.option("--page-size", type=int, default=50)
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
def find(archived, name, page, page_size, workspace):
    workspace_id = workspace_controller.find_workspace(workspace)['id'] 
    projects = project_controller.find_projects(workspace_id, archived, name, page)
    for project in projects:
        click.echo(printer(project))

@project.command()
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.argument("name")
@click.argument("color")
@click.option("--client")
@click.option("--public", is_flag=True, default=True)
#@click.option("--estimate")
@click.option("--note")
@click.option("--billable", is_flag=True, default=False)
@click.option("--rate-amount", type=int)
@click.option("--rate-currency")
def add(name, workspace, client, public, color, note, billable, rate_amount, rate_currency):
    workspace_id = workspace_controller.find_workspace(workspace)['id']
    click.echo(f"DEBUG: workspace id: {workspace_id}")
    if client:
        client_id = client_controller.find_client(workspace_id, client)['id']
    else:
        client_id = None
    click.echo(f"DEBUG: client id: {client_id}")
    new_project = project_controller.add_project(workspace_id, name, color, client_id, public, note, billable, rate_amount, rate_currency)
    click.echo(printer(new_project))

@project.command()
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.argument("project")
def delete(project, workspace):
    workspace_id = workspace_controller.find_workspace(workspace)['id']
    project_id = project_controller.find_project(workspace_id, project)['id']
    deleted_project = project_controller.delete_project(workspace_id, project_id)
    click.echo(printer(deleted_project))