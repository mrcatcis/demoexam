from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QColor, QFont, QPen, QBrush, QPolygon
from PyQt5.QtCore import Qt, QPoint
import math


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 200, 800, 600)
        self.setWindowTitle('TestQT')
        self.show()
        self.polygons = []

    def delete_triangles(self):
        self.polygons.clear()

    def keyPressEvent(self, event):
        if event().key() == Qt.Key_Delete:
            self.delete_triangles()
            self.update()

    def create_polygon(self, n: int, pos: QPoint, size: int):
        polygon = []
        delt = 2 * math.pi / n
        for i in range(n):
            i *= delt
            polygon.append(QPoint(pos.x() + int(math.sin(i) * size),
                                  pos.y() + int(math.cos(i) * size)))
        return QPolygon(polygon)

    def draw_polygons(self):
        for i in self.polygons:
            self.painter.drawPolygon(i)

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        self.polygons.append(self.create_polygon(5, QPoint(x, y), 30))
        self.update()

    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        self.draw_polygons()
        self.painter.end()


app = QApplication([])
root = Window()
app.exec_()
