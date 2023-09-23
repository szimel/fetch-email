import pygame
import math
from utils.display_email_utils import wrap_text, render_text_with_border
from .rainbow import rainbow_background
from pygame.locals import MOUSEBUTTONDOWN

# Set the dimensions of the screen
width, height = 800, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Kam Kam')

# static 'surfaces' for rainbow - should help with performance
rainbow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
rectangle_surface = pygame.Surface((width, height // 2), pygame.SRCALPHA)
rectangle_surface.fill((255, 255, 255))

# Load images once outside of the display_email function
mail_icon = pygame.image.load('images/new_mail.bmp')
mail_icon = pygame.transform.scale(mail_icon, (width, height))

def display_email(shared_dict):
    pygame.init()

    # keep track of which screen to show
    email_displayed = False

    # for the new mail animation
    animation_counter = 0
    animation_speed = 0.35
    animation_amplitude = 5  # This controls how "high" the hop is.

    # Define fonts for the body text
    font_body = pygame.font.SysFont('notosansmono', 24)

    # Variables for scrolling and touch dragging
    y_offset = 0
    dragging = False
    drag_start_y = 0
    last_y_offset = 0

    # Container to store the last 5 email bodies
    email_container = []
    current_email_index = 0

    # Define arrow button dimensions and positions
    arrow_width, arrow_height = 40, 80
    left_arrow_pos = (0, height // 2 - arrow_height // 2)
    right_arrow_pos = (width - arrow_width, height // 2 - arrow_height // 2)

    running = True

    # Define colors
    IDK = (196, 214, 227)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    counter = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return  # Exit the function if the window is closed
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if left_arrow_pos[0] <= x <= left_arrow_pos[0] + arrow_width and left_arrow_pos[1] <= y <= left_arrow_pos[1] + arrow_height:
                    current_email_index = min(current_email_index + 1, len(email_container) - 1)
                elif right_arrow_pos[0] <= x <= right_arrow_pos[0] + arrow_width and right_arrow_pos[1] <= y <= right_arrow_pos[1] + arrow_height:
                    current_email_index = max(current_email_index - 1, 0)
                else:
                    if not email_displayed:
                        email_displayed = True
                    else:
                        dragging = True
                        drag_start_y = event.pos[1]
                        last_y_offset = y_offset
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                y_offset = last_y_offset + (drag_start_y - event.pos[1])
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()

        # Check for new emails
        if shared_dict['body'] and shared_dict['body'] not in email_container:
            email_displayed = False
            email_container.insert(0, shared_dict['body'])
            if len(email_container) > 5:
                email_container.pop()
            current_email_index = 0

        # Render the body text into surfaces only if email_container is not empty
        if email_container:
            wrapped_body = wrap_text(email_container[current_email_index], font_body, width - 20 - 2 * arrow_width)
            body_lines = wrapped_body.split('\n')
            body_surfaces = [font_body.render(line, True, BLACK) for line in body_lines]

            # Draw the background and body text on the screen
            if email_displayed:
                counter += 1
                rainbow_background(screen, height, width, rainbow_surface, rectangle_surface, counter)

                # Draw each line of the body text, adjusted by the y_offset
                if counter > 50:
                    for i, body_surface in enumerate(body_surfaces):
                        screen.blit(body_surface, (10 + arrow_width, 10 + i*font_body.get_height() - y_offset))
            else:
                animation_counter += animation_speed
                y_offset = int(animation_amplitude * math.sin(animation_counter))
                screen.blit(mail_icon, (0, 0 - y_offset))

            # Draw the arrow buttons
            pygame.draw.polygon(screen, IDK, [(left_arrow_pos[0], height // 2), (left_arrow_pos[0] + arrow_width, left_arrow_pos[1]), (left_arrow_pos[0] + arrow_width, left_arrow_pos[1] + arrow_height)])
            pygame.draw.polygon(screen, IDK, [(right_arrow_pos[0], right_arrow_pos[1]), (right_arrow_pos[0], right_arrow_pos[1] + arrow_height), (right_arrow_pos[0] + arrow_width, height // 2)])

            if counter > 10000:
                counter = 80

            # Update the display
            pygame.display.flip()
            pygame.time.Clock().tick(30)
