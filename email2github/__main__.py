#!/usr/bin/env python -
# -*- encoding: UTF-8 -*-

# Standard imports

# Third party imports
import click

# Application imports
from commands.search import search
from commands.update import update

NAME    = "email2github"
VERSION = "1.0"

@click.group()
@click.version_option(VERSION, prog_name=NAME)
@click.pass_context
def cli(ctx):
    pass    # Entry point

cli.add_command(search)
cli.add_command(update)

if __name__ == "__main__":
    cli()
