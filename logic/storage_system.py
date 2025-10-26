"""
Storage system for player's home.
Handles inventory capacity, home storage, and theft mechanics.
"""

import random

class StorageManager:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        
        # Home storage
        self.home_capacity = 12
        self.home_storage = {}  # {item: quantity}
        
        # Upgrades
        self.upgrades = {
            "small_chest": False,  # +10 capacity
            "large_chest": False,  # +20 capacity
        }
        
        # Theft protection
        self.guard_service_active = False
        self.theft_chance = 0.05  # 5% base chance
        self.theft_threshold = 70  # Gold value threshold
        
    def get_total_home_capacity(self):
        """Calculate current home storage capacity including upgrades."""
        capacity = self.home_capacity
        if self.upgrades["small_chest"]:
            capacity += 10
        if self.upgrades["large_chest"]:
            capacity += 20
        return capacity
    
    def get_home_storage_used(self):
        """Count items currently in home storage."""
        return sum(self.home_storage.values())
    
    def get_home_storage_remaining(self):
        """Get available home storage space."""
        return self.get_total_home_capacity() - self.get_home_storage_used()
    
    # ---------- Storage operations ----------
    
    def store_item(self, item, qty):
        """Move items from player to home storage."""
        if self.get_home_storage_remaining() < qty:
            raise ValueError(f"Not enough home storage space (need {qty}, have {self.get_home_storage_remaining()})")
        
        self.home_storage[item] = self.home_storage.get(item, 0) + qty
        return True
    
    def retrieve_item(self, item, qty):
        """Move items from home storage to player inventory."""
        if self.home_storage.get(item, 0) < qty:
            raise ValueError(f"Not enough {item} in home storage")
        
        self.home_storage[item] -= qty
        if self.home_storage[item] == 0:
            del self.home_storage[item]
        return True
    
    # ---------- Theft mechanics ----------
    
    def calculate_storage_value(self, items_data):
        """Calculate total gold value of items in home storage."""
        total_value = 0
        for item, qty in self.home_storage.items():
            if item in items_data:
                total_value += items_data[item]["base_price"] * qty
        return total_value
    
    def check_theft(self, items_data):
        """
        Check if theft occurs during the night.
        Returns: (theft_occurred: bool, stolen_items: dict, total_loss: int)
        """
        storage_value = self.calculate_storage_value(items_data)
        
        # No theft if below threshold or guard active
        if storage_value < self.theft_threshold or self.guard_service_active:
            return False, {}, 0
        
        # Roll for theft
        if self.rng.random() < self.theft_chance:
            return self._execute_theft(items_data)
        
        return False, {}, 0
    
    def _execute_theft(self, items_data):
        """Execute a theft event - steal 1-3 random items."""
        if not self.home_storage:
            return False, {}, 0
        
        # Randomly select 1-3 items to steal
        available_items = list(self.home_storage.keys())
        num_stolen = min(self.rng.randint(1, 3), len(available_items))
        
        stolen_items = {}
        total_loss = 0
        
        for _ in range(num_stolen):
            if not available_items:
                break
            
            item = self.rng.choice(available_items)
            available_items.remove(item)
            
            # Steal 1-3 of this item (or all if less)
            qty_to_steal = min(self.rng.randint(1, 3), self.home_storage[item])
            
            stolen_items[item] = qty_to_steal
            total_loss += items_data[item]["base_price"] * qty_to_steal
            
            # Remove from storage
            self.home_storage[item] -= qty_to_steal
            if self.home_storage[item] == 0:
                del self.home_storage[item]
        
        return True, stolen_items, total_loss
    
    # ---------- Guard service ----------
    
    def hire_guard(self, player_gold, cost=5):
        """Hire guard service for one day."""
        if player_gold < cost:
            raise ValueError("Not enough gold to hire guard")
        
        self.guard_service_active = True
        return cost
    
    def deactivate_guard(self):
        """Called at end of day - guard service expires."""
        self.guard_service_active = False