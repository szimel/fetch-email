import pygame
import random

# Define the colors
colors = [(229, 213, 213), (219, 170, 166), (247, 220, 174), (194, 219, 208), (196, 214, 227), (255, 255, 255)]
heart_colors = [(229, 213, 213), (219, 170, 166), (247, 220, 174), (194, 219, 208), (196, 214, 227)]

# Define the rain
rain_right = []
rain_left = []

# Load the heart and cloud images
heart_image = pygame.image.load('images/test_heart2.png')
heart_image = pygame.transform.scale(heart_image, (22, 22))

def colorize(image, new_color):
    # Create a new surface with the same dimensions as the `image`
    colorized_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    
    # Fill the new surface with the `new_color`
    colorized_image.fill(new_color)
    
    # Blit the `image` onto the `colorized_image` with the `BLEND_RGBA_MULT` flag
    colorized_image.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    return colorized_image

# Create a dictionary of colorized hearts
colorized_hearts = {color: colorize(heart_image, color) for color in heart_colors}

def rainbowAnimation(surface, counter, width, height):
    for i, color in enumerate(colors):
        pygame.draw.circle(surface, color, (width//2, height//2), (counter * 3) + (len(colors) - i - 1) * 30)


def rainAnimation(screen, counter):
    global rain_right, rain_left

    # set coordinates for rain
    if counter % 10 == 0: 
        #right rain coordinates & y
        right_loc_x = random.randrange(135, 275)
        rain_loc_y = 245

        #right rain color
        right_color = random.choice(heart_colors)


        #append rain to list
        rain_right.append([right_loc_x, rain_loc_y, right_color])

    if (counter + 5) % 10 == 0:
        #left rain coordinates & y
        left_loc_x = random.randrange(525, 665)
        rain_loc_y = 245

        #left rain color
        left_color = random.choice(heart_colors)

        #append rain to list
        rain_left.append([left_loc_x, rain_loc_y, left_color])

    # update and draw rain positions
    for rain_list in [rain_right, rain_left]:
        new_rain_list = []
        for rain in rain_list:
            rain[1] += 6
            if rain[1] <= 505:
                image = colorized_hearts[rain[2]]
                screen.blit(image, (rain[0]-image.get_width()//2, rain[1]-image.get_height()//2))
                new_rain_list.append(rain)
        if rain_list is rain_right:
            rain_right = new_rain_list
        else:
            rain_left = new_rain_list

            