import requests, json, datetime
import os
import urllib
import requests
import click

ENDPOINT = "https://api.clockify.me/api/"
VERBOSE = False
NAMEONLY = False
CLOCKIFY_API_KEY = os.environ.get('CLOCKIFY_API_KEY', None)
CONFIG_FOLDER = os.environ.get('CLOCKIFY_CLI_CONFIG', '~/.clockify.cfg')
headers = {"X-Api-Key": None}

def name_or_id_to_id(name, name_to_id):
    try:
        # name is a valid name
        return name_to_id[name]
    except KeyError:
        for valid_id in name_to_id.values():
            if valid_id == name:
                # name is a valid id
                return valid_id
        raise ValueError(f"Given name {name} is not a valid name or id")

class WorkspaceType(click.ParamType):
    name = "workspace"

    def convert(self, value, param, ctx):
        try:
            return name_or_id_to_id(value, get_workspaces())
        except ValueError:
            self.fail(f"Could not found project with name/id '{value!r}'", param, ctx)

WorkspaceName = WorkspaceType()

def set_api(api):
    headers["X-Api-Key"] = api

def call(path, json={}, method="GET"):
    rq = getattr(requests, method.lower(), None)
    if rq == None:
        raise click.UsageError(f"Cannot perform http request with {method} method")

    url = urllib.parse.urljoin(ENDPOINT, path)
    try:
        r = rq(url, json=json, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise click.UsageError(f"Cannot load requested api endpoint {path} with data {json}. Call failed with the following error: {str(e)}")

    try:
        return r.json()
    except ValueError as e:
        raise click.UsageError(f"Cannot decode response at {path} with data {json}. Call failed with the following error: {str(e)}")

def get_workspaces():
    r = call("workspaces/")
    return {workspace["name"]:workspace["id"] for workspace in r}

def get_projects(workspace, clientid=None):
    r = call(f'workspaces/{workspace}/projects/')
    if clientid != None:
        r = [p for p in r if p["clientId"] == clientid]
    return {project["name"]:project["id"] for project in r}

def get_project_id(workspace, project):
    try:
        return name_or_id_to_id(project, get_projects(workspace))
    except ValueError:
        raise ValueError(f"Could not found project with project name/id {project}) in {workspace} workspace")

def get_clients(workspace):
    r = call(f'workspaces/{workspace}/clients')
    return {client["name"]:client["id"] for client in r}

def get_client_id(workspace, client):
    try:
        return name_or_id_to_id(client, get_clients(workspace))
    except ValueError:
        raise ValueError(f"Could not found client with client name/id {tag} in {workspace} workspace")

def get_tags(workspace):
    r = call(f'workspaces/{workspace}/tags/')
    return {tag["name"]:tag["id"] for tag in r}

def get_tag_id(workspace, tag):
    try:
        return name_or_id_to_id(tag, get_tags(workspace))
    except ValueError:
        raise ValueError(f"Could not found tag with tag name/id {tag} in {workspace} workspace")

def print_json(inputjson):
    click.echo(json.dumps(inputjson, indent=2))

def get_current_time():
    return str(datetime.datetime.utcnow().isoformat())+'Z'

def start_time_entry(workspace, description, billable="false", project=None, tags=None):
    start = get_current_time()
    project_id = None
    if project != None:
        project_id = get_project_id(workspace, project)

    tag_ids = []
    if tags != None:
        for tag in tags:
            tag_ids.append(get_tag_id(workspace, tag))

    body = {"start": start, "billable": billable, "description": description,
            "projectId": project_id, "taskId": None, "tagIds": tag_ids}
    r = call(f'workspaces/{workspace}/timeEntries/', json=body, method="POST")
    return r

def get_in_progress(workspace):
    r = call(f'workspaces/{workspace}/timeEntries/inProgress')
    return r

def finish_time_entry(workspace):
    current = get_in_progress(workspace)
    current_id = current["id"]
    body = {"start": current["timeInterval"]["start"], 
            "billable": current["billable"], "description": current["description"], 
            "projectId": current["projectId"], "taskId": current["taskId"], 
            "tagIds": current["tagIds"], "end": get_current_time()}
    r = call(f'workspaces/{workspace}/timeEntries/{current_id}', method="PUT", json=body)
    return r

def get_time_entries(workspace):
    r = call(f'workspaces/{workspace}/timeEntries/')
    return r[:10]

def remove_time_entry(workspace, tid):
    r = call(f'workspaces/{workspace}/timeEntries/{tid}')
    return r.json()

def add_workspace(name):
    body = {"name": name}
    r = call(f'workspaces/', json=body)
    return r

def add_project(workspace, name):
    body = {"name": name, "clientId": "", "isPublic": "false", "estimate": None,
            "color": None, "billable": None}
    r = call(f'workspaces/{workspace}/projects/', json=body)
    return r

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose output")
@click.option('--nameonly', is_flag=True, help="Print only names and do not display ids")
def cli(verbose, nameonly):
    global VERBOSE
    global NAMEONLY
    VERBOSE = verbose
    NAMEONLY = nameonly
    config_file = os.path.expanduser(CONFIG_FOLDER)
    if CLOCKIFY_API_KEY != None and CLOCKIFY_API_KEY != "":
        set_api(CLOCKIFY_API_KEY)
    elif os.path.exists(config_file):
        with open(config_file) as f:
            api = f.read()
            set_api(api)
    else:
        new = click.prompt("Your API key")
        with open(config_file, 'w') as f:
            f.write(new)
        set_api(new)

@click.command('start', short_help='Start a new time entry')
@click.argument('workspace', type=WorkspaceName)
@click.argument('description')
@click.option('--billable', is_flag=True, default=False, help="Set if entry is billable")
@click.option('--project', '-p', default=None, help="Project ID")
@click.option('--tag', '-g', multiple=True, help='Multiple tags permitted')
def start(workspace, description, billable, project, tag):
    ret = start_time_entry(workspace, description, billable, project, list(tag))
    if VERBOSE:
        print_json(ret)

@click.command('finish', short_help='Finish an on-going time entry')
@click.argument('workspace', type=WorkspaceName)
def finish(workspace):
    ret = finish_time_entry(workspace)
    if VERBOSE:
        print_json(ret)

@click.command('clients', short_help='Show all clients')
@click.argument('workspace', type=WorkspaceName)
def clients(workspace):
    data = get_clients(workspace)
    if VERBOSE:
        print_json(data)
    elif NAMEONLY:
        for name in data.keys():
            click.echo(f'{name}')
    else:
        for name in data:
            id = data[name]
            click.echo(f'{id}: {name}')

@click.command('tags', short_help='Show all tags')
@click.argument('workspace', type=WorkspaceName)
def tags(workspace):
    data = get_tags(workspace)
    if VERBOSE:
        print_json(data)
    elif NAMEONLY:
        for name in data.keys():
            click.echo(f'{name}')
    else:
        for name in data:
            id = data[name]
            click.echo(f'{id}: {name}')

@click.command('projects', short_help='Show all projects')
@click.argument('workspace', type=WorkspaceName)
@click.option('--client', '-c', default=None, help="Optional client filter")
def projects(workspace, client):
    if client != None:
        client = name_or_id_to_id(client, get_clients(workspace))
    data = get_projects(workspace,client)
    if VERBOSE:
        print_json(data)
    elif NAMEONLY:
        for name in data.keys():
            click.echo(f'{name}')
    else:
        for name in data:
            id = data[name]
            click.echo(f'{id}: {name}')

@click.command('inprogress', short_help='Show current active time entry')
@click.argument('workspace', type=WorkspaceName)
def inprogress(workspace):
    data = get_in_progress(workspace)
    if VERBOSE:
        print_json(data)
    elif NAMEONLY:
        for name in data.keys():
            click.echo(f'{name}')
    else:
        for name in data:
            id = data[name]
            click.echo(f'{id}: {name}')
@click.command('workspaces', short_help='Show all workspaces')
def workspaces():
    data = get_workspaces()
    if VERBOSE:
        print_json(data)
    elif NAMEONLY:
        for name in data.keys():
            click.echo(f'{name}')
    else:
        for name in data:
            id = data[name]
            click.echo(f'{id}: {name}')

@click.command('entries', short_help='Show previous 10 time entries')
@click.argument('workspace', type=WorkspaceName)
def entries(workspace):
    data = get_time_entries(workspace)
    if VERBOSE:
        print_json(data)
    elif NAMEONLY:
        for name in data.keys():
            click.echo(f'{name}')
    else:
        for entry in data:
            click.echo(f'{entry["id"]}: {entry["description"]}')

@click.command('remove_entry', short_help='Remove entry')
@click.argument('workspace', type=WorkspaceName)
@click.argument('time entry ID')
def remove_entry(workspace, tid):
    ret = remove_time_entry(workspace, tid)
    if VERBOSE:
        print_json(ret)

@click.command('add_workspace', short_help='Add a workspace')
@click.argument('name')
def add_w(name):
    ret = add_workspace(name)
    if VERBOSE:
        print_json(ret)

@click.command('add_project', short_help='Add a project')
@click.argument('workspace', type=WorkspaceName)
@click.argument('name')
def add_p(workspacename):
    ret = add_project(workspace, name)
    if VERBOSE:
        print_json(ret)

cli.add_command(start)
cli.add_command(finish)
cli.add_command(clients)
cli.add_command(tags)
cli.add_command(projects)
cli.add_command(workspaces)
cli.add_command(inprogress)
cli.add_command(entries)
cli.add_command(remove_entry)
cli.add_command(add_w)
cli.add_command(add_p)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
