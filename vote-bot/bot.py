"""The Discord bot client."""
from dslash import CommandClient
from polympics import UnauthenticatedClient

from .config import GUILD_ID, POLYMPICS_API_URL

client = CommandClient(guild_id=GUILD_ID)
polympics = UnauthenticatedClient(base_url=POLYMPICS_API_URL)


@client.event
async def on_ready():
    """Print to the console when the bot is ready."""
    print(f"Discord: Logged in as {client.user}.")
    print("----------")
