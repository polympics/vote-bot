"""Run the bot."""
import logging

from . import commands  # noqa: F401 - Just to register them.
from .bot import client
from .config import DISCORD_TOKEN

logging.basicConfig(level=logging.INFO)
client.run(DISCORD_TOKEN)
