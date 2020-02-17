import click
import dateparser
from clockify_cli.controller import workspace as workspace_controller
from clockify_cli.controller import project as project_controller
from clockify_cli.controller import task as task_controller
from clockify_cli.controller import tag as tag_controller
from clockify_cli.controller import timeentry as timeentry_controller
from clockify_cli.controller import user as user_controller


def debug_printer(c):
    return f"{c}"

def nameonly_printer(c):
    return f'{c["description"]}'

def default_printer(c):
    return f'{c["id"]}:{c["description"]}'

printer = default_printer

@click.group()
@click.pass_context
def entries(ctx):
    global printer
    while ctx.parent: ctx = ctx.parent
    if ctx.params['nameonly']:
        printer = nameonly_printer
    elif ctx.params['verbose']:
        printer = debug_printer
    else:
        printer = default_printer


@entries.command()
@click.argument("start")
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.option("--billable", is_flag=True, default=False)
@click.option("--description")
@click.option("--project")
@click.option("--task")
@click.option("--end")
@click.option("--tag", multiple=True)
def add(start, workspace, billable, description, project, task, end, tag):

    start_date = dateparser.parse(start).replace(microsecond=0)
    end_date = None
    if end != None:
        end_date = dateparser.parse(end).replace(microsecond=0)

    workspace_id = workspace_controller.find_workspace(workspace)["id"]

    project_id = None
    if project != None:
        project_id = project_controller.find_project(workspace_id, project)["id"] 

    task_id = None
    if task != None:
        task_id = task_controller.find_task(workspace_id, project_id, task)["id"]

    tag_ids = []
    for t in tag:
        tag_ids.append(tag_controller.find_tag(workspace_id, t)["id"])

    click.echo(tag_ids) 
    time_entry = timeentry_controller.add(workspace_id, start_date, project_id, task_id, end_date, billable, description, tag_ids) 
    click.echo(printer(time_entry))

@entries.command()
@click.argument("end")
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.option("--user", required=True)
def stop(workspace, user, end):
    workspace_id = workspace_controller.find_workspace(workspace)["id"]
    user_id = user_controller.find_user(workspace_id, user)["id"]

    end_date = None
    if end != None:
        end_date = dateparser.parse(end)
    
    entry = timeentry_controller.stop(workspace_id, user_id, end_date)
    click.echo(printer(entry))

@entries.command()
@click.argument("entryid")
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.option("--consider-duration-format", is_flag=True, default=False)
@click.option("--hydrated", is_flag=True, default=False)
def get(entryid, workspace, consider_duration_format, hydrated):
    workspace_id = workspace_controller.find_workspace(workspace)["id"]
    entry = timeentry_controller.get(workspace_id, entryid, consider_duration_format, hydrated)
    click.echo(printer(entry))


@entries.command()
@click.argument("entryid")
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
def delete(entryid, workspace):
    workspace_id = workspace_controller.find_workspace(workspace)["id"]
    timeentry_controller.delete(workspace_id, entryid)
    click.echo(f"{entryid} deleted")

@entries.command()
@click.option("--workspace", required=True, autocompletion=workspace_controller.workspace_autocomplete)
@click.option("--user", required=True)
@click.option("--description")
@click.option("--start")
@click.option("--end")
@click.option("--project")
@click.option("--task")
@click.option("--tag", multiple=True)
@click.option("--project-required/--project-not-required", default=True)
@click.option("--task-required/--tas-not-required", is_flag=True, default=True)
@click.option("--consider-duration-format/--ignore-duration-format", is_flag=True, default=True)
@click.option("--hydrated", is_flag=True, default=False)
@click.option("--in-progress", is_flag=True, default=False)
@click.option("--page", type=int, default=1)
def find(workspace, user, description, start, end, project, task, tag, project_required, task_required, consider_duration_format, hydrated, in_progress, page):
    workspace_id = workspace_controller.find_workspace(workspace)["id"]
    user_id = user_controller.find_user(workspace_id, user)["id"]

    start_date = None
    if start != None:
        start_date = dateparser.parse(start)

    end_date = None
    if end != None:
        end_date = dateparser.parse(end)

    project_id = None
    if project != None:
        project_id = project_controller.find_project(workspace_id, project)

    task_id = None
    if task != None:
        task_id = task_controller.find_task(workspace_id, project_id, task)

    tag_ids = []
    if tag != None:
        for t in tag:
            tag_ids.append(tag_controller.find_tag(workspace_id, t))

    request = {
        "description": description,
        "start": start_date,
        "end": end_date,
        "project": project_id,
        "task": task_id,
        "tags": tag_ids
    }

    request_config = {
        "project-required": project_required,
        "task-required": task_required,
        "consider-duration-format": consider_duration_format,
        "hydrated": hydrated,
        "in-progress": in_progress,
        "page": page
    }



    entries = timeentry_controller.find(workspace_id, user_id, request, request_config)
    for entry in entries:
        click.echo(printer(entry))
