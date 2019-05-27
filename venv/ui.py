from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from models import Cockroach, Snowflake, Washcloth
from random import randint, choice
from time import sleep

win_size = QtCore.QRect(0, 0, 1920, 1010)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_logic()

    def init_ui(self):
        self.setGeometry(win_size)
        self.setWindowTitle("Bots' Amplitude")
        self.setWindowIcon(QtGui.QIcon(r"../pict/icon.png"))
        self.setWindowState(QtCore.Qt.WindowMaximized)  # везде проверить и сделать правильно карту
        self.scene = QtWidgets.QGraphicsScene(self.rect().x(), self.rect().y(), self.rect().width() - 40,
                                              self.rect().height() - 50)
        self.sqr_width = 40
        for i in range(0, int(self.scene.sceneRect().height()) + 1, self.sqr_width):
            item = QtWidgets.QGraphicsLineItem(round(self.scene.sceneRect().x()), i,
                                               round(self.scene.sceneRect().x() + self.scene.sceneRect().width()),
                                               i + 1)
            pen = QtGui.QPen(QtGui.QColor(130, 0, 0))
            pen.setStyle(QtCore.Qt.DashDotLine)
            item.setPen(pen)
            self.scene.addItem(item)
        for i in range(0, int(self.scene.sceneRect().width()) + 1, self.sqr_width):
            item = QtWidgets.QGraphicsLineItem(i, int(self.scene.sceneRect().y()), i + 1,
                                               int(self.scene.sceneRect().y() + self.scene.sceneRect().height()))
            pen = QtGui.QPen(QtGui.QColor(130, 0, 0))
            pen.setStyle(QtCore.Qt.DashDotLine)
            item.setPen(pen)
            self.scene.addItem(item)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHints(QtGui.QPainter.Antialiasing |
                                 QtGui.QPainter.HighQualityAntialiasing)
        self.view.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)
        self.view.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(222, 192, 216)))
        self.setCentralWidget(self.view)
        self.show()

    def init_logic(self):
        self.map = [['-' for j in range(0, int(self.scene.sceneRect().height()), self.sqr_width)]
                    for i in range(0, int(self.scene.sceneRect().width()), self.sqr_width)]
        self.sqr_view = 4
        self.creatures = []
        self.add_creature('Cockroach', 8, 5, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 9, 5, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 7, 6, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 8, 6, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 9, 6, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 7, 7, MainWindow.gen_features('Cockroach'))
        self.add_creature('Cockroach', 8, 7, MainWindow.gen_features('Cockroach'))
        self.add_creature('Snowflake', 42, 10, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 43, 10, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 42, 11, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 43, 11, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 44, 11, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 43, 12, MainWindow.gen_features('Snowflake'))
        self.add_creature('Snowflake', 44, 12, MainWindow.gen_features('Snowflake'))
        self.add_creature('Washcloth', 25, 19, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 24, 20, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 25, 20, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 26, 20, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 24, 21, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 25, 21, MainWindow.gen_features('Washcloth'))
        self.add_creature('Washcloth', 26, 21, MainWindow.gen_features('Washcloth'))
        self.gen_water()
        self.game = True
        self.start()

    def del_creature(self, creature):
        self.scene.remove(creature.item)
        self.map[creature.x][creature.y] = '-'
        self.creatures.remove(creature)

    def shuffle(self):
        def swap(creatures, i, j):
            creatures[i], creatures[j] = creatures[j], creatures[i]
        for _ in range(len(self.creatures) // 3):
            swap(self.creatures, randint(0, len(self.creatures) - 1), randint(0, len(self.creatures) - 1))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.game = not self.game

    def start(self):
        while self.game:
            self.shuffle()
            for cr in self.creatures:
                cr.turn()
            sleep(3)

    def add_creature(self, type, x, y, gene, gen_number=1):
        if type == 'Cockroach':
            obj = Cockroach(x, y, gene, gen_number, self)
        elif type == 'Snowflake':
            obj = Snowflake(x, y, gene, gen_number, self)
        else:
            obj = Washcloth(x, y, gene, gen_number, self)
        if self.map[x][y] is not '-':
            del obj
        else:
            self.map[x][y] = obj
            self.creatures.append(obj)
            self.scene.addItem(obj.item)

    def apocalepse(self):
        for _ in range(len(self.creatures)//2):
            self.del_creature(choice(self.creatures))

    @staticmethod
    def gen_features(type):
        gene = {"attack": {"-x": randint(8, 12) * 10, "+x": randint(8, 12) * 10,
                           "+y": randint(8, 12) * 10, "-y": randint(8, 12) * 10},
                "defense": {"-x": randint(0, 4) * 10, "+x": randint(0, 4) * 10,
                            "+y": randint(0, 4) * 10, "-y": randint(0, 4) * 10},
                "capacity": {"hp": randint(7, 14) * 100, "water": randint(7, 14) * 100}}
        if type == 'Cockroach':
            gene["capacity"]["vitamin"] = randint(7, 14) * 100
            gene["capacity"]["plant"] = randint(7, 14) * 100
        elif type == 'Snowflake':
            gene["capacity"]["meat"] = randint(7, 14) * 100
            gene["capacity"]["plant"] = randint(7, 14) * 100
        else:
            gene["capacity"]["vitamin"] = randint(7, 14) * 100
            gene["capacity"]["meat"] = randint(7, 14) * 100
        return gene

    def gen_water(self):
        for _ in range(30):
            i = randint(0, len(self.map) - 1)
            j = randint(0, len(self.map[i]) - 1)
            if self.map[i][j] == '-':
                self.map[i][j] = 'w'
                number = randint(1, 3)
                item = QtWidgets.QGraphicsPixmapItem(QtGui.QPixmap(r"..\pict\water{}.png".format(number)))
                item.setOffset(i * self.sqr_width, j * self.sqr_width)
                self.scene.addItem(item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
