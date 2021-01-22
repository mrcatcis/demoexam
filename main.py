from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint
from math import pi, sin, cos


class Window(QWidget):
    class Polygon():
        def __init__(self, n, pos, size):
            self.n = n
            self.pos = pos
            self.size = size
            self.polygon = self.createPolygon(n, pos, size)

        def createPolygon(self, n: int, pos: QPoint, size: int):
            polygon = []
            delt = 2 * pi / n
            for i in range(n):
                i *= delt
                polygon.append(QPoint(pos.x() + int(sin(i) * size),
                                      pos.y() + int(cos(i) * size)))
            return QPolygon(polygon)

        def addAngle(self):
            self.n += 1
            self.polygon = self.createPolygon(self.n, self.pos, self.size)

    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 800, 600)
        self.setWindowTitle('5.2')
        self.show()

        self.polygons = []

    def deleteTriangles(self):
        self.polygons.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteTriangles()
            self.update()

    def findPolygon(self, pos):
        for i in range(len(self.polygons)):
            if self.polygons[i].polygon.containsPoint(pos, Qt.OddEvenFill):
                return i
        return -1

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        index = self.findPolygon(QPoint(x, y))
        if index == -1:
            self.polygons.append(self.Polygon(3, QPoint(x, y), 50))
        else:
            self.polygons[index].addAngle()

        self.update()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        self.drawPolygons()
        self.painter.end()

    def drawPolygons(self):
        for polygon in self.polygons:
            self.painter.drawPolygon(polygon.polygon)


if __name__ == '__main__':
    app = QApplication([])
    root = Window()
    app.exec_()
