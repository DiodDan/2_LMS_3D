import pygame
import pygame_widgets
from pygame_widgets.button import Button
from main import start_me_up

pygame.init()
win = pygame.display.set_mode((600, 600))
button = Button(win, 100, 100, 300, 150, onClick=start_me_up)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()

    win.fill((255, 255, 255))

    pygame_widgets.update(events)

    button.listen(events)
    button.draw()

    pygame.display.update()
