# DieBot2000

My second Discord dice rolling robot.  This time we use "\" (slash) commands, since Discord is promising to eliminate bots that use the old command syntax.

## Installation and usage
- pip install the necessary libraries in `requirements.txt`
  - You probably want to run this in a virtual environment of some sort
- Add your server's private key to the environment, via two options:
  - Create a `discord_bot_env.json` file w/ following structure:
    - `{"discord_token":"YOUR TOKEN HERE"}`
  - Add `DISCORD_TOKEN` to your local environment variables (set equal to token)
  - NOTE: JSON file will take precedence over environment variable if both are set
- run `python main.py`

## Heroku
There are a few files included here just for Heroku usage:
- `Procfile` - specifies command to run
- `runtime.txt` - specifies version of python to use (chose something newish)

## Helpful Links
- `interactions.py` - Discord bot library
  - https://discord-py-slash-command.readthedocs.io/en/latest/quickstart.html
- A git repo I used to help understand running DieBot2000 on Heroku
  - https://github.com/tasukaru/discord.py-heroku
- My Heroku site for DieBot2000
  - https://dashboard.heroku.com/apps/diebot2000
