"""Learning a new discord / python interface
"""

import os
import json
from pathlib import Path

import interactions

import common

ENV_PATH = Path('discord_bot_env.json')
GUILD_ID = 462259244390154240 # Add to env

def main():
    """Main entry point of script
    """

    if ENV_PATH.exists():
        env = json.load(open(ENV_PATH, 'r'))
        token = env['discord_token']
    elif os.getenv('DISCORD_TOKEN'):
        token = os.getenv('DISCORD_TOKEN')
    else:
        raise RuntimeError('No Discord Token available')

    bot = interactions.Client(token=token)

    @bot.command(name='roll',
                 description='Roll some dice!',
                 scope=462259244390154240)
    @interactions.option(description='Dice expression (and math operations)',)
    @interactions.option(description='Optional comment',)
    @interactions.option(description='(optional) number of time to repeat message')
    @interactions.option(description='True for a min operation (across each repeat)')
    @interactions.option(description='True for a max operation (across each repeat)')
    async def roll(ctx: interactions.CommandContext,
                   dice_expr: str,
                   comment: str=None,
                   repeat: int=1,
                   min_val: bool=False,
                   max_val: bool=False):

        if True in (min_val, max_val) and repeat == 1:
            repeat = 2

        if repeat < 1 or repeat > 100:
            await ctx.send("Repeat must be between 1 and 100",
                           ephemeral=True)
            return

        ephemeral = False
        if repeat == 1:
            dice_str, value = common.parse_dice_str(dice_expr)
            if value is None:
                msg = dice_str
                ephemeral = True
            else:
                msg = f"{dice_expr} --> __**{value}**__"

        else:
            dice_str, _ = common.parse_dice_str(dice_expr)
            values = [common.parse_dice_str(dice_expr)[1] for _ in range(repeat)]

            if min_val:
                min_val_actual = min(values)
                msg = (f"min({dice_expr}, {repeat}) --> "
                       f"min({values}) --> "
                       f"__**{min_val_actual}**__")

            elif max_val:
                max_val_actual = max(values)
                msg = (f"max({dice_expr}, {repeat}) --> "
                       f"max({values}) --> "
                       f"__**{max_val_actual}**__")

            else:
                msg = (f"repeat({dice_expr}, {repeat}) --> {values}")


        # Replicate results as necessary
        if not ephemeral and comment is not None:
            msg += f" # {comment}"

        await ctx.send(msg, ephemeral=ephemeral)

    bot.start()

if __name__ == '__main__':
    main()
