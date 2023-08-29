import pygame
from utils.rainbow_utils import rainbowAnimation, rainAnimation


pygame.display.set_caption('Kam Kam')

def rainbow_background(screen, height, width, rainbow_surface, rectangle_surface, counter):
    max_radius = 38

    # Draw the rainbow animation 
    if counter <= max_radius:
        rainbowAnimation(rainbow_surface, counter, width, height)
    screen.blit(rainbow_surface, (0, 0))
    screen.blit(rectangle_surface, (0, height // 2))

    if counter >= 40:
        rainAnimation(screen, counter)
    
    if counter > 10000: 
        counter = 40




























# import pygame
# from rainbow_utils import rainbowAnimation, rainAnimation

# # Initialize pygame
# pygame.init()

# # Screen dimensions
# width, height = 800, 480
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption('Kam Kam')

# # static 'surfaces' for rainbow - should help with performance
# rainbow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
# rectangle_surface = pygame.Surface((width, height // 2), pygame.SRCALPHA)
# rectangle_surface.fill((255, 255, 255))

# max_radius = 38


# # Main loop

# heart_rain = []


# #frame counter
# counter = 0

# # Clear the screen
# screen.fill((255, 255, 255))
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             running = False

#     # background rainbow code: 
#     if new_email:
#         counter += 1

#         # Draw the rainbow animation 
#         if counter <= max_radius:
#             rainbowAnimation(rainbow_surface, counter, width, height)
#         screen.blit(rainbow_surface, (0, 0))
#         screen.blit(rectangle_surface, (0, height // 2))

#         if counter >= 40:
#             rainAnimation(screen, counter)
        
#         if counter > 10000: 
#             counter = 40


#     # Display Email code: 

#     pygame.display.flip()
#     pygame.time.Clock().tick(30)

# pygame.quit()
