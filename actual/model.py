from random import randint
from abc import ABC

from constants import MIN_VALUE, START_VALUE, MAX_VALUE


class Card:
    def __init__(self, row_number, col_number):
        self.row_number = row_number
        self.col_number = col_number
        self.matrix = [[Square(self, i, j) for j in range(col_number)] for i in range(row_number)]

    def __getitem__(self, coors):
        row, col = coors[0:2]
        if 0 <= row < self.row_number and 0 <= col < self.col_number:
            return self.matrix[row][col]

    def place_beast(self, beast):
        while True:
            row = randint(0, self.row_number - 1)
            col = randint(0, self.col_number - 1)
            square = self.matrix[row][col]
            if square.is_empty:
                square.beasts.append(beast)
                beast.square = square
                break


class Square:
    def __init__(self, card, row, col):
        self.card = card
        self.row = row
        self.col = col
        self.beasts = []

    @property
    def top(self):
        return self.card[self.row - 1, self.col]

    @property
    def bottom(self):
        return self.card[self.row + 1, self.col]

    @property
    def left(self):
        return self.card[self.row, self.col - 1]

    @property
    def right(self):
        return self.card[self.row, self.col + 1]

    @property
    def is_empty(self):
        return not bool(self.beasts)

    def cell_value(self):
        return


class Beast(ABC):
    obj_counter = 0

    def __init__(self):
        self.square = None
        Beast.obj_counter += 1
        self.id = Beast.__name__ + str(self.obj_counter)
        self.race = ''
        self.resources = {}

    def move_top(self):
        top = self.square.top
        if top and top.is_empty:
            self.square.beasts.remove(self)
            self.square = top
            self.square.beasts.append(self)
            return True
        return False

    def move_bottom(self):
        bottom = self.square.bottom
        if bottom and bottom.is_empty:
            self.square.beasts.remove(self)
            self.square = bottom
            self.square.beasts.append(self)
            return True
        return False

    def move_left(self):
        left = self.square.left
        if left and left.is_empty:
            self.square.beasts.remove(self)
            self.square = left
            self.square.beasts.append(self)
            return True
        return False

    def move_right(self):
        right = self.square.right
        if right and right.is_empty:
            self.square.beasts.remove(self)
            self.square = right
            self.square.beasts.append(self)
            return True
        return False

    @property
    def draw_inf(self):
        return self.square.col, self.square.row, self.race, self.id

    @property
    def is_alive(self):
        return not filter(lambda res: res < MIN_VALUE, self.resources.values())

    @property
    def relative_resources(self):
        return {key: 1 - value / MAX_VALUE for key, value in self.resources.items()}


class Cockroach(Beast):
    def __init__(self):
        super().__init__()
        self.race = Cockroach.__name__
        self.resources = {res: START_VALUE for res in ('vitamins', 'fruits')}


class Snowflake(Beast):
    def __init__(self):
        super().__init__()
        self.race = Snowflake.__name__
        self.resources = {res: START_VALUE for res in ('meat', 'fruits')}


class Washcloth(Beast):
    def __init__(self):
        super().__init__()
        self.race = Washcloth.__name__
        self.resources = {res: START_VALUE for res in ('vitamins', 'meat')}


BEAST_TYPES = (Cockroach, Snowflake, Washcloth)
