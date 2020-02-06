import click
from clockify_cli import net

def find_clients(workspaceID, archived=False, name=None, page=1):
    clients, code = net.call(f"v1/workspaces/{workspaceID}/clients/", json={
        "archived": archived,
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

def _find_client(workspaceID, target_client, archived):
    page = 1
    clients = find_clients(workspaceID, archived=archived, page=page)
    while clients:
        for client in clients:
            if client['name'] == target_client or client['id'] == target_client:
                return client
        page = page + 1
        clients = find_clients(workspaceID, archived=archived, page=page)

    return None

def find_client(workspaceID, target_client):
    client = _find_client(workspaceID, target_client, False)
    if not client:
        client = _find_client(workspaceID, target_client, True)
    if not client:
        raise click.UsageError(f"Cannot find {target_client} client") 

    return client

def add_client(workspaceID, name):
    client, code = net.call(f'v1/workspaces/{workspaceID}/clients/', method="POST", json={"name": name})
    if code == 400:
        raise click.UsageError(f"Client with name {name} already exists on workspace")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return client
