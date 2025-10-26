"""
Game progression and win condition tracking.
Handles 30-day time limit and ranking system.
"""

class ProgressionTracker:
    def __init__(self):
        self.current_day = 1
        self.max_days = 30
        self.goal_gold = 100
        
        # Ranking thresholds
        self.ranks = {
            "S": 20,  # Complete in 20 days or less
            "A": 25,  # Complete in 25 days or less
            "B": 30,  # Complete in 30 days or less
            "F": 999, # Failed (ran out of time)
        }
        
        # Game state
        self.game_won = False
        self.game_over = False
        self.final_rank = None
        self.win_day = None
        
    def advance_day(self):
        """Move to next day."""
        if self.game_over:
            return False
        
        self.current_day += 1
        
        # Check if time ran out
        if self.current_day > self.max_days:
            self.game_over = True
            self.final_rank = "F"
            return False
        
        return True
    
    def check_win_condition(self, player_gold):
        """Check if player has reached goal."""
        if player_gold >= self.goal_gold and not self.game_won:
            self.game_won = True
            self.game_over = True
            self.win_day = self.current_day
            self.final_rank = self._calculate_rank()
            return True
        return False
    
    def _calculate_rank(self):
        """Calculate rank based on completion day."""
        if self.win_day is None:
            return "F"
        
        if self.win_day <= self.ranks["S"]:
            return "S"
        elif self.win_day <= self.ranks["A"]:
            return "A"
        elif self.win_day <= self.ranks["B"]:
            return "B"
        else:
            return "F"
    
    def get_days_remaining(self):
        """Get days left in the game."""
        return max(0, self.max_days - self.current_day + 1)
    
    def get_progress_percentage(self, player_gold):
        """Get progress toward goal as percentage."""
        return min(100, int((player_gold / self.goal_gold) * 100))
    
    def get_game_status(self, player_gold):
        """Get complete game status info."""
        return {
            "current_day": self.current_day,
            "max_days": self.max_days,
            "days_remaining": self.get_days_remaining(),
            "player_gold": player_gold,
            "goal_gold": self.goal_gold,
            "progress_percent": self.get_progress_percentage(player_gold),
            "game_won": self.game_won,
            "game_over": self.game_over,
            "final_rank": self.final_rank,
            "win_day": self.win_day,
        }
    
    def get_rank_description(self, rank):
        """Get flavor text for each rank."""
        descriptions = {
            "S": "🌟 MASTER MERCHANT! You're a trading legend!",
            "A": "⭐ EXPERT TRADER! Very impressive!",
            "B": "✓ SKILLED MERCHANT! You made it!",
            "F": "❌ OUT OF TIME! Better luck next time...",
        }
        return descriptions.get(rank, "Unknown rank")