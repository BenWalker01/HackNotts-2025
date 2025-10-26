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

def draw_textbox_(screen, ui_assets):
    # Get the screen dimensions
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    
    # Calculate position to center the scroll panel
    scroll_x = (screen_width - ui_assets.scroll_panel.get_width()) // 2
    scroll_y = (screen_height - ui_assets.scroll_panel.get_height()) // 2
    
    # Draw the scroll panel centered
    screen.blit(ui_assets.scroll_panel, (scroll_x, scroll_y))

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
    
    
