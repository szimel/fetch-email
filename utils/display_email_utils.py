import pygame

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

def wrap_text(text, font, max_width):
    words = text.split(' ')
    wrapped_lines = []
    current_line = words[0]
   
    for word in words[1:]:
        # Test the width with the new word added
        test_line = current_line + ' ' + word
        # If the width with the new word doesn't exceed the max width
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word

    wrapped_lines.append(current_line)
    return '\n'.join(wrapped_lines)