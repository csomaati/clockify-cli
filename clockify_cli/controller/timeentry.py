import click
import datetime
from clockify_cli import net

def add(workspaceID, start, projectID=None, taskID=None, end=None, billable=True, description=None, tag_ids=[]):
    request = {
        "start": f"{start.replace(microsecond=0).isoformat()}Z",
        "billable": billable,
        "tagIds": tag_ids
    }
    if projectID:
        request["projectId"] = projectID

    if taskID:
        request["taskId"] = taskID
    
    if end != None:
        request["end"] = f"{end.replace(microsecond=0).isoformat()}Z"

    if description:
        request["description"] = description

    new_entry, code = net.call(f"v1/workspaces/{workspaceID}/time-entries", method="POST", json=request)
    if code == 400:
        raise click.UsageError("Project/Tag doesn't exist or doesn't belong to workspace; Task doesn't exist or doesn't belong to project; Start datetime is after end datetime;Time entry requires additional info (check workspace settings);")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")

    return new_entry

def get(workspace_id, entry_id, use_duration_format, hydrated):
    request = {
        "consider-duration-format": use_duration_format,
        "hydrated": hydrated
    }
    entry, code = net.call(f"v1/workspaces/{workspace_id}/time-entries/{entry_id}", json=request)
    if code == 400:
        raise click.UsageError("Time entry with given ID doesn't exist")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return entry

def delete(workspace_id, entry_id):
    _, code = net.call(f"v1/workspaces/{workspace_id}/time-entries/{entry_id}", method="DELETE", response_required=False)
    if code == 400:
        raise click.UsageError("Time entry with given ID doesn't exist")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Unknown Error")
    return None 


def stop(workspace_id, user_id, end):
    entry, code = net.call(f"v1/workspaces/{workspace_id}/user/{user_id}/time-entries", method="PATCH", json={"end": f"{end.replace(microsecond=0).isoformat()}Z"})
    if code == 204:
        raise click.UsageError("No content")
    elif code == 400:
        raise click.UsageError("Required information is not present on currently running time entry. Check your workspace settings.")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Unknown Error")
    return entry


def find(workspace_id, user_id, request, request_config):
    rq = {}
    rq.update(request)
    rq.update(request_config)

    for k in [x for x in rq.keys()]:
        if rq[k] == None:
            del rq[k]
    
    entries, code = net.call(f"v1/workspaces/{workspace_id}/user/{user_id}/time-entries", json=rq)

    if code == 400:
        raise click.UsageError("User with given ID doesn't exist")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not Found")
    return entries
