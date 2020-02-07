import click
from clockify_cli import net

def find_tags(workspaceID, archived=False, name=None, page=1):
    clients, code = net.call(f"v1/workspaces/{workspaceID}/tags/", json={
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

def _find_tag(workspaceID, target_tag, archived):
    page = 1
    tags = find_tags(workspaceID, archived=archived, page=page)
    while tags:
        for tag in tags:
            if tag['name'] == target_tag or tag['id'] == target_tag:
                return tag
        page = page + 1
        tags = find_tags(workspaceID, archived=archived, page=page)

    return None


def find_tag(workspaceID, target_tag):
    # first try to find in active tags:
    tag = _find_tag(workspaceID, target_tag, False)
    if not tag:
        tag = _find_tag(workspaceID, target_tag, True)
    
    if not tag:
        raise click.UsageError(f"Cannot find {target_tag} tag")

    return tag


def add_tag(workspaceID, name):
    tag, code = net.call(f"v1/workspaces/{workspaceID}/tags", method="POST", json={"name": name})
    if code == 400:
        raise click.UsageError(f"Tag {name} already exists")
    elif code == 401:
        raise click.UsageError("Unauthorized")
    elif code == 403:
        raise click.UsageError("Forbidden")
    elif code == 404:
        raise click.UsageError("Not found")
    return tag