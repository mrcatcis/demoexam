from PyQt5.Qt  import QPushButton, QPointF
from PyQt5.QtGui import QColor, QPainter, QPolygonF
from math import sin, cos, pi

class Button(QPushButton):
    # Данный метод принимает следующие параметры:
    # radius - радиус описанной окружности кнопки
    # angles - количество углов кнопки 3, 4 или 5
    # Инициализирует кнопку
    # Ничего не возвращает
    def __init__(self, parent, angles, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.angles = angles
        self.chosen = False

    # Данный метод принимает следующие параметры:
    # radius - радиус описанной окружности кнопки
    # angles - количество углов кнопки 3, 4 или 5
    # создаёт QPolygonF
    # возвращает его 
    def create_polygon(self, radius, angles):
        if angles == 3:
            rotation = pi/6
        elif angles == 4:
            rotation = pi/4
        elif angles == 5:
            rotation = 3*pi/2
        else:
            raise('wrong count angles')
        polygon = QPolygonF()
        alpha = 2*pi/angles
        for i in range(angles):
            d = alpha * i + rotation
            x = radius * cos(d)
            y = radius * sin(d)
            polygon.append(QPointF(self.width()/2+x, self.height()/2+y))
        return polygon

    def paintEvent(self, event):
        super(Button, self).paintEvent(event)
        qp = QPainter()
        qp.begin(self)
        qp.setPen(QColor(255, 0, 0))
        if self.chosen:
            qp.setBrush(QColor(255, 0, 0))
        else:
            qp.setBrush(QColor(255, 255, 255))
        qp.drawPolygon(self.create_polygon(self.width()/2,
                                           self.angles))
        qp.end()