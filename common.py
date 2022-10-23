"""Common functions for handling bot commands

Currently bridges the gap between pyparsing objects
"""

import pyparsing as pp
import random

import command_parser

DICE_EMOJI = {':d4:' : '<:d4:797105702878314556>',
              ':d6:' : '<:d6:797105706351460374>',
              ':d8:' : '<:d8:797105702367658065>',
              ':d10:' : '<:d10:797105706125492284>',
              ':d12:' : '<:d12:797105704678588418>',
              ':d20:' : '<:d20:797105703084752916>',
              ':d100:': 'd:100:'}

RAND = random.Random()

def make_math_parser():
    dice_roller = command_parser.DiceRoll(RAND)

    dice_parser = (pp.Optional(pp.Word(pp.nums)) +
                   pp.Suppress(pp.oneOf('d D')) +
                   pp.Word(pp.nums))
    dice_parser.setParseAction(dice_roller.parser_callback)

    int_parser = pp.Word(pp.nums)
    int_parser.setParseAction(lambda x: int(x[0]))

    sign_op = pp.oneOf('+ -')
    mult_op = pp.oneOf('* /')
    add_op = pp.oneOf('+ -')

    combiner = command_parser.CombineOp()
    signer = command_parser.SignOp()

    return pp.infixNotation(dice_parser | int_parser,
                            [(sign_op, 1,
                              pp.opAssoc.RIGHT,
                              signer.parser_callback),
                             (mult_op, 2,
                              pp.opAssoc.LEFT,
                              combiner.parser_callback),
                             (add_op, 2,
                              pp.opAssoc.LEFT,
                              combiner.parser_callback),
                            ])

MATH_PARSER = make_math_parser()

def parse_dice_str(dice_str):
    """Perform normal dice parsing operations:
        *
    """
    print(f"Raw roll request: {dice_str}") # TODO (jjh): convert to logging

    try:
        roll_obj = MATH_PARSER.parseString(dice_str)[0]

    except pp.ParseException as ex:
        bstr, idx, error = ex.args
        underline_error = f"{bstr[:idx]}__{bstr[idx]}__{bstr[idx+1:]}"
        return f"Huh?  This looks wrong: {underline_error} [{error}]", None

    roll_str, roll_val = str(roll_obj), int(roll_obj)
    for emoji_name in DICE_EMOJI:
        if emoji_name in roll_str:
            roll_str = roll_str.replace(emoji_name,
                                        DICE_EMOJI[emoji_name])
    return roll_str, roll_val
