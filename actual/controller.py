import sys
from random import shuffle, choice
from time import sleep

from constants import ROW_NUMBER, COL_NUMBER, DELAY_TIME, BEAST_NUMBER, EVEN_DISTRIBUTION
from model import Card, BEAST_TYPES


RUN = 0
PAUSE = 1
STOP = 2


def death_check(beast):
    if beast.is_alive:
        return True
    beast.square.beasts.remove(beast)
    del beast
    return False


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
        self.card.place_beast(beast)
        self.view.field.draw_image(*beast.draw_inf)
        sq = beast.square
        print(beast.id, sq.x, sq.y)

    def move_top(self, beast):
        beast.move_top()
        self.view.field.move_right('beast_' + str(beast.id))

    def move_bottom(self, beast):
        beast.move_bottom()
        self.view.field.move_bottom('beast_' + str(beast.id))

    def move_left(self, beast):
        beast.move_left()
        self.view.field.move_left('beast_' + str(beast.id))

    def move_right(self, beast):
        beast.move_right()
        self.view.field.move_right('beast_' + str(beast.id))

    def run_pause(self, event=None):
        self.run = RUN if self.run == PAUSE else PAUSE

    def stop(self, event=None):
        self.run = STOP
        self.view.destroy()

    def __call__(self, *args, **kwargs):
        self.create_beasts()
        while True:
            sleep(DELAY_TIME)
            if self.run == RUN:
                # shuffle(self.beasts)
                for beast in self.beasts:
                    self.move_right(beast)
                    sq = beast.square
                    print(beast.id, sq.x, sq.y)
                self.beasts = [beast for beast in self.beasts if death_check(beast)]  # killing beasts
            elif self.run == STOP:
                break
