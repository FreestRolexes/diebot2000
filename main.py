"""Learning a new discord / python interface
"""

import os
import json
from pathlib import Path
import random

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

    @bot.command(name='newdice',
                 description='Reset the hands of fate!',
                 scope=462259244390154240)
    async def newdice(ctx: interactions.CommandContext):
        adj = common.RAND.choice(common.ADJECTIVES)
        color = common.RAND.choice(list(common.COLOR_DICT))
        seed = adj + color.replace(' ', '').lower()
        common.RAND.seed(seed)
        await ctx.send(f"You draw {adj}, '{color}'-colored dice from the "
                       "dice bag!",
                       ephemeral=False)


    @bot.command(name='alien',
                 description='Game over, man!',
                 scope=462259244390154240)
    @interactions.option(description='Number of dice you are rolling',)
    @interactions.option(description='Number of stress dice (if you push)',)
    @interactions.option(description='Comment that will be printed w/ rolls',)
    async def alien(ctx: interactions.CommandContext,
                    numdice: int,
                    numstress: int=None,
                    comment: str=None):
        if numdice < 0:
            await ctx.send(f"`numdice` must be 1 or more (not {numdice})",
                           ephemeral=True)
            return

        normal = [random.randint(1, 6) for _ in range(numdice)]
        num_success = normal.count(6)

        if numstress is not None:
            stress_rolls = [random.randint(1, 6) for _ in range(numstress)]
            panic = (1 in stress_rolls)
        else:
            panic = False
            stress_rolls = []

        if panic:
            success_msg = "You panic! Roll on panic table (pg. 70)."
        elif (num_success > 0):
            success_msg = "You succeed!"
        else:
            success_msg = "You failed!"

        def replace_w_emojis(die_list, ignore_ones=False):
            one_indices = []
            six_indices = []
            for idx in range(len(die_list)):
                if die_list[idx] == 1:
                    one_indices.append(idx)
                elif die_list[idx] == 6:
                    six_indices.append(idx)

            if not ignore_ones:
                for idx in one_indices:
                    die_list[idx] = ":scorpion:"

            for idx in six_indices:
                die_list[idx] = ":dart:"

            return die_list

        normal = replace_w_emojis(normal, ignore_ones=True)
        stress_rolls = replace_w_emojis(stress_rolls, ignore_ones=False)
        msg = f"{success_msg} (rolls: {normal}"
        if stress_rolls:
            msg += f", stress rolls: {stress_rolls}"

        msg += ")"

        if comment is not None:
            msg += f" # {comment}"

        await ctx.send(msg,
                       ephemeral=False)



    @bot.command(name='init',
                 description='Who goes first?',
                 scope=462259244390154240)
    @interactions.option(description='Other named NPCs (commas between names)')
    async def init(ctx: interactions.CommandContext,
             npc_names: str=None):
        names = ['Jeff',
                 'Josh',
                 'Matt',
                 'Nick',
                 'Scott']
        random.shuffle(names)

        if npc_names is not None:
            npc_names = npc_names.split(',')
            print(npc_names)
            random.shuffle(npc_names)
            names += npc_names

        #if len(names) > 10:


        cards = list(range(10))
        init_vals = []
        for _ in range(len(names)):
            card = random.choice(cards)
            init_vals.append(card)
            cards.remove(card)

        sorted_names = sorted(zip(names, init_vals),
                              key = lambda x: x[1])

        title_str = f"{'__Name__': <10}{'__Init__': >20}"
        #init_strs = [f"{name: <10}{init: >20}" for name, init in zip(names, init_vals)]
        init_strs = [f"{name: <10}{init: >20}" for name, init in sorted_names]
        #init_strs = "\n".join(["\t" + name + ":\t\t" + str(init) for name, init in zip(names,
        #                                                                          init_vals)])
        #msg = "Init values:\n" + init_strs
        msg = title_str + "\n" + "\n".join(init_strs)
        await ctx.send(msg,
                       ephemeral=False)

    bot.start()

if __name__ == '__main__':
    main()
