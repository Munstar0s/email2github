# -*- encoding: UTF-8 -*-

# Standard imports
import logging

# Third party imports
from rich.logging import RichHandler
from rich.console import Console

# Application imports

FORMAT = "%(message)s"
logging.basicConfig(level="INFO", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()])

logger  = logging.getLogger()
console = Console()
