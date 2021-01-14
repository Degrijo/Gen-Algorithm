from random import randint
from abc import ABC

from constants import COCKROACH_PICT, SNOWFLAKE_PICT, WASHCLOTH_PICT, MIN_VALUE, MAX_VALUE


class Card:
    def __init__(self, row_number, col_number):
        self.row_number = row_number
        self.col_number = col_number
        self.matrix = [[Square(self, i, j) for j in range(col_number)] for i in range(row_number)]

    def __getitem__(self, coors):
        x, y = coors[0:2]
        if 0 <= x < self.row_number and 0 <= y < self.col_number:
            return self.matrix[x][y]

    def place_beast(self, beast):
        while True:
            x = randint(0, self.row_number - 1)
            y = randint(0, self.col_number - 1)
            square = self.matrix[x][y]
            if square.is_empty:
                square.beasts.append(beast)
                beast.square = square
                break


class Square:
    def __init__(self, card, x, y):
        self.card = card
        self.x = x
        self.y = y
        self.beasts = []

    @property
    def top(self):
        return self.card[self.x - 1, self.y]

    @property
    def bot(self):
        return self.card[self.x + 1, self.y]

    @property
    def left(self):
        return self.card[self.x, self.y - 1]

    @property
    def right(self):
        return self.card[self.x, self.y + 1]

    @property
    def is_empty(self):
        return not bool(self.beasts)


class Beast(ABC):
    def __init__(self):
        self.square = None

    def move_top(self):
        top = self.square.top
        if top:
            self.square = top

    def move_bot(self):
        bot = self.square.bot
        if bot:
            self.square = bot

    def move_left(self):
        left = self.square.left
        if left:
            self.square = left

    def move_right(self):
        right = self.square.right
        if right:
            self.square = right


class Cockroach(Beast):
    def __init__(self):
        super().__init__()
        self.pict = COCKROACH_PICT
        self.vitamins = MIN_VALUE
        self.fruits = MIN_VALUE

    @property
    def is_alive(self):
        return not (self.vitamins < MIN_VALUE or self.fruits < MIN_VALUE)


class Snowflake(Beast):
    def __init__(self):
        super().__init__()
        self.pict = SNOWFLAKE_PICT
        self.meat = MIN_VALUE
        self.fruits = MIN_VALUE

    @property
    def is_alive(self):
        return not (self.meat < MIN_VALUE or self.fruits < MIN_VALUE)


class Washcloth(Beast):
    def __init__(self):
        super().__init__()
        self.pict = WASHCLOTH_PICT
        self.meat = MIN_VALUE
        self.vitamins = MIN_VALUE

    @property
    def is_alive(self):
        return not (self.meat < MIN_VALUE or self.vitamins < MIN_VALUE)


BEAST_TYPES = (Cockroach, Snowflake, Washcloth)
