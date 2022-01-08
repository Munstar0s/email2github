# -*- encoding: UTF-8 -*-

# Standard imports
import asyncio

# Third party imports
import click

# Application imports
from app.resolver import Resolver

@click.command()
@click.argument("emails")
@click.option("-o", "--output", type=click.Path(), help="Save the results as CSV in a file")
@click.option("-q", "--quiet", is_flag=True, help="Suppress helping messages")
def search(emails, output, quiet):
    """Search email addresses on Github

    This command try to resolve email addresses to Github accounts with various
    techniques, from the most simple to the most intrusive.

    Email addresses could be set from a file or from a comma-separated list.
    """

    try:
        loop     = asyncio.new_event_loop()
        resolver = Resolver(output=output, quiet=quiet)

        asyncio.set_event_loop(loop)
        loop.run_until_complete(resolver.run(emails))

    except SystemExit:
        loop.run_until_complete(resolver.stop())
        loop.close()
        exit(0)

    except KeyboardInterrupt:
        loop.run_until_complete(resolver.stop())
        loop.close()
        exit(0)
