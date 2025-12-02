"""Модуль с модульными тестами для класса Snake."""

import unittest

from game.snake import Snake


class TestSnake(unittest.TestCase):
    """Набор тестов, проверяющих поведение змейки."""

    def setUp(self) -> None:
        """Создаёт базовый экземпляр змейки перед каждым тестом."""
        self.cell_size = 20
        self.snake = Snake(5, 5, self.cell_size)

    def test_initial_length_is_one(self) -> None:
        """Проверяет, что начальная длина змейки равна одной клетке."""
        self.assertEqual(len(self.snake.body_cells()), 1)

    def test_move_changes_head_position(self) -> None:
        """Проверяет, что при движении координаты головы изменяются."""
        head_before = self.snake.head_cell()
        self.snake.move()
        head_after = self.snake.head_cell()
        self.assertNotEqual(head_before, head_after)

    def test_change_direction_blocks_reverse(self) -> None:
        """Убеждается, что разворот на 180 градусов запрещён.

        После попытки сменить направление на противоположное змейка
        продолжает двигаться вперёд, а не назад.
        """
        head_before = self.snake.head_cell()
        self.snake.change_direction(-1, 0)
        self.snake.move()
        head_after = self.snake.head_cell()
        self.assertGreater(head_after[0], head_before[0])

    def test_grow_increases_length(self) -> None:
        """Проверяет, что метод grow() увеличивает длину змейки."""
        self.snake.grow()
        self.snake.move()
        self.assertEqual(len(self.snake.body_cells()), 2)

    def test_self_collision_detection(self) -> None:
        """Тестирует корректность обнаружения самоукуса змейки."""
        s = Snake(5, 5, self.cell_size)
        s.grow(3)
        s.move()
        s.move()
        s.move()
        s._body = [(5, 5), (5, 6), (6, 6), (6, 5)]
        s.change_direction(0, 1)
        s.move()
        self.assertTrue(s.check_self_collision())


if __name__ == "__main__":
    unittest.main()
