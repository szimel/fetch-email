import pygame
import math
from utils.display_email_utils import wrap_text
from .rainbow import rainbow_background
from pygame.locals import MOUSEBUTTONDOWN
import os

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

# Define arrow button dimensions and positions
arrow_width, arrow_height = 40, 80
left_arrow_pos = (0, height // 2 - arrow_height // 2)
right_arrow_pos = (width - arrow_width, height // 2 - arrow_height // 2)

# Determine the base directory dynamically
base_dir = os.path.dirname(os.path.abspath(__file__))

clock = pygame.time.Clock()

# def cleanup_images(email_container, image_directory):
    # # Step 1: Identify images to keep
    # kept_images = [email['image_path'] for email in email_container if email['image_path'] is not None]

    # # Step 2: List all images in the directory
    # all_images = os.listdir(image_directory)

    # print(image_directory)

    # # Step 3: Delete unlinked images
    # for image in all_images:
    #     print('got here')
    #     image_path = os.path.join(image_directory, image)
    #     relative_image_path = os.path.relpath(image_path, image_directory)  # get the relative path
    #     if relative_image_path not in kept_images:
    #         print(f'Deleting {image_path}')
    #         os.remove(image_path)

MAX_WIDTH = 700

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

    running = True

    # Define colors
    IDK = (196, 214, 227)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    counter = 0

    image_directory = "stored-images" # Directory to store images

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
        new_email = {'body': shared_dict['body'], 'image_path': shared_dict['image_path']}
        if new_email not in email_container:
            email_displayed = False
            email_container.insert(0, new_email)
            if len(email_container) > 1:
                print('popped!')
                email_container.pop()
                # cleanup_images(email_container, image_directory)
            current_email_index = 0

        # Render the body text into surfaces only if email_container is not empty
        if email_container:
            current_email = email_container[current_email_index]
            wrapped_body = wrap_text(current_email['body'], font_body, width - 20 - 2 * arrow_width)
            body_lines = wrapped_body.split('\n')
            body_surfaces = [font_body.render(line, True, BLACK) for line in body_lines]

            if email_displayed:
                counter += 1
                rainbow_background(screen, height, width, rainbow_surface, rectangle_surface, counter)

                # Draw each line of the body text, adjusted by the y_offset
                if counter > 50:
                    for i, body_surface in enumerate(body_surfaces):
                        position = (10 + arrow_width, 10 + i*font_body.get_height() * 1.5 - y_offset)
                        screen.blit(body_surface, position)

                    # Calculate total text height
                    text_height = len(body_surfaces) * font_body.get_height() * 1.5
                    
                    image_path = current_email['image_path']
                    if image_path is not None:
                        image_path = os.path.join(base_dir, image_path)
                        image = pygame.image.load(image_path)
                        # Get the dimensions of the image
                        img_width, img_height = image.get_size()
                        
                        # Calculate the scaling factor to resize the image to the desired width
                        scaling_factor = MAX_WIDTH / img_width if img_width > MAX_WIDTH else 1
                        
                        # Calculate the new dimensions
                        new_width = int(img_width * scaling_factor)
                        new_height = int(img_height * scaling_factor)
                        
                        # Resize the image
                        image = pygame.transform.scale(image, (new_width, new_height))
                        
                        image_position = (10 + arrow_width, 10 + text_height - y_offset)
                        screen.blit(image, image_position)
                
                # Draw the arrow buttons
                pygame.draw.polygon(screen, IDK, [(left_arrow_pos[0], height // 2), (left_arrow_pos[0] + arrow_width, left_arrow_pos[1]), (left_arrow_pos[0] + arrow_width, left_arrow_pos[1] + arrow_height)])
                pygame.draw.polygon(screen, IDK, [(right_arrow_pos[0], right_arrow_pos[1]), (right_arrow_pos[0], right_arrow_pos[1] + arrow_height), (right_arrow_pos[0] + arrow_width, height // 2)])
            else:
                # Reset the counter and clear the screen with a white background
                counter = 0
                screen.fill(WHITE)  # Clear the screen with white color
                rainbow_surface.fill((0, 0, 0, 0))  # Clear the rainbow_surface with transparent color

                animation_counter += animation_speed
                y_offset = int(animation_amplitude * math.sin(animation_counter))
                screen.blit(mail_icon, (0, 0 - y_offset))

            if counter > 10000:
                counter = 80

            # Update the display
            pygame.display.flip()
            clock.tick(30)
