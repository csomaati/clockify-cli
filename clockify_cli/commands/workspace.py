import click
from clockify_cli import tools, net

def debug_printer(ws):
    return f"{ws}"

def nameonly_printer(ws):
    return f'{ws["name"]}'

def default_printer(ws):
    return f'{ws["id"]}:{ws["name"]}'


printer = default_printer


def get_workspaces():
    response, code = net.call("v1/workspaces")
    if code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")

    # workspaces = [wsp.WorkspaceDto(w) for w in response]
    workspace = [w for w in response]
    return workspace

def find_workspace(name_or_id):
    workspaces = get_workspaces()
    for ws in workspaces:
        if ws["id"] == name_or_id or ws["name"] == name_or_id:
            return ws
    raise ValueError(f"Cannot find workspace with the given name/id {name_or_id}")

def add_workspace(name):
    ws, code = net.call("v1/workspaces/", method="POST", json={"name": name})    
    if code == 400:
        raise click.UsageError(f"Workspace {name} already exists, or workspace name is not valid")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return ws


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
    workspaces = get_workspaces()
    for ws in workspaces:
        click.echo(printer(ws))

@workspace.command()
@click.argument("name")
def add(name):
    new_ws = add_workspace(name)
    click.echo(printer(new_ws))