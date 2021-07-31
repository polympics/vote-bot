# Polympics Voting Bot

This is an interaction-based Discord bot for artwork voting in the Polympics.

## Installation

Dependencies:

- [Python 3.9+](https://www.python.org/downloads/) (Python 3.x where x >= 9)
- [Poetry](https://python-poetry.org/docs/master/#installation)

  Click the link for installation instructions, or:

  **\*nix:**
  `curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -`

  **Windows Powershell:**
  `(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -`

Once you have these dependencies installed:

1. **Create a virtual environment:** `poetry shell`
2. **Install dependencies:** `poetry install --no-dev`
   (remove `--no-dev` for development dependencies)

## Configuration

You can configure the bot using a file named `config.ini`, placed in this
directory. You can also provide options in environment variables, but config
file settings will overwrite environment variable settings.

The following options are available:

| Name                | Default                           | Description                          |
|---------------------|-----------------------------------|--------------------------------------|
| `discord_token`     | *Required*                        | A bot token for Discord.             |
| `db_password`       | *Required*                        | The database password.               |
| `db_name`           | `"polympics"`                     | The PostgreSQL database name.        |
| `db_user`           | `"polympics"`                     | The username for the database.       |
| `db_host`           | `"127.0.0.1"`                     | The database host address.           |
| `db_port`           | `5432`                            | The port for the database host.      |
| `polympics_api_url` | `https://polympics.herokuapp.com` | The base URL of the Cupid API.       |
| `guild_id`          | `814317488418193478`              | The ID of the Discord server to use. |
| `admin_role_id`     | `846944483315679242`              | The ID of the Discord admin role.    |

## Commands

The following commands are available:

- **Run the bot:** `poe bot`
- **Auto-format and lint code (requires dev dependecies):** `poe format`

Note that if to run outside of the Poetry shell (without running
`poetry shell`) you may have to replace `poe` with `poetry run poe`.
