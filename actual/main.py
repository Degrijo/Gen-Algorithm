from threading import Thread

from view import View
from controller import Controller


if __name__ == '__main__':
    view = View()
    view.display()
    # logic = Thread(target=Controller(view))
    # logic.start()
