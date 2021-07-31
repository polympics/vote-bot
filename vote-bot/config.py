"""Tool for parsing and exporting config options."""
from __future__ import annotations

import configparser
import os
import pathlib
from typing import Any

BASE_PATH = pathlib.Path(__file__).parent.parent


def normalise_options(data: dict[str, Any]) -> dict[str, Any]:
    """Normalise config option keys."""
    return {key.lower().replace("-", "_"): value for key, value in data.items()}


data = normalise_options(os.environ)
parser = configparser.ConfigParser()
if parser.read(BASE_PATH / "config.ini"):
    data.update(normalise_options(parser["polympics-vote"]))


DB_NAME = data.get("db_name", "polympics-vote")
DB_USER = data.get("db_user", "polympics-vote")
DB_PASSWORD = data["db_password"]
DB_HOST = data.get("db_host", "localhost")
DB_PORT = int(data.get("db_port", 5432))

GUILD_ID = int(data.get("guild_id", 814317488418193478))
ADMIN_ROLE_ID = int(data.get("admin_role_id", 846944483315679242))
DISCORD_TOKEN = data["discord_token"]
POLYMPICS_API_URL = data.get("polympics_api_url", "https://polympics.herokuapp.com")
