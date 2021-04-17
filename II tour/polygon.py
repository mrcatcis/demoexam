from math import sin, cos, pi
from PyQt5.Qt import QPointF
from PyQt5.QtGui import QPolygonF
class Polygon():
    # Данный метод принимает следующие параметры:
    # radius - радиус описанной окружности многоугольника
    # angles - количество углов многоугольника 3, 4 или 5
    # pos - кордината центра многоугольника
    # Инициализирует многоугольник
    # Ничего не возвращает
    def __init__(self, radius, angles, pos):
        self.radius = radius
        self.angles = angles
        self.pos = pos
        self.polygon = self.create_polygon(radius, angles)

    # Данный метод принимает следующие параметры:
    # radius - радиус описанной окружности многоугольника
    # angles - количество углов многоугольника 3, 4 или 5
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
            polygon.append(QPointF(self.pos.x()+x, self.pos.y()+y))
        return polygon