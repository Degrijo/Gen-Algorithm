from random import randint
from abc import ABC

from constants import MIN_VALUE, START_VALUE, MAX_VALUE, START_DAMAGE, START_DEFENCE, START_VAMPIRISM, AGING_RESOURCE, \
    AGING_HP
# hp instead of resources

PARAMS = {'hp': {'percent': False}, 'damage_min': {'percent': False}, 'vampirism': {'percent': True},
          'damage_max': {'percent': False, 'gte': 'damage_min'}, 'defence': {'percent': False},
          'vitamins': {'percent': False}, 'fruits': {'percent': False}, 'meat': {'percent': False}}


class Card:
    def __init__(self, row_number, col_number):
        self.row_number = row_number
        self.col_number = col_number
        self.matrix = [[Square(self, i, j) for j in range(col_number)] for i in range(row_number)]

    def __getitem__(self, coors):
        row, col = coors[0:2]
        if 0 <= row < self.row_number and 0 <= col < self.col_number:
            return self.matrix[row][col]

    def random_place_beast(self, beast):
        while True:
            row = randint(0, self.row_number - 1)
            col = randint(0, self.col_number - 1)
            square = self.matrix[row][col]
            if square.is_empty:
                square.add_beast(beast)
                beast.square = square
                break

    def manual_place_beast(self, beast, row, col):
        square = self.matrix[row][col]
        if square and square.is_empty:
            square.add_beast(beast)
            beast.square = square
            return True
        return False


class Square:
    def __init__(self, card, row, col):
        self.card = card
        self.row = row
        self.col = col
        self.beast = None

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
        return not bool(self.beast)

    def remove_beast(self):
        self.beast = None

    def add_beast(self, beast):
        self.beast = beast


class Beast(ABC):
    obj_counter = 0
    square = None
    race = ''
    features = ()
    loot = ''

    def __init__(self, gens):
        Beast.obj_counter += 1
        self.id = Beast.__name__ + str(self.obj_counter)
        if gens:
            self.special_skills = {skill: gens.pop(skill) for skill in self.features}
            self.skills = gens
        else:
            self.special_skills = {skill: MAX_VALUE for skill in self.features}
            self.skills = {'hp': MAX_VALUE, 'damage_min': START_DAMAGE, 'damage_max': START_DAMAGE,
                           'defence': START_DEFENCE, 'vampirism': START_VAMPIRISM}
        self.special_resources = {res: START_VALUE * self.special_skills[res] for res in self.features}
        self.resources = {'hp': self.skills['hp']}

    def move_top(self):
        top = self.square.top
        if top and top.is_empty:
            self.square.remove_beast()
            self.square = top
            self.square.add_beast(self)
            return True
        return False

    def move_bottom(self):
        bottom = self.square.bottom
        if bottom and bottom.is_empty:
            self.square.remove_beast()
            self.square = bottom
            self.square.add_beast(self)
            return True
        return False

    def move_left(self):
        left = self.square.left
        if left and left.is_empty:
            self.square.remove_beast()
            self.square = left
            self.square.add_beast(self)
            return True
        return False

    def move_right(self):
        right = self.square.right
        if right and right.is_empty:
            self.square.remove_beast()
            self.square = right
            self.square.add_beast(self)
            return True
        return False

    def _attack(self, enemy):
        damage = randint(self.skills['damage_min'], self.skills['damage_min'])
        total_damage = self._defence(damage)
        self.update_special_rec(enemy.loot, total_damage * self.skills['vampirism'] // 100)

    def _defence(self, damage):
        with_defence = damage - self.skills['defence']
        if with_defence > 0:
            hp = self.resources['hp']
            self.update_res('hp', -with_defence)
            if hp < with_defence:
                return self.resources['hp']
            else:
                return with_defence
        return 0

    def attack_top(self):
        top = self.square.top
        if top and not top.is_empty and self.race != top.beast.race:
            self._attack(top.beast)
            return True
        return False

    def attack_bottom(self):
        bottom = self.square.bottom
        if bottom and not bottom.is_empty and self.race != bottom.beast.race:
            self._attack(bottom.beast)
            return True
        return False

    def attack_left(self):
        left = self.square.left
        if left and not left.is_empty and self.race != left.beast.race:
            self._attack(left.beast)
            return True
        return False

    def attack_right(self):
        right = self.square.right
        if right and not right.is_empty and self.race != right.beast.race:
            self._attack(right.beast)
            return True
        return False

    def aging(self):
        for key in self.features:
            self.update_special_rec(key, -AGING_RESOURCE)
            if not self.special_resources[key]:
                self.update_res('hp', AGING_HP)

    def suicide(self):
        self.square.remove_beast()

    def update_res(self, res, value):
        if self.resources[res] + value > self.skills[res]:
            self.resources[res] = self.skills[res]
        elif self.resources[res] + value < 0:
            self.resources[res] = 0
        else:
            self.resources[res] += value

    def update_special_rec(self, res, value):
        if self.special_resources[res] + value > self.special_skills[res]:
            self.special_resources[res] = self.special_skills[res]
        elif self.special_resources[res] + value < 0:
            self.special_resources[res] = 0
        else:
            self.special_resources[res] += value

    @property
    def draw_inf(self):
        return self.square.col, self.square.row, self.race, self.id

    @property
    def is_alive(self):
        return bool(self.resources['hp'])


class Cockroach(Beast):
    features = ('vitamins', 'fruits')
    loot = 'meat'

    def __init__(self, gens=None):
        super().__init__(gens)
        self.race = Cockroach.__name__


class Snowflake(Beast):
    features = ('meat', 'fruits')
    loot = 'vitamins'

    def __init__(self, gens=None):
        super().__init__(gens)
        self.race = Snowflake.__name__


class Washcloth(Beast):
    features = ('vitamins', 'meat')
    loot = 'fruits'

    def __init__(self, gens=None):
        super().__init__(gens)
        self.race = Washcloth.__name__


BEAST_TYPES = (Cockroach, Snowflake, Washcloth)
