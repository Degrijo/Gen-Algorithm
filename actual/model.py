import itertools
from random import randint
from abc import ABC

from constants import MIN_VALUE, MAX_VALUE


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
    def bottom(self):
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
    obj_counter = 0

    def __init__(self):
        self.square = None
        Beast.obj_counter += 1
        self.id = self.obj_counter
        self.race = ''

    def move_top(self):
        top = self.square.top
        if top:
            self.square = top

    def move_bottom(self):
        bottom = self.square.bottom
        if bottom:
            self.square = bottom

    def move_left(self):
        left = self.square.left
        if left:
            self.square = left

    def move_right(self):
        right = self.square.right
        if right:
            self.square = right

    @property
    def draw_inf(self):
        return self.square.x, self.square.y, self.race, 'beast_' + str(self.id)


class Cockroach(Beast):
    def __init__(self):
        super().__init__()
        self.race = Cockroach.__name__
        self.vitamins = MIN_VALUE
        self.fruits = MIN_VALUE

    @property
    def is_alive(self):
        return not (self.vitamins < MIN_VALUE or self.fruits < MIN_VALUE)


class Snowflake(Beast):
    def __init__(self):
        super().__init__()
        self.race = Snowflake.__name__
        self.meat = MIN_VALUE
        self.fruits = MIN_VALUE

    @property
    def is_alive(self):
        return not (self.meat < MIN_VALUE or self.fruits < MIN_VALUE)


class Washcloth(Beast):
    def __init__(self):
        super().__init__()
        self.race = Washcloth.__name__
        self.meat = MIN_VALUE
        self.vitamins = MIN_VALUE

    @property
    def is_alive(self):
        return not (self.meat < MIN_VALUE or self.vitamins < MIN_VALUE)


BEAST_TYPES = (Cockroach, Snowflake, Washcloth)
