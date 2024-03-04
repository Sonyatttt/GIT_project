import os
import pygame
import time
import random

pygame.init()
pygame.display.set_caption('Змейка')
width = 600
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 102, 0)
yellow = (253, 233, 16)

snake_position = [100, 50]
snake_body = [[100, 50],
              [90, 50],
              [80, 50],
              [70, 50]]

apple_position = [random.randrange(1, (width // 10)) * 10,
                  random.randrange(1, (height // 10)) * 10]

fruit_spawn = True
direction = 'RIGHT'
change_to = direction
apple = 0
FPS = 14
level = 0


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_fo = pygame.font.SysFont(font, size)

    apples_eaten = score_font.render('Яблоки: ' + str(apple), True, color)
    apples_eat = score_fo.render('Уровень: ' + str(level), True, color)
    score_rect = apples_eaten.get_rect()

    score_re = apples_eat.get_rect()
    score_re.midtop = (40, 30)

    screen.blit(apples_eaten, score_rect)
    screen.blit(apples_eat, score_re)


def game_over():
    font = pygame.font.SysFont('Arial', 50)
    fonty = pygame.font.SysFont('Arial', 30)
    game_over_surface = font.render('Вы проиграли ', True, black)
    game_over_sur = fonty.render('Яблоки: ' + str(apple) + '    Уровень: ' + str(level),
                                 True, black)

    game_over_rect = game_over_surface.get_rect()
    game_over_re = game_over_sur.get_rect()

    game_over_rect.midtop = (width / 2, height / 4)
    game_over_re.midtop = (300, 270)

    screen.blit(game_over_surface, game_over_rect)
    screen.blit(game_over_sur, game_over_re)

    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()


screen.fill(green)
all_sprites = pygame.sprite.Group()
sprite_image = load_image('grass1.jpg')
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = sprite_image
sprite.rect = sprite.image.get_rect()
new_sprite = pygame.transform.scale(sprite_image, (10, 10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
                if change_to == 'UP' and direction != 'DOWN':
                    direction = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
                if change_to == 'DOWN' and direction != 'UP':
                    direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
                if change_to == 'LEFT' and direction != 'RIGHT':
                    direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
                if change_to == 'RIGHT' and direction != 'LEFT':
                    direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10
    if pygame.mouse.get_focused():
        all_sprites.draw(screen)
    pygame.display.flip()

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == apple_position[0] and snake_position[1] == apple_position[1]:
        apple += 1
        fruit_spawn = False
        if apple % 5 == 0:
            level += 1
    else:
        snake_body.pop()

    if not fruit_spawn:
        apple_position = [random.randrange(1, (width // 10)) * 10,
                          random.randrange(1, (height // 10)) * 10]

    fruit_spawn = True

    for pos in snake_body:
        pygame.draw.rect(screen, yellow,
                         pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, red, pygame.Rect(
        apple_position[0], apple_position[1], 10, 10))

    if snake_position[0] < 0 or snake_position[0] > width - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > height - 10:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(1, white, 'Arial', 20)
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
