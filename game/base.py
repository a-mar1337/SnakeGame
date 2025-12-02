"""Базовые геометрические примитивы для игровых объектов.

Содержит класс BaseSquare, описывающий клетку/квадрат на игровом поле,
от которого наследуются змейка и яблоко.
"""

import pygame


class BaseSquare:
    """Базовый класс квадрата на игровом поле.

    Хранит координаты клетки, размер и цвет, а также предоставляет
    методы для получения прямоугольника Pygame и отрисовки.
    """

    def __init__(self,
                 cell_x: int,
                 cell_y: int,
                 cell_size: int,
                 color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """Создаёт квадрат в указанной клетке.

        Args:
            cell_x: Координата клетки по оси X.
            cell_y: Координата клетки по оси Y.
            cell_size: Размер клетки в пикселях.
            color: Цвет квадрата в формате (R, G, B).
        """
        self.cell_x: int = cell_x
        self.cell_y: int = cell_y
        self.cell_size: int = cell_size
        self.color: tuple[int, int, int] = color

    def rect(self) -> pygame.Rect:
        """Возвращает прямоугольник Pygame для текущей клетки.

        Returns:
            Объект ``pygame.Rect``, соответствующий положению и размеру
            квадрата на экране.
        """
        return pygame.Rect(
            self.cell_x * self.cell_size,
            self.cell_y * self.cell_size,
            self.cell_size,
            self.cell_size,
        )

    def draw(self, surface: pygame.Surface) -> None:
        """Рисует квадрат на указанной поверхности.

        Args:
            surface: Поверхность Pygame, на которую выполняется отрисовка.
        """
        pygame.draw.rect(surface, self.color, self.rect())
