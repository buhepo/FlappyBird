import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Параметры окна
WIDTH, HEIGHT = 400, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Цвета
BLUE = (135, 206, 235)
BUTTON_COLOR = (255, 242, 0)
BUTTON_BORDER_COLOR = (163, 153, 3)
GREEN = (0, 255, 0)

# Параметры птицы
bird_x = 100
bird_y = 300
bird_width = 51  # Ширина птицы
bird_height = 36  # Высота птицы
bird_velocity = 0
bird_rotation = 0  # Угол поворота
bird_image = pygame.image.load('images/bird.png')

# Гравитация и скорость птицы
gravity = 0.1
jump_strength = -3
max_fall_speed = 1.5
bird_velocity = min(bird_velocity + gravity, max_fall_speed)

# Параметры первой трубы
tube_width = 50
tube_gap = 200
first_tube_x = WIDTH  # Первая труба
tube_height = random.randint(50, 400)
tube_y = [tube_height, tube_height + tube_gap]

# Параметры последующих труб
tube_spacing = 0.01
next_tube_x =tube_spacing - tube_width

# Счет и ускорение
score = 0
speed_multiplier = 0.75

# Флаг для отслеживания конца игры
game_over = False

# Загрузка изображения птицы
bird_image = pygame.image.load('images/bird.png')
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))

# Функция для начала новой игры
def restart_game():
    global bird_y, bird_velocity, first_tube_x, tube_height, tube_y, next_tube_x, score, game_over, speed_multiplier
    bird_y = 300
    bird_velocity = 0
    first_tube_x = WIDTH + 100  # Первая труба
    tube_height = random.randint(50, 400)
    tube_y = [tube_height, tube_height + tube_gap]
    next_tube_x = tube_spacing
    score = 0
    game_over = False
    speed_multiplier = .75  # Сбросить ускорение

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength

    if not game_over:
        # Птица
        if bird_velocity > 0:
            bird_rotation = -45  # Если падает, угол -45 градусов
        else:
            bird_rotation = 45  # Если в прыжке, угол +45 градусов

        bird_y += bird_velocity
        bird_velocity = min(bird_velocity + gravity, max_fall_speed)  # Ограничиваем максимальную скорость падения

        # Трубы
        first_tube_x -= 3 * speed_multiplier  # Замедли движение первой трубы
        next_tube_x -= 3 * speed_multiplier  # Замедли движение последующих труб
        if first_tube_x < -tube_width:
            first_tube_x = WIDTH + 100
            tube_height = random.randint(50, 400)
            tube_y = [tube_height, tube_height + tube_gap]
            next_tube_x = 0.1
            score += 1
            speed_multiplier += 0.035  # Увеличиваем ускорение

        # Коллизии
        bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
        top_tube_rect = pygame.Rect(first_tube_x, 0, tube_width, tube_y[0])
        bottom_tube_rect = pygame.Rect(first_tube_x, tube_y[1], tube_width, HEIGHT - tube_y[1])

        if bird_rect.colliderect(top_tube_rect) or bird_rect.colliderect(bottom_tube_rect) or bird_y > HEIGHT or bird_y < 0:
            game_over = True

    # Отрисовка фона (голубой)
    WINDOW.fill(BLUE)

    if not game_over:
        # Если игра не окончена, отобразим текущий счет
        font = pygame.font.Font(None, 36)
        text = font.render("Счет: " + str(score), True, (0, 0, 0))  # Черный цвет для счета
        WINDOW.blit(text, (WIDTH // 2 - 40, 50))

        # Отрисовка зеленых труб
        top_tube = pygame.Rect(first_tube_x, 0, tube_width, tube_y[0])
        bottom_tube = pygame.Rect(first_tube_x, tube_y[1], tube_width, HEIGHT - tube_y[1])
        pygame.draw.rect(WINDOW, GREEN, top_tube)
        pygame.draw.rect(WINDOW, GREEN, bottom_tube)

        # Вращение птицы
        bird_rotated = pygame.transform.rotozoom(bird_image, bird_rotation, 1)
        bird_rect = bird_rotated.get_rect(center=(bird_x + bird_width // 2, bird_y + bird_height // 2))
        WINDOW.blit(bird_rotated, bird_rect.topleft)

    if game_over:
        # Если игра окончена, отобразим счет и кнопку "Еще раз"
        font = pygame.font.Font(None, 36)
        text = font.render("Счет: " + str(score), True, (0, 0, 0))  # Черный цвет для счета
        WINDOW.blit(text, (WIDTH // 2 - 40, HEIGHT // 2 - 20))

        # Отображение кнопки "Еще раз"
        button_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 20, 100, 50)
        pygame.draw.rect(WINDOW, BUTTON_COLOR, button_rect)
        pygame.draw.rect(WINDOW, BUTTON_BORDER_COLOR, button_rect, 3)  # Обводка кнопки
        font = pygame.font.Font(None, 30)
        text = font.render("Еще раз", True, (0, 0, 0))  # Черный цвет для текста
        text_rect = text.get_rect(center=button_rect.center)
        WINDOW.blit(text, text_rect)

        # Обработка нажатия на кнопку "Еще раз"
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_x, mouse_y):
            if pygame.mouse.get_pressed()[0]:
                restart_game()

    # Обновление экрана
    pygame.display.update()
