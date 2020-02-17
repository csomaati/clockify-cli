import click
from clockify_cli import net

def find_tasks(workspaceID, projectID, active=False, name=None, page=1):
    clients, code = net.call(f"v1/workspaces/{workspaceID}/projects/{projectID}/tasks/", json={
        "is-active": active,
        "name": name,
        "page": page,
    })
    if code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return clients

def _find_task(workspaceID, projectID, target_task, active):
    page = 1
    tasks = find_tasks(workspaceID, projectID, active=active, page=page)
    while tasks:
        for task in tasks:
            if task['name'] == target_task or task['id'] == target_task:
                return task
        page = page + 1
        tasks = find_tasks(workspaceID, projectID, active=active, page=page)

    return None


def find_task(workspaceID, projectID, target_task):
    # first try to find in active tasks:
    task = _find_task(workspaceID, projectID, target_task, False)
    if not task:
        task = _find_task(workspaceID, projectID, target_task, True)
    
    if not task:
        raise click.UsageError(f"Cannot find {target_task} task")

    return task


def add_task(workspaceID, projectID, name, estimate=None, status=None):
    request = {
        "projectId": projectID,
        "name": name,
    }
    if estimate != None:
        request["estimate"] = estimate
    if status != None:
        request["status"] = status
    new_task, code = net.call(f"v1/workspaces/{workspaceID}/projects/{projectID}/tasks/", method="POST", json=request)
    if code == 400:
        raise click.UsageError(f"Task {name} already exists or {projectID} is doesn't exist")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return new_task