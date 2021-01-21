from random import shuffle, choice
from time import sleep

from constants import ROW_NUMBER, COL_NUMBER, STEP_DELAY, BEAST_NUMBER, EVEN_DISTRIBUTION, VISIBLE_SQUARE_NUMBER
from model import Card, BEAST_TYPES


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
        self.card.place_beast(beast)
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

    def run_pause(self, event=None):
        self.run = RUN if self.run == PAUSE else PAUSE

    def stop(self, event=None):
        self.run = STOP
        self.view.destroy()

    def kill_beast(self, beast):
        if beast.is_alive:
            return True
        beast.square.beasts.remove(beast)
        self.view.field.delete_image(beast.id)
        del beast
        return False

    def __call__(self, *args, **kwargs):
        self.create_beasts()
        while True:
            sleep(STEP_DELAY)
            if self.run == RUN:
                shuffle(self.beasts)
                for beast in self.beasts:
                    self.move_right(beast)
                    sq = beast.square
                self.beasts = [beast for beast in self.beasts if self.kill_beast(beast)]
            elif self.run == STOP:
                break
