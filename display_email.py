import pygame
import math
from email_utils import wrap_text, send_email

global subject, body
subject = ''
body = ''

def render_text_with_border(text, font, text_color, border_color):
    # Render the text in the border color
    text_surface = font.render(text, True, border_color)
    border_surface = pygame.Surface((text_surface.get_width() + 4, text_surface.get_height() + 4))
    for x in range(-2, 3):
        for y in range(-2, 3):
            border_surface.blit(text_surface, (x + 2, y + 2))
    # Render the text in the main color
    text_surface = font.render(text, True, text_color)
    border_surface.blit(text_surface, (2, 2))
    return border_surface

def update_vars(new_subject, new_body):
    global subject, body
    subject = new_subject
    body = new_body
        
# Load images once outside of the display_email function
mail_icon = pygame.image.load('new_mail.jpeg')
mail_icon = pygame.transform.scale(mail_icon, (480, 320))
background = pygame.image.load("background_1.jpeg")
background = pygame.transform.scale(background, (480, 320))


def display_email():
    pygame.init()
    
    # Set the dimensions of the screen
    width, height = 480, 320
    screen = pygame.display.set_mode((width, height))
    
    # keep track of which screen to show
    email_displayed = False
    # for the new mail animation
    animation_counter = 0
    animation_speed = 0.035
    animation_amplitude = 5  # This controls how "high" the hop is.
    
    # Define fonts for the body text
    font_body = pygame.font.SysFont('notosansmono', 19)
    
    # Variables for scrolling and touch dragging
    y_offset = 0
    dragging = False
    drag_start_y = 0
    last_y_offset = 0

    prev_body = None
    body_surfaces = None

    running = True
    
    # Define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREY = (250, 250, 250)
    
    while running:
        # ... at the beginning of the while loop ...
        if body != prev_body:
            email_displayed = False
            prev_body = body

            # Render the body text into surfaces
            wrapped_body = wrap_text(body, font_body, width - 20)
            body_lines = wrapped_body.split('\n')
            body_surfaces = [render_text_with_border(line, font_body, BLACK, WHITE) for line in body_lines]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return  # Exit the function if the window is closed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not email_displayed:
                    print('right one')
                    email_displayed = True
                    # send_email(subject, body)
                else: 
                    dragging = True
                    drag_start_y = event.pos[1]
                    last_y_offset = y_offset
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                y_offset = last_y_offset + (drag_start_y - event.pos[1])

        # Draw the background and body text on the screen
        if email_displayed:
            screen.blit(background, (0, 0))

            # Draw each line of the body text, adjusted by the y_offset
            for i, body_surface in enumerate(body_surfaces):
                screen.blit(body_surface, (10, 10 + i*font_body.get_height() - y_offset))
        else:
            animation_counter += animation_speed
            y_offset = int(animation_amplitude * math.sin(animation_counter))
            screen.blit(mail_icon, (0, 0 - y_offset))

        # Update the display
        pygame.display.flip()
