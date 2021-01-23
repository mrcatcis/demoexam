from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint
from math import pi, sin, cos

# Основной класс с окном
class Window(QWidget):

    # Класс правильного многоугольника
    class Polygon():
        
        # Инициализация класса
        def __init__(self, n: int, pos: QPoint, size: int):
            self.n = n
            self.pos = pos
            self.size = size
            self.polygon = self.createPolygon(n, pos, size)

        # Создание многоугольника
        def createPolygon(self, n: int, pos: QPoint, size: int) -> QPolygon:
            polygon = []
            delt = 2 * pi / n
            for i in range(n):
                i *= delt
                polygon.append(QPoint(pos.x() + int(sin(i) * size),
                                      pos.y() + int(cos(i) * size)))
            return QPolygon(polygon)

        # Добавление угла в многоугольник
        def addAngle(self):
            self.n += 1
            self.polygon = self.createPolygon(self.n, self.pos, self.size)

    # Инициализация главного окна
    def __init__(self):
        super().__init__()
        self.setWindowTitle('5.3')
        self.show()
        self.polygons = []

    # Возврашает количество многоугольников
    def countPolygons(self) -> int:
        return len(self.polygons)

    # Создаёт и показывает окно об ошибке
    def showError(self):
        errorDialog = QMessageBox()
        errorDialog.setWindowTitle('5.3')
        errorDialog.setText('Отсутствуют фигуры на поле')
        errorDialog.setIcon(QMessageBox.Warning)
        errorDialog.exec_()

    # Удаление всех многоугольников с поля
    def deletePolygons(self):
        if self.countPolygons() > 0:
            self.polygons.clear()
        else:
            self.showError()

    # Обработка события нажатия клавиши
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            self.deletePolygons()
            self.update()

    # Нахождение многоугольника в котором лежит заданная точка, возвращает -1 если не найдено
    def findPolygon(self, pos: QPoint) -> int:
        for i in range(len(self.polygons)):
            if self.polygons[i].polygon.containsPoint(pos, Qt.OddEvenFill):
                return i
        return -1

    # Обработка события нажатия кнопки мыши
    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        index = self.findPolygon(QPoint(x, y))
        if index == -1:
            self.polygons.append(self.Polygon(3, QPoint(x, y), 50))
        else:
            self.polygons[index].addAngle()

        self.update()

    # Обработка события рисования
    def paintEvent(self, event):
        self.painter = QPainter(self)
        self.painter.begin(self)
        self.drawPolygons()
        self.painter.end()

    # Отрисовка всех многоугольников
    def drawPolygons(self):
        for polygon in self.polygons:
            self.painter.drawPolygon(polygon.polygon)


if __name__ == '__main__':
    app = QApplication([])
    root = Window()
    app.exec_()
