"""
NPC deals and scams system for the Tavern.
Generates random offers with good deals and potential scams.
"""

import random

class NPCDealManager:
    def __init__(self, seed=None):
        self.rng = random.Random(seed)
        
        # Current active deal
        self.active_deal = None
        self.days_until_next_deal = self._roll_next_deal_day()
        
        # Appraisal skill
        self.has_appraisal_skill = False
        
    def _roll_next_deal_day(self):
        """Random 3-5 days until next deal appears."""
        return self.rng.randint(3, 5)
    
    # ---------- Deal generation ----------
    
    def advance_day(self):
        """Called when day advances. Check if new deal appears."""
        self.days_until_next_deal -= 1
        
        if self.days_until_next_deal <= 0:
            self.active_deal = self._generate_deal()
            self.days_until_next_deal = self._roll_next_deal_day()
        else:
            self.active_deal = None
    
    def _generate_deal(self):
        """Generate a new deal (60% good, 40% scam)."""
        is_scam = self.rng.random() > 0.6
        
        if is_scam:
            return self._generate_scam()
        else:
            return self._generate_good_deal()
    
    def _generate_good_deal(self):
        """Generate a legitimate good deal."""
        deal_types = [
            {
                "type": "bulk_discount",
                "item": self.rng.choice(["spices", "cloth", "iron", "leather"]),
                "quantity": 3,
                "discount": 0.33,  # Buy 3 for price of 2
                "description": "A traveling merchant offers you bulk goods at a discount!",
            },
            {
                "type": "percentage_off",
                "item": self.rng.choice(["wood", "salt", "ale", "wheat"]),
                "quantity": self.rng.randint(2, 5),
                "discount": self.rng.choice([0.15, 0.20, 0.25]),
                "description": "A fellow trader wants to clear old stock quickly!",
            },
        ]
        
        deal = self.rng.choice(deal_types)
        deal["is_scam"] = False
        deal["npc_name"] = self.rng.choice([
            "Honest Tom", "Merchant Mary", "Trader Bill", "Lady Eleanor"
        ])
        return deal
    
    def _generate_scam(self):
        """Generate a scam deal."""
        scam_types = [
            {
                "type": "fake_item",
                "item": "spices",  # Advertised item
                "actual_item": "wheat",  # What you actually get
                "quantity": 2,
                "discount": 0.30,  # Seems too good to be true
                "description": "A suspicious figure offers 'rare exotic spices' at an unbelievable price...",
                "tell": "The merchant avoids eye contact and fidgets nervously.",
            },
            {
                "type": "low_quality",
                "item": self.rng.choice(["iron", "cloth", "leather"]),
                "quantity": 3,
                "discount": 0.40,  # Very suspicious discount
                "value_multiplier": 0.5,  # Worth only half when you try to sell
                "description": "A merchant guarantees 'premium quality' goods at a steep discount!",
                "tell": "The goods look slightly damaged or worn.",
            },
        ]
        
        scam = self.rng.choice(scam_types)
        scam["is_scam"] = True
        scam["npc_name"] = self.rng.choice([
            "Shifty Pete", "Mysterious Stranger", "Hooded Figure", "Nervous Ned"
        ])
        return scam
    
    # ---------- Deal interaction ----------
    
    def get_active_deal(self):
        """Get current deal if one exists."""
        return self.active_deal
    
    def get_deal_price(self, deal, base_price):
        """Calculate discounted price for a deal."""
        total_base = base_price * deal["quantity"]
        discount_amount = total_base * deal["discount"]
        return int(total_base - discount_amount)
    
    def reveal_scam_probability(self, deal):
        """Use appraisal skill to detect if deal is suspicious."""
        if not self.has_appraisal_skill:
            return None
        
        if deal["is_scam"]:
            # Appraisal reveals 80% chance it's a scam
            return self.rng.uniform(0.70, 0.90)
        else:
            # Legit deals show low risk
            return self.rng.uniform(0.05, 0.20)
    
    def accept_deal(self, deal, player_gold):
        """
        Accept a deal.
        Returns: (success: bool, item_received: str, qty_received: int, cost: int, was_scam: bool)
        """
        if not deal:
            raise ValueError("No active deal")
        
        # Calculate cost (we'll need base_price from items, pass it in or calculate)
        # For now, return the deal info for the caller to handle payment
        
        result = {
            "is_scam": deal["is_scam"],
            "advertised_item": deal["item"],
            "quantity": deal["quantity"],
        }
        
        if deal["is_scam"]:
            if deal["type"] == "fake_item":
                result["actual_item"] = deal["actual_item"]
                result["scam_type"] = "fake_item"
            elif deal["type"] == "low_quality":
                result["actual_item"] = deal["item"]
                result["value_multiplier"] = deal["value_multiplier"]
                result["scam_type"] = "low_quality"
        else:
            result["actual_item"] = deal["item"]
        
        # Clear the deal after accepting
        self.active_deal = None
        
        return result
    
    def decline_deal(self):
        """Decline the current deal."""
        self.active_deal = None