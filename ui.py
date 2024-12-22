from graphics import *

class UI:
    def __init__(self, graphics):
        self.graphics = graphics
        self.screen = graphics.screen

    def draw_dialog(self, message, width=600, height=200, padding=10):
        """
        Draws a dialog window with a message, handling text wrapping.

        Args:
            screen: The game screen.
            message: The message to display.
            width: The width of the dialog box.
            height: The height of the dialog box.
            padding: The padding between the text and the dialog box border.
        """
        # Colors
        background_color = (50, 50, 50)
        border_color = (200, 200, 200)
        text_color = (255, 255, 255)

        # Get screen dimensions
        screen_width, screen_height = self.screen.get_size()

        # Dialog position
        x = (screen_width - width) // 2
        y = screen_height - height - 20  # Place near the bottom

        # Draw dialog background
        pygame.draw.rect(self.screen, background_color, (x, y, width, height))

        # Draw border
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 3)

        # Render wrapped text
        font = pygame.font.Font(None, 24)
        text_lines = wrap_text(message, font, width - 2 * padding)

        # Draw each line of text
        line_height = font.get_linesize()
        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, text_color)
            text_rect = text_surface.get_rect(topleft=(x + padding, y + padding + i * line_height))
            self.screen.blit(text_surface, text_rect)

def wrap_text(text, font, max_width):
    """
    Wraps text into multiple lines that fit within a given width.
    Args:
        text: The text to wrap.
        font: The pygame font object.
        max_width: The maximum width for each line of text.
    Returns:
        A list of strings, where each string is a line of wrapped text.
    """
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


