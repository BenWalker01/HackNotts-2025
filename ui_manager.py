import pygame
import os

class Button:
    def __init__(self, x, y, width, height, text, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        font_path = os.path.join('assets', 'font.ttf')
        self.is_hovered = False
        self.normal_font = pygame.font.Font(font_path, font_size)
        self.bold_font = pygame.font.Font(font_path, font_size + 8)
        
    def draw(self, screen):
        # Choose font based on hover state
        current_font = self.bold_font if self.is_hovered else self.normal_font
        
        # Render text
        text_surface = current_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Draw text
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class UIAssets: # ADD ALL UR ASSETS/PANELS HERE
    def __init__(self):
        # Load and scale the wood panel
        menu_path = os.path.join('assets', 'ui', 'fantasy_pixelart', 'panels', 'wood_panel.png')
        self.menu_panel = pygame.image.load(menu_path)
        self.menu_panel = pygame.transform.scale(self.menu_panel, (600, 600))
        

        hud_path = os.path.join('assets', 'ui','hud_panel.png')
        self.hud_panel = pygame.image.load(hud_path)
        self.hud_panel = pygame.transform.scale(self.hud_panel, (768, 128))

        scroll_path = os.path.join('assets', 'ui','square_scroll_panel.png')
        self.scroll_panel = pygame.image.load(scroll_path)
        self.scroll_panel = pygame.transform.scale(self.scroll_panel, (650,600))

        
        # Create buttons
        self.start_button = None  # Will be initialized in draw_menu_UI
        


def draw_hud_UI(screen, ui_assets):
    # Get the screen dimensions
    screen_width = screen.get_width()
    
    # Position HUD panel at top-right corner
    hud_x = screen_width - ui_assets.hud_panel.get_width()
    hud_y = 0
    
    # Draw the HUD panel
    screen.blit(ui_assets.hud_panel, (hud_x, hud_y))

def _blit_wrapped_text(screen, text, font, color, rect, line_height=4):
    """Render text inside rect with word-wrapping. Returns the last y used."""
    x, y, w, h = rect
    space = font.size(" ")[0]
    max_width = w
    words = text.split(" ")
    line = ""
    cur_y = y
    for word in words:
        test = f"{line}{word} "
        if font.size(test)[0] <= max_width:
            line = test
        else:
            surf = font.render(line.rstrip(), True, color)
            screen.blit(surf, (x, cur_y))
            cur_y += surf.get_height() + line_height
            line = f"{word} "
    if line:
        surf = font.render(line.rstrip(), True, color)
        screen.blit(surf, (x, cur_y))
        cur_y += surf.get_height() + line_height
    return cur_y

def draw_textbox_(screen, ui_assets, text: str):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    # Center scroll panel
    sw, sh = screen.get_width(), screen.get_height()
    panel = ui_assets.scroll_panel
    px = (sw - panel.get_width()) // 2
    py = (sh - panel.get_height()) // 2
    screen.blit(panel, (px, py))

    # Text area with padding
    pad = 28
    text_rect = pygame.Rect(
        px + pad, py + pad, panel.get_width() - 2 * pad, panel.get_height() - 2 * pad
    )

    # Load a readable font
    font_path = os.path.join('assets', 'font.ttf')
    font = pygame.font.Font(font_path, 22)

    # Header (optional)
    header = "Common-Folk Talk"
    header_surf = font.render(header, True, (56, 34, 12))
    screen.blit(header_surf, (text_rect.x, text_rect.y))
    body_rect = text_rect.copy()
    body_rect.y += header_surf.get_height() + 8

    # Body
    _blit_wrapped_text(screen, text, font, (28, 16, 8), body_rect)

def draw_menu_UI(screen, ui_assets):
    # Get the screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Calculate position to center the panel
    panel_x = (screen_width - 600) // 2
    panel_y = (screen_height - 600) // 2
    
    # Draw the wood panel

    screen.blit(ui_assets.menu_panel, (panel_x, panel_y))
    
    # Initialize button if not exists
    if ui_assets.start_button is None:
        button_x = screen_width // 2 - 100
        button_y = screen_height // 2 - 25
        ui_assets.start_button = Button(button_x, button_y, 200, 50, "Start Game")
    
    # Draw button
    ui_assets.start_button.draw(screen)
    
    return ui_assets.start_button
    
    
