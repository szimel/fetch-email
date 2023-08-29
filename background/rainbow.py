import pygame
from utils.rainbow_utils import rainbowAnimation, rainAnimation


pygame.display.set_caption('Kam Kam')

def rainbow_background(screen, height, width, rainbow_surface, rectangle_surface, counter):
    max_radius = 38
    screen.fill((255, 255, 255))    

    if counter <= max_radius:
        rainbowAnimation(rainbow_surface, counter, width, height)
    screen.blit(rainbow_surface, (0, 0))
    screen.blit(rectangle_surface, (0, height // 2))

    if counter >= 40:
        rainAnimation(screen, counter)

