"""Dice Expression parsers functions

Leans heavily on pyparsing functionality (and dataclasses... because reasons)

"""

import operator
import copy
import dataclasses
import random

import pyparsing as pp


@dataclasses.dataclass
class DiceRoll:

    rand: random.Random = dataclasses.field(default_factory=random.Random)
    format_str: str = "[{num_dice}:d{sides}:-->**{value}**]"

    num_dice: int = None
    num_sides: int = None

    roll: int = dataclasses.field(init=False)

    def parser_callback(self, tokens):
        print("DiceRoll callback", tokens)
        # copy (not deepcopy) sufficient: all distinct values are immutable
        new_dice_roll = copy.copy(self)

        # Num dice is optional: if not present, assume 1
        if len(tokens) == 1:
            new_dice_roll.num_dice = 1
            new_dice_roll.num_sides = int(tokens[0])
        else:
            new_dice_roll.num_dice = int(tokens[0])
            new_dice_roll.num_sides = int(tokens[1])

        roll = sum([new_dice_roll.rand.randint(1, new_dice_roll.num_sides)
                    for _ in range(new_dice_roll.num_dice)])
        new_dice_roll.roll = roll

        return new_dice_roll

    def __str__(self):

        return self.format_str.format(num_dice=self.num_dice,
                                      sides=self.num_sides,
                                      value=self.roll)

    def __int__(self):
        return self.roll


OP_MAP = {'-' : operator.sub,
          '+' : operator.add,
          '*' : operator.mul,
          '/' : operator.floordiv}

@dataclasses.dataclass
class CombineOp:
    """Combination operation

    Format string values except:
        * 'op1': string of first operand
        * 'op2': string of second operad
        * 'operator': string of operator
        * 'value': integer value of expression
    """

    format_str: str = "({op1} {operator} {op2})"

    op1: int = None
    op2: int = None
    operator: str = None

    def parser_callback(self, tokens):
        tokens = tokens[0] # pull off parsed values from infix tuple
        print("Combine callback", tokens)
        new_combine = copy.copy(self)
        new_combine.op1, new_combine.operator, new_combine.op2 = tokens[:3]
        if len(tokens[3:]):
            new_combine = new_combine.parser_callback([[new_combine] +
                                                       tokens[3:]])
        return new_combine

    def __str__(self):
        # TODO (jjh): Handle sign inversions if a signed object comes in
        # if (isinstance(self.op2, SignOp) and
        #     self.op2.sign !=

        return self.format_str.format(op1=self.op1,
                                      op2=self.op2,
                                      operator=self.operator,
                                      value=int(self))

    def __int__(self):
        return OP_MAP[self.operator](int(self.op1),
                                     int(self.op2))


@dataclasses.dataclass
class SignOp:

    format_str: str = "{sign}{op1}"

    op1: int = None
    sign: str = None

    def parser_callback(self, tokens):
        print("SignOp callback", tokens)
        new_sign = copy.copy(self)
        new_sign.sign, new_sign.op1 = tokens[0]
        return new_sign

    def __str__(self):
        return self.format_str.format(op1=self.op1,
                                      sign=self.sign,
                                      value=int(self))

    def __int__(self):
        val = int(self.op1)
        if self.sign == '-':
            val = operator.neg(val)
        return val
