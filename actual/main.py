from threading import Thread

from view import View
from controller import Controller


if __name__ == '__main__':
    view = View()
    controller = Controller(view)
    view.set_controller(controller)
    thread = Thread(target=controller)
    thread.start()
    view.display()
