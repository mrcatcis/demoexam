from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5 import Qt, QtCore
from PyQt5.Qt import QPushButton, QRect
from math import hypot, inf
from button import Button
from polygon import Polygon


class MainWindow(QWidget):
    # Данный метод не принимает значений
    # Выполняет инициализацию главного окна
    # Ничего не возвращает
    def __init__(self):
        super().__init__()
        self.init_gui()
        self.show()
        self.polygons = []
        self.chosen_polygon = None

    # Данный метод не принимает значений
    # Выполняет инициализацию GUI в окне
    # Ничего не возвращает
    def init_gui(self):
        self.setWindowTitle('Главное окно')
        self.setStyleSheet("font-size: 20px;")
        self.setGeometry(0, 0, 830, 700)

        self.button_triangle = Button(self, 3)
        self.button_triangle.setGeometry(10, 10, 200, 200)
        self.button_triangle.clicked.connect(self.choose_triangle)

        self.button_square = Button(self, 4)
        self.button_square.setGeometry(10, 220, 200, 200)
        self.button_square.clicked.connect(self.choose_square)

        self.button_penta = Button(self, 5)
        self.button_penta.setGeometry(10, 430, 200, 200)
        self.button_penta.clicked.connect(self.choose_penta)

        self.button_delete = QPushButton(self, text='Delete')
        self.button_delete.setGeometry(510, 640, 150, 50)
        self.button_delete.clicked.connect(self.delete_polygon)

        self.button_exit = QPushButton(self, text='Exit')
        self.button_exit.setGeometry(670, 640, 150, 50)
        self.button_exit.setStyleSheet(("background-color: #ff8800"))
        self.button_exit.clicked.connect(self.close)

    # Данный метод не принимает значений
    # Удаляет выбранный многоугольник если такой существует
    # Ничего не возвращает
    def delete_polygon(self):
        if self.chosen_polygon is not None:
            self.polygons.pop(self.chosen_polygon)
            self.chosen_polygon = None
            self.update()

    # Данный метод принимает позицию точки
    # Проверяет находится ли точка в области рисования
    # Возвращает bool
    def is_in_paint_box(self, pos):
        return QPolygon(QRect(220, 10, 600, 620)).containsPoint(pos, QtCore.Qt.OddEvenFill)

    # Данный метод не принимает значений
    # Проверяет какая кнопка выбранный
    # Возвращает количество углов у выбранной кнопки
    # или None если выбранных кнопок нет
    def get_chosen_angles(self):
        if self.button_triangle.chosen:
            return 3
        if self.button_square.chosen:
            return 4
        if self.button_penta.chosen:
            return 5
        return None

    # Данный метод принимает следующие значения: pos1 - первая точка;
    # pos 2 - вторая точка
    # Вычисляет расстояние между ними
    # Возвращает это расстояние
    def distance(self, pos1, pos2):
        return hypot(pos1.x() - pos2.x(), pos1.y() - pos2.y())

    # Данный метод не принимает значений
    # Показывает сообщение о том что на холсте есть 5 фигур
    # Ничего не возвращает
    def show_too_many_figures(self):
        error = QMessageBox()
        error.setWindowTitle('Ошибка')
        error.setText('На холсте уже есть 5 фигур')
        error.setIcon(QMessageBox.Warning)
        error.exec()

    # Данный метод принимает координаты точки
    # Находит ближайший к ней многоугольник
    # Возвращает номер этого многоугольника
    # или None если многоугольника не существует
    def find_close_polygon(self, pos):
        min_distance = inf
        min_index = None
        for i, polygon in enumerate(self.polygons):
            distance = self.distance(pos, polygon.pos)
            if distance < min_distance and distance < polygon.radius:
                min_distance = distance
                min_index = i
        return min_index

    # Данный метод является обработкой нажатия клавиш
    # Вызывается автоматически
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            self.delete_polygon()
            self.update()

    # Данный метод является обработкой нажатия клавишы мыши
    # Вызывается автоматически
    def mousePressEvent(self, event):
        if (event.buttons() & QtCore.Qt.RightButton
                and self.is_in_paint_box(event.pos())):
            self.unchoose_buttons()
        elif (event.buttons() & QtCore.Qt.LeftButton
                and self.is_in_paint_box(event.pos())):
            angles = self.get_chosen_angles()
            if angles is not None:
                if len(self.polygons) < 5:
                    # TODO change size; probably use new window
                    self.polygons.append(Polygon(100, angles, event.pos()))
                else:
                    self.show_too_many_figures()

            else:  # no selected button
                index = self.find_close_polygon(event.pos())
                self.chosen_polygon = index

        self.update()

    # Данный метод не принимает значений
    # Убирает выбранную кнопку
    # Ничего не возвращает
    def unchoose_buttons(self):
        self.button_triangle.chosen = False
        self.button_square.chosen = False
        self.button_penta.chosen = False

    # Данный метод не принимает значений
    # Выбирает треугольную кнопку
    # Ничего не возвращает
    def choose_triangle(self):
        self.unchoose_buttons()
        self.button_triangle.chosen = True
        self.update()

    # Данный метод не принимает значений
    # Выбирает квадратную кнопку
    # Ничего не возвращает
    def choose_square(self):
        self.unchoose_buttons()
        self.button_square.chosen = True
        self.update()

    # Данный метод не принимает значений
    # Выбирает пятиугольную кнопку
    # Ничего не возвращает
    def choose_penta(self):
        self.unchoose_buttons()
        self.button_penta.chosen = True
        self.update()

    # Данный метод является обработкой рисования
    # Вызывается автоматически
    def paintEvent(self, event):
        super().paintEvent(event)
        qp = QPainter()
        qp.begin(self)
        qp.drawRect(220, 10, 600, 620)
        qp.setBrush(QColor(255, 0, 0))
        for i, polygon in enumerate(self.polygons):
            qp.drawPolygon(polygon.polygon)
            if i == self.chosen_polygon:
                qp.setBrush(QColor(0, 0, 0, 0))
                qp.drawEllipse(polygon.pos, polygon.radius, polygon.radius)
                qp.setBrush(QColor(255, 0, 0))
        qp.end()


if __name__ == '__main__':
    app = QApplication([])
    root = MainWindow()
    app.exec()
