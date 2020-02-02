
import requests, json, datetime
import os
import urllib
import requests
import click

from clockify_cli import commands 
from clockify_cli import net

VERBOSE = False
NAMEONLY = False
CLOCKIFY_API_KEY = os.environ.get('CLOCKIFY_API_KEY', None)

@click.group()
@click.option('--verbose', is_flag=True, help="Enable verbose output")
@click.option('--nameonly', is_flag=True, help="Print only names and do not display ids")
def cli(verbose, nameonly):
    global VERBOSE
    global NAMEONLY
    VERBOSE = verbose
    NAMEONLY = nameonly
    if CLOCKIFY_API_KEY != None and CLOCKIFY_API_KEY != "":
        net.set_api(CLOCKIFY_API_KEY)
    else:
        click.UsageError("Please set your API key in CLOCKIFY_API_KEY env variable")

cli.add_command(commands.workspace)
cli.add_command(commands.user)
cli.add_command(commands.client)
cli.add_command(commands.tag)
cli.add_command(commands.project)
cli.add_command(commands.task)

def main():
    cli(obj={})

if __name__ == "__main__":
    main()
