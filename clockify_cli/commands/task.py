import click
from clockify_cli.controller import workspace as workspace_controller
from clockify_cli.controller import project as project_controller
from clockify_cli.controller import task as task_controller

def debug_printer(c):
    return f"{c}"

def nameonly_printer(c):
    return f'{c["name"]}'

def default_printer(c):
    return f'{c["id"]}:{c["name"]}'

printer = default_printer

@click.group()
@click.pass_context
def task(ctx):
    global printer
    while ctx.parent: ctx = ctx.parent
    if ctx.params['nameonly']:
        printer = nameonly_printer
    elif ctx.params['verbose']:
        printer = debug_printer
    else:
        printer = default_printer

@task.command()
@click.option("--name", default=None)
@click.option("--active", is_flag=True, default=False)
@click.option("--page", type=int, default=1)
@click.option("--workspace", required=True)
@click.option("--project", required=True)
def find(active, name, page, workspace, project):
    workspace_id = workspace_controller.find_workspace(workspace)["id"]
    project_id = project_controller.find_project(workspace_id, project)["id"]
    tasks = task_controller.find_tasks(workspace_id, project_id, active, name, page)
    for task in tasks:
        click.echo(printer(task))

@task.command()
@click.option("--workspace", required=True)
@click.option("--project", required=True)
@click.option("--assignee", multiple=True)
@click.option("--estimate")
@click.option("--status")
@click.argument("name")
def add(name, workspace, project, assignee, estimate, status):
    workspace_id = workspace_controller.find_workspace(workspace)["id"]
    project_id = project_controller.find_project(workspace_id, project)["id"]
    new_task = task_controller.add_task(workspace_id, project_id, name, estimate, status)
    click.echo(printer(new_task))