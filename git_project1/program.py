import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 200, 200
    screen = pygame.display.set_mode(size)
    running = True
    n = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEOEXPOSE:
                screen.fill((0, 0, 0))
                font = pygame.font.Font(None, 100)
                text = font.render(f"{n}", True, (255, 0, 0))
                text_x = width // 2 - text.get_width() // 2
                text_y = height // 2 - text.get_height() // 2
                screen.blit(text, (text_x, text_y))
                n += 1
        pygame.display.flip()
