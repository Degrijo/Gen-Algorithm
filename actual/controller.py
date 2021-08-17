from random import shuffle, choice
from time import sleep

from constants import ROW_NUMBER, COL_NUMBER, STEP_DELAY, BEAST_NUMBER, EVEN_DISTRIBUTION, ACTION_DELAY
from model import Card, BEAST_TYPES

# kill beast right now, delay before death, instant pause

RUN = 0
PAUSE = 1
STOP = 2


class Controller:
    def __init__(self, view):
        self.view = view
        self.beasts = []
        self.run = RUN
        self.card = Card(ROW_NUMBER, COL_NUMBER)

    def create_beasts(self):
        if EVEN_DISTRIBUTION:
            beast_amount = len(BEAST_TYPES)
            common = BEAST_NUMBER // beast_amount
            for beast_type in BEAST_TYPES:
                for _ in range(common):
                    beast = beast_type()
                    self.create_beast(beast)
            for _ in range(BEAST_NUMBER - common * beast_amount):
                beast = choice(BEAST_TYPES)()
                self.create_beast(beast)
        else:
            for _ in range(BEAST_NUMBER):
                beast = choice(BEAST_TYPES)()
                self.create_beast(beast)

    def create_beast(self, beast):
        self.beasts.append(beast)
        self.card.random_place_beast(beast)
        self.view.field.draw_image(*beast.draw_inf)

    def custom_create_beast(self, beast, x, y):
        if self.card.manual_place_beast(beast, x, y):
            self.beasts.append(beast)
            self.view.field.draw_image(*beast.draw_inf)

    def move_top(self, beast):
        if beast.move_top():
            self.view.field.move_right(beast.id)

    def move_bottom(self, beast):
        if beast.move_bottom():
            self.view.field.move_bottom(beast.id)

    def move_left(self, beast):
        if beast.move_left():
            self.view.field.move_left(beast.id)

    def move_right(self, beast):
        if beast.move_right():
            self.view.field.move_right(beast.id)

    def attack_top(self, beast):
        if beast.attack_top():
            self.view.field.attack_top(beast.id)
            if not beast.is_alive:
                self.suicide(beast)

    def attack_bottom(self, beast):
        if beast.attack_bottom():
            self.view.field.attack_bottom(beast.id)
            if not beast.is_alive:
                self.suicide(beast)

    def attack_left(self, beast):
        if beast.attack_left():
            self.view.field.attack_left(beast.id)
            if not beast.is_alive:
                self.suicide(beast)

    def attack_right(self, beast):
        if beast.attack_right():
            self.view.field.attack_right(beast.id)
            if not beast.is_alive:
                self.suicide(beast)

    def run_pause(self, event=None):
        self.run = RUN if self.run == PAUSE else PAUSE

    def stop(self, event=None):
        self.run = STOP
        self.view.destroy()

    def suicide(self, beast):
        self.beasts.remove(beast)
        beast.suicide()
        self.view.field.delete_image(beast.id)

    def aging(self, beast):
        beast.aging()
        if not beast.is_alive:
            self.suicide(beast)

    def __call__(self, *args, **kwargs):
        self.create_beasts()
        self.custom_create_beast(BEAST_TYPES[0](), 2, 3)
        self.custom_create_beast(BEAST_TYPES[1](), 2, 4)
        while True:
            sleep(STEP_DELAY)
            if self.run == RUN:
                shuffle(self.beasts)
                for beast in self.beasts:
                    sleep(ACTION_DELAY)
                    sq = beast.square.right
                    if sq:
                        if not sq.is_empty and beast.race != sq.beast.race:
                            self.attack_right(beast)
                        else:
                            self.move_right(beast)
            elif self.run == STOP:
                break
