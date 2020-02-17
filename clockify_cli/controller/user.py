import click
from clockify_cli import net

def find_users(workspaceID, page=1):
    clients, code = net.call(f"v1/workspaces/{workspaceID}/users/", json={
        "page": page,
    })
    net.response_code_handler(code)
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
    net.response_code_handler(code)
    return user