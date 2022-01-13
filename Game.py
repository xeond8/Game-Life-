import random
import sys

import pygame


class Game:
    def __init__(self, width, height, rows, columns):
        self.width = width  # Длина окна с игрой
        self.height = height  # Высота окна с игрой
        self.x_rate = int((width - 2 * INDENT) / columns)  # Длина ячейки по оси X
        self.y_rate = int((height - 2 * INDENT) / rows)  # Длина ячейки по оси Y
        self.screen = pygame.display.set_mode([width, height])  # Инициализируем окно с игрой
        self.grid = Grid(rows, columns)  # Инициализируем сетку с ячейками

    def show_cells(self):  # Выводим ячейки
        # pygame.draw.line(Surface, color, start_pos, end_pos, width=1)
        for i in range(self.grid.rows + 1):  # Рисуем горизонтальные линии сетки
            pygame.draw.line(self.screen, LINES_COLOR, (INDENT, INDENT + i * self.y_rate),
                             (self.x_rate * self.grid.columns + INDENT, INDENT + i * self.y_rate), LINE_WIDTH)
        for j in range(self.grid.columns + 1):  # Рисуем вертикальные линии сетки
            pygame.draw.line(self.screen, LINES_COLOR, (INDENT + j * self.x_rate, INDENT),
                             (INDENT + j * self.x_rate, INDENT + self.y_rate * self.grid.rows), LINE_WIDTH)

        for cells_row in self.grid.cells:
            for cell in cells_row:  # Цикл для каждой клетки из игры
                if cell.is_alive:  # Заполняем ячейку цветом если в ячейке есть жизнь
                    # Чтобы имитировать заполнение ячейки рисуем прямоугольник с помощью pygame.draw.rect()
                    # В параметрах этой функции указываем окно, цвет прямойгольника, координаты левого верхнего угла
                    # А также длину и ширину прямоугольника в виде [x, y, width, height]
                    pygame.draw.rect(self.screen, LIFE_COLOR,
                                     [INDENT + cell.x * self.x_rate + LINE_WIDTH - 1,
                                      INDENT + cell.y * self.y_rate + LINE_WIDTH - 1,
                                      self.x_rate - LINE_WIDTH, self.y_rate - LINE_WIDTH])


class Cell:  # Тип определяющий клетку
    def __init__(self, y, x, is_alive):
        # В библиотеке pygame точка (0, 0) - левый верхний угол, ось X идёт вправо, а ось Y вниз
        self.x = x  # Индекс ячейки по оси X
        self.y = y  # Индекс ячейки по оси Y
        self.is_alive = is_alive  # Информация о жизни в клетке

    def count_neighbors(self, net):  # Функция для подсчёта количества живых соседей ячейки
        count = 0
        for i in range(self.y - 1, self.y + 2):
            for j in range(self.x - 1, self.x + 2):
                if i == self.y and j == self.x:
                    continue
                if 0 <= i < net.rows and 0 <= j < net.columns:
                    count += int(net.cells[i][j].is_alive)
        return count

    def rule(self, table):  # Функция для определения существования жизни в клетке на следуюзщем ходу
        if 2 <= self.count_neighbors(table) <= 3 and self.is_alive:
            return True
        elif self.count_neighbors(table) == 3 and not self.is_alive:
            return True
        else:
            return False


class Grid:
    def __init__(self, rows, columns):
        self.rows = rows  # Количество строк в сетке
        self.columns = columns  # Количество столбцов в клетке
        # self.cells - Двумерный список с клетками (объектами типа Cell), наличие жизни в которых определяется случайно
        self.cells = [[Cell(i, j, random.choice([False, True])) for j in range(columns)] for i in range(rows)]

    def update_life(self):  # Функция для определения наличия жизни на следующем ходу в ячейках сетки
        temp_grid = Grid(self.rows, self.columns)
        temp_grid.cells = [[Cell(i, j, 0) for j in range(self.columns)] for i in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                temp_grid.cells[i][j].is_alive = self.cells[i][j].rule(self)
        self.cells = temp_grid.cells


SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
NUMBER_OF_ROWS = 25
NUMBER_OF_COLUMNS = 25
LINES_COLOR = (165, 165, 165)
LIFE_COLOR = (22, 224, 90)
LINE_WIDTH = 4
INDENT = 15

pygame.init()  # Инициализировать библиотеку pygame
pygame.display.set_caption('Игра "Жизнь"')  # Вводим название окна с игрой
game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, NUMBER_OF_ROWS, NUMBER_OF_COLUMNS)
clock = pygame.time.Clock()  # Создаём объект типа Clock для регулиции частоты кадров в секунду

while True:
    game.screen.fill((0, 0, 0))  # Заполняем экран игры фоном
    clock.tick(15)  # Устанавливаем частоту кадров в секунду
    for event in pygame.event.get():  # Получаем события из очереди
        if event.type == pygame.QUIT:  # Завершаем работу программы если пользователь вышел из игры
            pygame.quit()
            sys.exit()
    game.show_cells()  # Рисуем все клетки
    pygame.display.flip()  # Выводим на экран всё, что нарисовали
    game.grid.update_life()  # Обновляем статус жизни в клетках
