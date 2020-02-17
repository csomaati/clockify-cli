import click
from clockify_cli import net

def workspace_autocomplete(ctx, args, incomplete):
    candidates = []
    workspaces = get_workspaces()
    for workspace in workspaces:
        candidates.append(workspace["name"])
    return [x for x in candidates if x.startswith(incomplete)]


def get_workspaces():
    response, code = net.call("v1/workspaces")
    net.response_code_handler(code)

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
    net.response_code_handler(code, {400: click.UsageError(f"Workspace {name} already exists, or workspace name is not valid")})
    return ws
