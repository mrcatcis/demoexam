from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint
from math import pi, sin, cos

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 800, 600)
        self.setWindowTitle('5.1')
        self.show()
        self.polygons = []

    def deletePolygons(self):
        self.polygons.clear()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deleteTriangles()
            self.update()

    def createPolygon(self, n: int, pos: QPoint, size: int):
        polygon = []
        delt = 2 * pi / n
        for i in range(n):
            i *= delt
            polygon.append(QPoint(pos.x() + int(sin(i) * size),
                                  pos.y() + int(cos(i) * size)))
        return QPolygon(polygon)

    def drawPolygons(self):
        for i in self.polygons:
            self.painter.drawPolygon(i)

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        self.polygons.append(self.createPolygon(3, QPoint(x, y), 50))
        self.update()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        self.drawPolygons()
        self.painter.end()


if __name__ == '__main__':
    app = QApplication([])
    root = Window()
    app.exec_()
