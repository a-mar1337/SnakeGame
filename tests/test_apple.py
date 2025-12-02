"""Модуль с модульными тестами для класса Apple."""

import unittest

from game.apple import Apple
from game.snake import Snake


class TestApple(unittest.TestCase):
    """Набор тестов, проверяющих поведение яблока."""

    def test_spawn_not_on_snake(self) -> None:
        """Проверяет, что новое яблоко не появляется на теле змейки."""
        cols = 10
        rows = 10
        cell_size = 20

        snake = Snake(cols // 2, rows // 2, cell_size)
        snake.grow(3)
        for _ in range(3):
            snake.move()

        apple = Apple.spawn_random(cols, rows, cell_size, snake.body_cells())

        self.assertNotIn(apple.cell(), snake.body_cells())


if __name__ == "__main__":
    unittest.main()
