"""Main module of the Snake game.

Содержит главное меню, запуск игрового цикла, работу со статистикой
и настройку параметров игрока (имя, скорость, сложность).
"""

import sys
from datetime import datetime

import pygame

from game.snake import Snake
from game.apple import Apple


VIRTUAL_WIDTH = 1300
VIRTUAL_HEIGHT = 1300

GRID_COLS = 15
GRID_ROWS = 15
CELL_SIZE = VIRTUAL_WIDTH // GRID_COLS

FPS_BASE = 30

LIGHT_GREEN = (170, 215, 81)
DARK_GREEN = (162, 209, 73)
BORDER_COLOR = (0, 0, 0)

STATE_MENU = "menu"
STATE_GAME = "game"


def save_result(player_name: str, score: int) -> None:
    """Сохраняет результат одной игры в файл статистики.

    Строка сохраняется в формате: ``YYYY-MM-DD HH:MM:SS;Имя;Счёт``.

    Args:
        player_name: Имя игрока.
        score: Набранный счёт.
    """
    with open("results.txt", "a", encoding="utf-8") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{now};{player_name};{score}\n")


def load_best_score() -> int:
    """Считывает лучший результат из файла статистики.

    Файл ``results.txt`` просматривается построчно, из каждой строки
    извлекается значение счёта, после чего выбирается максимум.

    Returns:
        Максимальный счёт среди всех записей или 0, если файла ещё нет
        или он пустой.
    """
    best = 0
    try:
        with open("results.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) >= 3:
                    try:
                        s = int(parts[2])
                        if s > best:
                            best = s
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return best


def draw_background(surface: pygame.Surface,
                    cols: int,
                    rows: int,
                    cell_size: int) -> None:
    """Рисует шахматное игровое поле и рамку.

    Args:
        surface: Поверхность, на которую производится отрисовка.
        cols: Количество колонок клеток.
        rows: Количество строк клеток.
        cell_size: Размер клетки в пикселях.
    """
    for x in range(cols):
        for y in range(rows):
            if (x + y) % 2 == 0:
                color = LIGHT_GREEN
            else:
                color = DARK_GREEN
            rect = pygame.Rect(
                x * cell_size,
                y * cell_size,
                cell_size,
                cell_size,
            )
            pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(
        surface,
        BORDER_COLOR,
        pygame.Rect(0, 0, cols * cell_size, rows * cell_size),
        width=2,
    )


def run_menu(screen: pygame.Surface,
             clock: pygame.time.Clock) -> tuple[str, int, str]:
    """Отображает главное меню и возвращает выбранные параметры игры.

    В меню пользователь может ввести имя, выбрать начальную скорость
    и уровень сложности. Завершение работы приложения возможно по ESC.

    Args:
        screen: Главное окно Pygame.
        clock: Объект таймера для ограничения FPS меню.

    Returns:
        Кортеж ``(player_name, speed, difficulty)``, где:
            * ``player_name`` – имя игрока;
            * ``speed`` – выбранная начальная скорость;
            * ``difficulty`` – строка ``"easy"``, ``"normal"`` или ``"hard"``.
    """
    running = True

    menu_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT)).convert()

    font_big = pygame.font.SysFont(None, 96)
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    selected_speed = 10
    min_speed = 3
    max_speed = 25
    difficulties = ["easy", "normal", "hard"]
    diff_index = 1

    player_name = ""
    active_name = False

    center_x = VIRTUAL_WIDTH // 2
    row_y1 = VIRTUAL_HEIGHT // 3
    row_y2 = row_y1 + 130
    row_y3 = row_y2 + 130
    row_y4 = row_y3 + 130

    field_width = 400
    field_height = 60
    btn_square = 60

    name_rect = pygame.Rect(center_x - field_width // 2,
                            row_y1,
                            field_width,
                            field_height)

    speed_minus_rect = pygame.Rect(center_x - field_width // 2,
                                   row_y2,
                                   btn_square,
                                   btn_square)
    speed_value_rect = pygame.Rect(
        center_x - field_width // 2 + btn_square + 10,
        row_y2,
        field_width - 2 * (btn_square + 10),
        btn_square,
    )
    speed_plus_rect = pygame.Rect(center_x + field_width // 2 - btn_square,
                                  row_y2,
                                  btn_square,
                                  btn_square)

    difficulty_rect = pygame.Rect(center_x - field_width // 2,
                                  row_y3,
                                  field_width,
                                  field_height)

    start_rect = pygame.Rect(center_x - 150, row_y4, 300, 70)

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if active_name:
                    if event.key == pygame.K_RETURN:
                        active_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    else:
                        if len(player_name) < 12 and event.unicode.isprintable():
                            player_name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                sw, sh = screen.get_size()
                scale_x = VIRTUAL_WIDTH / sw
                scale_y = VIRTUAL_HEIGHT / sh
                vx = mx * scale_x
                vy = my * scale_y

                if name_rect.collidepoint(vx, vy):
                    active_name = True
                else:
                    active_name = False

                if speed_minus_rect.collidepoint(vx, vy):
                    selected_speed = max(min_speed, selected_speed - 1)
                elif speed_plus_rect.collidepoint(vx, vy):
                    selected_speed = min(max_speed, selected_speed + 1)
                elif difficulty_rect.collidepoint(vx, vy):
                    diff_index = (diff_index + 1) % len(difficulties)
                elif start_rect.collidepoint(vx, vy):
                    if not player_name:
                        player_name = "Player"
                    return player_name, selected_speed, difficulties[diff_index]

        menu_surface.fill((30, 120, 60))

        title_surf = font_big.render("ЗМЕЙКА", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(center_x, VIRTUAL_HEIGHT // 5))
        menu_surface.blit(title_surf, title_rect)

        name_label = font.render("Имя игрока:", True, (0, 0, 0))
        menu_surface.blit(name_label, (center_x - field_width // 2, row_y1 - 50))

        pygame.draw.rect(
            menu_surface,
            (255, 255, 255) if active_name else (230, 230, 230),
            name_rect,
            border_radius=10,
        )
        name_display = player_name if player_name else "Введите имя..."
        color = (0, 0, 0) if player_name else (120, 120, 120)
        name_text = font.render(name_display, True, color)
        menu_surface.blit(
            name_text,
            name_text.get_rect(midleft=(name_rect.x + 15, name_rect.centery)),
        )

        speed_label = font.render("Начальная скорость:", True, (0, 0, 0))
        menu_surface.blit(speed_label, (center_x - field_width // 2, row_y2 - 50))

        pygame.draw.rect(menu_surface, (50, 50, 50), speed_minus_rect, border_radius=10)
        pygame.draw.rect(menu_surface, (50, 50, 50), speed_plus_rect, border_radius=10)
        pygame.draw.rect(menu_surface, (230, 230, 230), speed_value_rect, border_radius=10)

        minus_text = font.render("-", True, (255, 255, 255))
        plus_text = font.render("+", True, (255, 255, 255))
        value_text = font.render(str(selected_speed), True, (0, 0, 0))

        menu_surface.blit(minus_text, minus_text.get_rect(center=speed_minus_rect.center))
        menu_surface.blit(plus_text, plus_text.get_rect(center=speed_plus_rect.center))
        menu_surface.blit(value_text, value_text.get_rect(center=speed_value_rect.center))

        diff_label = font.render("Сложность:", True, (0, 0, 0))
        menu_surface.blit(diff_label, (center_x - field_width // 2, row_y3 - 60))

        pygame.draw.rect(menu_surface, (230, 230, 230), difficulty_rect, border_radius=10)
        diff_name = difficulties[diff_index].capitalize()
        diff_text = font.render(diff_name, True, (0, 0, 0))
        menu_surface.blit(diff_text, diff_text.get_rect(center=difficulty_rect.center))

        pygame.draw.rect(menu_surface, (70, 160, 70), start_rect, border_radius=10)
        start_text = font.render("Старт", True, (255, 255, 255))
        menu_surface.blit(start_text, start_text.get_rect(center=start_rect.center))

        hint = small_font.render("ESC - выход, клик по полю имени для ввода", True, (0, 0, 0))
        menu_surface.blit(hint, (10, VIRTUAL_HEIGHT - hint.get_height() - 10))

        sw, sh = screen.get_size()
        scaled = pygame.transform.smoothscale(menu_surface, (sw, sh))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()


def run_game(screen: pygame.Surface,
             clock: pygame.time.Clock,
             player_name: str,
             base_speed: int,
             difficulty: str) -> bool:
    """Запускает один игровой сеанс змейки.

    Обрабатывает управление, обновляет позицию змейки и яблока, считает
    очки, сохраняет результат и отображает экран окончания игры.

    Args:
        screen: Главное окно Pygame.
        clock: Объект pygame.time.Clock для ограничения FPS.
        player_name: Имя текущего игрока.
        base_speed: Начальная скорость, выбранная в меню.
        difficulty: Строка сложности: 'easy', 'normal' или 'hard'.

    Returns:
        True, если игрок выбрал «Играть снова», иначе False.
    """
    if difficulty == "easy":
        speed = max(5, base_speed)
        apples_per_speedup = 7
    elif difficulty == "hard":
        speed = max(15, base_speed)
        apples_per_speedup = 4
    else:
        speed = base_speed
        apples_per_speedup = 5

    min_speed = 3
    max_speed = 30

    pygame.mixer.init()
    try:
        eat_sound = pygame.mixer.Sound("sounds/eat.wav")
    except Exception:
        eat_sound = None
    try:
        gameover_sound = pygame.mixer.Sound("sounds/gameover.wav")
    except Exception:
        gameover_sound = None

    game_surface = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT)).convert()

    cols = GRID_COLS
    rows = GRID_ROWS

    snake = Snake(cols // 2, rows // 2, CELL_SIZE)
    apple = Apple.spawn_random(cols, rows, CELL_SIZE, snake.body_cells())

    running = True
    game_over = False
    paused = False
    score = 0
    best_score = load_best_score()

    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 28)

    button_width = 260
    button_height = 60
    button_margin = 20
    btn_x = (VIRTUAL_WIDTH - button_width) // 2
    btn_y_restart = VIRTUAL_HEIGHT // 2 + 40
    btn_y_quit = btn_y_restart + button_height + button_margin

    while running:
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                    speed = min(max_speed, speed + 1)
                if event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE, pygame.K_KP_MINUS):
                    speed = max(min_speed, speed - 1)

                if event.key == pygame.K_p and not game_over:
                    paused = not paused

                if not game_over and not paused:
                    if event.key in (pygame.K_w, pygame.K_UP):
                        snake.change_direction(0, -1)
                    elif event.key in (pygame.K_s, pygame.K_DOWN):
                        snake.change_direction(0, 1)
                    elif event.key in (pygame.K_a, pygame.K_LEFT):
                        snake.change_direction(-1, 0)
                    elif event.key in (pygame.K_d, pygame.K_RIGHT):
                        snake.change_direction(1, 0)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over:
                mx, my = pygame.mouse.get_pos()
                screen_w, screen_h = screen.get_size()
                scale_x = VIRTUAL_WIDTH / screen_w
                scale_y = VIRTUAL_HEIGHT / screen_h
                vx = mx * scale_x
                vy = my * scale_y

                restart_rect = pygame.Rect(btn_x, btn_y_restart, button_width, button_height)
                quit_rect = pygame.Rect(btn_x, btn_y_quit, button_width, button_height)

                if restart_rect.collidepoint(vx, vy):
                    return True
                elif quit_rect.collidepoint(vx, vy):
                    running = False

        if not game_over and not paused:
            snake.move()
            head_x, head_y = snake.head_cell()

            if not (0 <= head_x < cols and 0 <= head_y < rows):
                game_over = True
                if gameover_sound:
                    gameover_sound.play()

            if not game_over and snake.check_self_collision():
                game_over = True
                if gameover_sound:
                    gameover_sound.play()

            if not game_over and snake.head_cell() == apple.cell():
                score += 1
                snake.grow()
                apple = Apple.spawn_random(cols, rows, CELL_SIZE, snake.body_cells())
                if eat_sound:
                    eat_sound.play()

                if score % apples_per_speedup == 0:
                    speed = min(max_speed, speed + 1)

            if game_over:
                save_result(player_name, score)
                if score > best_score:
                    best_score = score

        draw_background(game_surface, cols, rows, CELL_SIZE)
        apple.draw(game_surface)
        snake.draw(game_surface)

        score_surf = font.render(f"Счёт: {score}", True, (0, 0, 0))
        best_surf = font.render(f"Рекорд: {best_score}", True, (0, 0, 0))
        game_surface.blit(score_surf, (10, 10))
        game_surface.blit(best_surf, (10, 20 + score_surf.get_height()))

        hint_text = "P - пауза   +/- - скорость"
        hint_surf = small_font.render(hint_text, True, (0, 0, 0))
        game_surface.blit(
            hint_surf,
            (10, VIRTUAL_HEIGHT - hint_surf.get_height() - 10),
        )

        if paused and not game_over:
            overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            game_surface.blit(overlay, (0, 0))
            pause_surf = font.render("Пауза (P - продолжить)", True, (255, 255, 255))
            pause_rect = pause_surf.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2))
            game_surface.blit(pause_surf, pause_rect)

        if game_over:
            overlay = pygame.Surface((VIRTUAL_WIDTH, VIRTUAL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            game_surface.blit(overlay, (0, 0))

            title_surf = font.render("Игра окончена", True, (255, 255, 255))
            title_rect = title_surf.get_rect(center=(VIRTUAL_WIDTH // 2, VIRTUAL_HEIGHT // 2 - 40))
            game_surface.blit(title_surf, title_rect)

            restart_rect = pygame.Rect(btn_x, btn_y_restart, button_width, button_height)
            quit_rect = pygame.Rect(btn_x, btn_y_quit, button_width, button_height)

            pygame.draw.rect(game_surface, (50, 150, 50), restart_rect, border_radius=10)
            pygame.draw.rect(game_surface, (150, 50, 50), quit_rect, border_radius=10)

            restart_text = font.render("Играть снова", True, (255, 255, 255))
            quit_text = font.render("Выход", True, (255, 255, 255))

            game_surface.blit(restart_text, restart_text.get_rect(center=restart_rect.center))
            game_surface.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

        screen_w, screen_h = screen.get_size()
        scaled = pygame.transform.smoothscale(game_surface, (screen_w, screen_h))
        screen.blit(scaled, (0, 0))
        pygame.display.flip()

    return False


def main() -> None:
    """Точка входа в приложение.

    Инициализирует Pygame, создаёт окно и переключает управление между
    главным меню и игровым циклом до тех пор, пока пользователь не
    закроет приложение.
    """
    pygame.init()

    info = pygame.display.Info()
    screen_width = int(info.current_w * 0.9)
    screen_height = int(info.current_h * 0.9)
    screen = pygame.display.set_mode(
        (screen_width, screen_height),
        pygame.RESIZABLE | pygame.HWSURFACE | pygame.DOUBLEBUF,
    )
    pygame.display.set_caption("Змейка")

    clock = pygame.time.Clock()

    while True:
        player_name, base_speed, difficulty = run_menu(screen, clock)
        restart = True
        while restart:
            restart = run_game(screen, clock, player_name, base_speed, difficulty)


if __name__ == "__main__":
    main()
