from random import shuffle, choice
from time import sleep

from constants import ROW_NUMBER, COL_NUMBER, DELAY_TIME, BEAST_NUMBER, EVEN_DISTRIBUTION
from model import Card, BEAST_TYPES


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
        self.card = Card(ROW_NUMBER, COL_NUMBER)

    def create_beasts(self):
        if EVEN_DISTRIBUTION:
            beast_amount = len(BEAST_TYPES)
            common = BEAST_NUMBER // beast_amount
            for beast_type in BEAST_TYPES:
                for _ in range(common):
                    beast = beast_type()
                    self.beasts.append(beast)
                    self.card.place_beast(beast)
            for _ in range(BEAST_NUMBER - common * beast_amount):
                beast = choice(BEAST_TYPES)()
                self.beasts.append(beast)
                self.card.place_beast(beast)
        else:
            for _ in range(BEAST_NUMBER):
                beast = choice(BEAST_TYPES)()
                self.beasts.append(beast)
                self.card.place_beast(beast)

    def redraw_beasts(self):
        for beast in self.beasts:
            self.view.update()

    def __call__(self, *args, **kwargs):
        self.create_beasts()
        self.view.update()
        while True:
            sleep(DELAY_TIME)
            shuffle(self.beasts)

            self.beasts = [beast for beast in self.beasts if death_check(beast)]  # killing beasts
            self.view.update()  # updating ui
