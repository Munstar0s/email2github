# -*- encoding: UTF-8 -*-

# Standard imports

# Third party imports
import asyncio
import click

# Application imports
from app.updater import Updater

@click.command()
def update():
    """Update the latest version of the tool

    This command checks if a new version of the tool is available. If it is,
    it downloads from Github and installs it.
    """

    try:
        loop        = asyncio.new_event_loop()
        updater     = Updater()

        asyncio.set_event_loop(loop)
        loop.run_until_complete(updater.download())

    except SystemExit:
        loop.run_until_complete(updater.stop())
        loop.close()
        exit(0)

    except KeyboardInterrupt:
        loop.run_until_complete(updater.stop())
        loop.close()
        exit(0)
