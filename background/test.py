import pygame
from rainbow import rainbow_background

pygame.init()

width = 800
height = 480
screen = pygame.display.set_mode((width, height))


running = True

# Clear the screen
screen.fill((255, 255, 255))

counter = 0

while running: 
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        running = False
  
  counter += 1
  rainbow_background(screen, height, width, rainbow_surface, rectangle_surface, counter)

  pygame.display.flip()
  pygame.time.Clock().tick(30)