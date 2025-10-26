# game_state.py
import pygame
from logic import market_api as api

class GameState:
    def __init__(self):
        api.init()
        
        # Game modes
        self.current_mode = "Menu"  # GAMEPLAY, TRADING, INVENTORY, STORAGE, UPGRADES
        
        # Location tracking
        self.current_location = None  # "market", "tavern", "home", etc.
        
        # UI state
        self.trading_vendor = None
        self.show_inventory = False
        
    def handle_interaction(self, player):
        """Called when player presses E near something."""
        # Check if near any NPCs/buildings
        location = self.detect_location(player)
        
        if location == "market":
            self.open_trading_ui("Trader Zara")
        elif location == "home":
            self.open_storage_ui()
        elif location == "tavern":
            self.check_for_deals()
    

    
    def open_trading_ui(self, vendor):
        self.current_mode = "TRADING"
        self.trading_vendor = vendor
    
    def draw_ui(self, screen):
        """Render all UI elements."""
        # Always draw HUD
        self.draw_hud(screen)
        
        # Draw mode-specific UI
        if self.current_mode == "TRADING":
            self.draw_trading_ui(screen)
        elif self.show_inventory:
            self.draw_inventory_ui(screen)
    
    def draw_hud(self, screen):
        """Draw top bar with gold, day, etc."""
        font = pygame.font.Font(None, 24)
        player_state = api.get_player_state()
        game_status = api.get_game_status()
        
        # Gold
        gold_text = font.render(f"Gold: {player_state['gold']}", True, (255, 215, 0))
        screen.blit(gold_text, (10, 10))
        
        # Day
        day_text = font.render(f"Day: {game_status['current_day']}/{game_status['max_days']}", True, (255, 255, 255))
        screen.blit(day_text, (200, 10))
