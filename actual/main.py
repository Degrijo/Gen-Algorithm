from threading import Thread

from view import View
from controller import Controller


if __name__ == '__main__':
    view = View()
    logic = Thread(target=Controller(view))
    view.display()
    logic.start()
