from PyQt5 import QtWidgets, QtGui, QtCore


class CreatureItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, parent, sqr_view, pen, pixmap, pixmap_menu):
        super().__init__(pixmap)
        self.pixmap_menu = pixmap_menu
        self.setAcceptHoverEvents(True)
        self.active = False
        self.pen = pen
        self.sqr_view = sqr_view
        self.parent = parent
        self.text = parent.get_hero_inf()  # добавить отображение шкалы ресурсов

    def hoverEnterEvent(self, event):
        self.active = True
        self.setZValue(self.zValue() + 1)
        QtWidgets.QGraphicsItem.hoverEnterEvent(self, event)

    def hoverLeaveEvent(self, event):
        self.active = False
        self.setZValue(self.zValue() - 1)
        QtWidgets.QGraphicsItem.hoverLeaveEvent(self, event)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(self.offset().x(), self.offset().y(), self.pixmap())
        if self.active:
            if self.offset().x() <= 920:
                painter.drawPixmap(1880 - self.pixmap_menu.width(), 960 - self.pixmap_menu.height(), self.pixmap_menu)
                painter.setPen(QtGui.QColor(0, 0, 0))
                painter.setFont(QtGui.QFont('Decorative', 10))
                painter.drawText(QtCore.QRect(1880 - self.pixmap_menu.width(), 960 - self.pixmap_menu.height(),
                                              self.pixmap_menu.width(), self.pixmap_menu.height()),
                                 QtCore.Qt.AlignLeft, self.text)
                if self.parent.plan:
                    painter.setFont(QtGui.QFont('Decorative', 12))
                    painter.drawText(QtCore.QRect(1880 - self.pixmap_menu.width(), 940,
                                                  self.pixmap_menu.width(), 20),
                                     QtCore.Qt.AlignLeft, self.parent.plan[0] + ' on ' + str(self.parent.plan[1]))
            else:
                painter.drawPixmap(0, 960 - self.pixmap_menu.height(), self.pixmap_menu)
                painter.setPen(QtGui.QColor(0, 0, 0))
                painter.setFont(QtGui.QFont('Decorative', 10))
                painter.drawText(QtCore.QRect(0, 960 - self.pixmap_menu.height(),
                                              self.pixmap_menu.width(), self.pixmap_menu.height()),
                                 QtCore.Qt.AlignLeft, self.text)
                if self.parent.plan:
                    painter.setFont(QtGui.QFont('Decorative', 12))
                    painter.drawText(QtCore.QRect(0, 940,
                                                  self.pixmap_menu.width(), 20),
                                     QtCore.Qt.AlignLeft, self.parent.plan[0] + ' on ' + str(self.parent.plan[1]))
            painter.setPen(self.pen)
            painter.drawRect(self.offset().x() - self.sqr_view, self.offset().y() - self.sqr_view,
                             self.sqr_view * 2 + self.pixmap().width(), self.sqr_view * 2 + self.pixmap().height())
