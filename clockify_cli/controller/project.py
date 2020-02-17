import click
from clockify_cli import net

def find_projects(workspaceID, archived=False, name=None, page=1):
    clients, code = net.call(f"v1/workspaces/{workspaceID}/projects/", json={
        "archived": archived,
        "name": name,
        "page": page,
    })
    net.response_code_handler(code)
    return clients

def _find_project(workspaceID, target_project, archived):
    page = 1
    projects = find_projects(workspaceID, archived=archived, page=page)
    while projects:
        for project in projects:
            if project['name'] == target_project or project['id'] == target_project:
                return project
        page = page + 1
        projects = find_projects(workspaceID, archived=archived, page=page)

    return None


def find_project(workspaceID, target_project):
    # first try to find in active projects:
    project = _find_project(workspaceID, target_project, False)
    if not project:
        project = _find_project(workspaceID, target_project, True)
    
    if not project:
        raise click.UsageError(f"Cannot find {target_project} project")

    return project

def add_project(workspaceID, name, color, client_id=None, public=False, note=None, billable=False, rate_amount=None, rate_currency=None):
    project_config = {"name": name, "public": public, "billable": billable}
    if client_id != None: 
        project_config['clientId'] = client_id
    if color != None:
        project_config["color"] = color
    if note != None:
        project_config['note'] = note
    if rate_amount != None and rate_currency != None:
        project_config["hourlyRate"] = {"amount": rate_amount, "currency": rate_currency}

    client, code = net.call(f'v1/workspaces/{workspaceID}/projects/', method="POST", json={
        "name": name,
        "clientId": client_id,
        "isPublic": public,
        "color": color,
        "note": note,
        "billable": billable,
        "hourlyRate": {
            "amount": rate_amount,
            "currency": rate_currency
        }
        })
    click.echo(f"DEBUG: {client}")
    net.response_code_handler(code, {400: click.UsageError(f"Project with name {name} already exists on workspace")})
    return client

def delete_project(workspaceID, projectID):
    deleted_project, code = net.call(f"v1/workspaces/{workspaceID}/projects/{projectID}", method="DELETE")
    net.response_code_handler(code, {400: click.UsageError("Project {projectID} not found")})
    return deleted_project