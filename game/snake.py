"""Модуль с классом Snake.

Содержит реализацию змейки, которая двигается по клеточному полю,
растёт при поедании яблок и умеет себя отрисовывать.
"""

from .base import BaseSquare
import pygame


class Snake:
    """Класс змейки на клеточном поле.

    Хранит координаты сегментов тела в виде списка клеток, текущее
    направление движения и количество ожидаемых сегментов роста.
    Предоставляет методы движения, изменения направления, роста и
    проверки столкновения с собственным телом.
    """

    def __init__(self,
                 start_x: int,
                 start_y: int,
                 cell_size: int,
                 color: tuple[int, int, int] = (0, 255, 0)) -> None:
        """Инициализирует змейку в заданной клетке.

        Args:
            start_x: Начальная координата по оси X (номер клетки).
            start_y: Начальная координата по оси Y (номер клетки).
            cell_size: Размер одной клетки в пикселях.
            color: Базовый цвет змейки (для тела).
        """
        self.cell_size: int = cell_size
        self._body: list[tuple[int, int]] = [(start_x, start_y)]
        self._direction: tuple[int, int] = (1, 0)
        self._grow_pending: int = 0
        self.color: tuple[int, int, int] = color

    def change_direction(self, dx: int, dy: int) -> None:
        """Меняет направление движения змейки.

        Запрещает разворот на 180 градусов (движение строго в обратную
        сторону) и игнорирует нулевое направление.

        Args:
            dx: Смещение по оси X (-1, 0 или 1).
            dy: Смещение по оси Y (-1, 0 или 1).
        """
        cur_dx, cur_dy = self._direction
        if (dx, dy) == (-cur_dx, -cur_dy):
            return
        if dx == 0 and dy == 0:
            return
        self._direction = (dx, dy)

    def move(self) -> None:
        """Делает один шаг змейки в текущем направлении.

        Голова перемещается на одну клетку вперёд, новое положение
        добавляется в начало списка тела. Если есть отложенный рост,
        длина не уменьшается, иначе удаляется последний сегмент.
        """
        head_x, head_y = self._body[0]
        dx, dy = self._direction
        new_head = (head_x + dx, head_y + dy)
        self._body.insert(0, new_head)

        if self._grow_pending > 0:
            self._grow_pending -= 1
        else:
            self._body.pop()

    def grow(self, amount: int = 1) -> None:
        """Запланировать увеличение длины змейки.

        Args:
            amount: На сколько сегментов увеличить длину.
        """
        self._grow_pending += amount

    def head_cell(self) -> tuple[int, int]:
        """Возвращает координаты головы змейки в клетках.

        Returns:
            Кортеж (x, y) – координаты головы.
        """
        return self._body[0]

    def body_cells(self) -> list[tuple[int, int]]:
        """Возвращает копию списка всех клеток тела змейки.

        Returns:
            Список кортежей (x, y) для каждого сегмента.
        """
        return list(self._body)

    def check_self_collision(self) -> bool:
        """Проверяет, столкнулась ли голова с телом змейки.

        Returns:
            True, если голова находится в одной из остальных клеток тела,
            иначе False.
        """
        head = self._body[0]
        return head in self._body[1:]

    def draw(self, surface: pygame.Surface) -> None:
        """Отрисовывает змейку на переданной поверхности.

        Тело рисуется прямоугольниками базового цвета, голова –
        отдельным прямоугольником с глазами и ротиком.

        Args:
            surface: Поверхность Pygame, на которую нужно нарисовать змейку.
        """
        for i, (x, y) in enumerate(self._body):
            if i == 0:
                continue
            square = BaseSquare(x, y, self.cell_size, (0, 70, 200))
            square.draw(surface)

        head_x, head_y = self._body[0]
        head_rect = pygame.Rect(
            head_x * self.cell_size,
            head_y * self.cell_size,
            self.cell_size,
            self.cell_size,
        )
        pygame.draw.rect(surface, (0, 120, 255), head_rect)

        eye_size = self.cell_size // 4
        eye_offset_x = self.cell_size // 6
        eye_offset_y = self.cell_size // 6

        left_eye = pygame.Rect(
            head_rect.x + eye_offset_x,
            head_rect.y + eye_offset_y,
            eye_size,
            eye_size,
        )
        right_eye = pygame.Rect(
            head_rect.x + self.cell_size - eye_offset_x - eye_size,
            head_rect.y + eye_offset_y,
            eye_size,
            eye_size,
        )
        pygame.draw.rect(surface, (255, 255, 255), left_eye)
        pygame.draw.rect(surface, (255, 255, 255), right_eye)

        pupil_size = max(1, eye_size // 3)
        left_pupil = pygame.Rect(
            left_eye.centerx - pupil_size // 2,
            left_eye.centery - pupil_size // 2,
            pupil_size,
            pupil_size,
        )
        right_pupil = pygame.Rect(
            right_eye.centerx - pupil_size // 2,
            right_eye.centery - pupil_size // 2,
            pupil_size,
            pupil_size,
        )
        pygame.draw.rect(surface, (0, 0, 0), left_pupil)
        pygame.draw.rect(surface, (0, 0, 0), right_pupil)

        mouth_height = max(1, self.cell_size // 8)
        mouth_rect = pygame.Rect(
            head_rect.x + self.cell_size // 4,
            head_rect.y + self.cell_size - mouth_height - 2,
            self.cell_size // 2,
            mouth_height,
        )
        pygame.draw.rect(surface, (0, 0, 150), mouth_rect)
