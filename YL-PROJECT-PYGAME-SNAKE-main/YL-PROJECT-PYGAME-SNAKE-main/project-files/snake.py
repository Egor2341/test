import pygame
import sys
import random
import os

HEIGHT = 640
WIDTH = 800
SIZE = 30
BLACK = (0, 0, 0)
GREEN = (80, 80, 80)
RED = (150, 150, 150)
UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)
SPEED = 20

fps_clock = pygame.time.Clock()
display = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
font = pygame.font.SysFont('arial', 50)
scores = 0
fps = 10
clock = pygame.time.Clock()


def start_screen():
    intro_text = ["Игра 'Змейка'"]

    fon = pygame.transform.scale(load_image('fon_zmeika.jpg'), (WIDTH, HEIGHT))
    display.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        display.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(fps)

def end_screen():


    fon = pygame.transform.scale(load_image('fon_over.jpg'), (WIDTH, HEIGHT))
    display.blit(fon, (0, 0))



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish()

        pygame.display.flip()
        clock.tick(fps)

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()

    return image


all_sprites = pygame.sprite.Group()
start_screen()

# функция финиша: закрывает игру
def finish():
    pygame.quit()
    sys.exit(0)


# генерация новых яблок
def make_new_apple():
    sprite = pygame.sprite.Sprite()
    sprite.image = load_image("apple.png", -1)
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    sprite.rect.x = random.randrange(0, WIDTH - SIZE)
    sprite.rect.y = random.randrange(0, HEIGHT - SIZE)
    apple = sprite
    return apple


# добавление элементов в змейку
def add_part_of_snake(snake, snake_tail, head):
    global scores, fps
    update = [-SIZE * x for x in head]
    scores += 1
    fps += 0.5
    
    if len(snake_tail) == 0:
        snake_tail.append(snake.move(update[0], update[1]))
    else:
        snake_tail.append(snake_tail[len(snake_tail) - 1].move(update[0], update[1]))


# функция отрисовки: отрисовка поля, яблок и змейки
def draw_snake(snake, snake_tail, head):
    tmp = snake.move(0, 0)
    speed_head = [SPEED * x for x in head]
    snake.move_ip(speed_head[0], speed_head[1])
    pygame.draw.rect(display, GREEN, snake)
    
    if len(snake_tail) == 0:
        return None
    
    pygame.draw.rect(display, (50, 50, 50), snake_tail[len(snake_tail) - 1])
    for i in range(0, len(snake_tail) - 1):
        snake_tail[len(snake_tail) - 1 - i] = snake_tail[len(snake_tail) - 2 - i]
        pygame.draw.rect(display, GREEN, snake_tail[len(snake_tail) - 1 - i])
    
    snake_tail[0] = tmp
    pygame.draw.rect(display, GREEN, snake_tail[0])
    
    
# основная функция
def main():
    global scores, fps
    pygame.display.set_caption('snake')
    snake = pygame.Rect(WIDTH / 2 - SIZE / 2, 
                        HEIGHT / 2 - SIZE / 2, 
                        SIZE, SIZE)    # сама змея
    head = RIGHT    # сторона движения головы
    apple = make_new_apple()    # текущее яблоко

    snake_tail = []     # тело змейки
    while True:
        for event in pygame.event.get():
            # закрытие окна
            if event.type == pygame.QUIT:
                finish()
            # управление
            elif event.type == pygame.KEYDOWN:
                # меняем сторону движения головы
                if event.key == pygame.K_UP or event.key == pygame.K_w and head != DOWN:
                    head = UP
                if event.key == pygame.K_DOWN or event.key == pygame.K_s and head != UP:
                    head = DOWN    
                if event.key == pygame.K_LEFT or event.key == pygame.K_a and head != RIGHT:
                    head = LEFT
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d and head != LEFT:
                    head = RIGHT
        
        # если нет места - финиш
        if snake.left < 0 or snake.right > WIDTH or snake.top < 0 or snake.bottom > HEIGHT:
            end_screen()

        # в противном случае - генерируем яблоко
        if snake.colliderect(apple):
            apple.kill()
            apple = make_new_apple()
            add_part_of_snake(snake, snake_tail, head)
        display.fill((50, 50, 50))
        text = font.render(str(scores), False, (150, 150, 150))
        display.blit(text, (10, 10))
        all_sprites.draw(display)
        draw_snake(snake, snake_tail, head)
        pygame.display.update()
        fps_clock.tick(fps)
    

main()


# MADE BY EGOR KOLESNIKOV & EGOR ANTIPIN