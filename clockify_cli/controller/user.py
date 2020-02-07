import click
from clockify_cli import net

def find_users(workspaceID, page=1):
    clients, code = net.call(f"v1/workspaces/{workspaceID}/users/", json={
        "page": page,
    })
    if code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return clients

def find_user(workspaceID, target_user):
    page = 1
    users = find_users(workspaceID, page=page)
    while users:
        for user in users:
            if user['name'] == target_user or user['id'] == target_user or user['email'] == target_user:
                return user
        page = page + 1
        users = find_users(workspaceID, page=page)

    raise click.UsageError(f"Cannot find {target_user} user")

def current_user():
    user, code = net.call("v1/user")
    if code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return user