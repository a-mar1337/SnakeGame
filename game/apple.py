"""Модуль с классом Apple.

Содержит реализацию яблока, которое появляется в свободной клетке поля
и умеет себя отрисовывать.
"""

import random
import pygame
from .base import BaseSquare


class Apple(BaseSquare):
    """Яблоко на игровом поле.

    Наследуется от базового квадрата и добавляет логику случайного
    появления и отрисовку более детализированного спрайта яблока.
    """

    def __init__(self,
                 cell_x: int,
                 cell_y: int,
                 cell_size: int,
                 color: tuple[int, int, int] = (255, 0, 0)) -> None:
        """Создаёт яблоко в заданной клетке.

        Args:
            cell_x: Координата клетки по оси X.
            cell_y: Координата клетки по оси Y.
            cell_size: Размер клетки в пикселях.
            color: Базовый цвет яблока.
        """
        super().__init__(cell_x, cell_y, cell_size, color)

    @staticmethod
    def spawn_random(cols: int,
                     rows: int,
                     cell_size: int,
                     forbidden_cells: list[tuple[int, int]]) -> "Apple":
        """Создаёт яблоко в случайной свободной клетке.

        Перебирает все клетки поля и исключает те, которые уже заняты
        (обычно телом змейки). Если свободных клеток нет, яблоко
        создаётся в (0, 0) как формальный объект.

        Args:
            cols: Количество колонок поля.
            rows: Количество строк поля.
            cell_size: Размер клетки в пикселях.
            forbidden_cells: Список занятых клеток (x, y).

        Returns:
            Экземпляр класса ``Apple`` в свободной клетке.
        """
        free_cells = [
            (x, y)
            for x in range(cols)
            for y in range(rows)
            if (x, y) not in forbidden_cells
        ]
        if not free_cells:
            x, y = 0, 0
        else:
            x, y = random.choice(free_cells)
        return Apple(x, y, cell_size)

    def cell(self) -> tuple[int, int]:
        """Возвращает координаты клетки, в которой находится яблоко.

        Returns:
            Кортеж (x, y) – координаты клетки.
        """
        return self.cell_x, self.cell_y

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает яблоко на переданной поверхности.

        Рисуется круг с бликом, коричневая ножка и зелёный листик,
        чтобы объект выглядел как стилизованное яблоко.

        Args:
            surface: Поверхность Pygame для отрисовки.
        """
        center_x = self.cell_x * self.cell_size + self.cell_size // 2
        center_y = self.cell_y * self.cell_size + self.cell_size // 2
        radius = self.cell_size // 2 - 3

        pygame.draw.circle(surface, (220, 0, 0), (center_x, center_y), radius)

        pygame.draw.circle(
            surface,
            (255, 150, 150),
            (center_x - radius // 3, center_y - radius // 3),
            max(1, radius // 4),
        )

        stem_width = max(2, self.cell_size // 10)
        stem_height = max(3, self.cell_size // 4)
        stem_rect = pygame.Rect(
            center_x - stem_width // 2,
            center_y - radius - stem_height + 2,
            stem_width,
            stem_height,
        )
        pygame.draw.rect(surface, (120, 70, 15), stem_rect)

        leaf_points = [
            (stem_rect.right, stem_rect.top),
            (stem_rect.right + self.cell_size // 4, stem_rect.top + self.cell_size // 6),
            (stem_rect.right, stem_rect.top + self.cell_size // 5),
        ]
        pygame.draw.polygon(surface, (0, 170, 0), leaf_points)
