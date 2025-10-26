"""
Upgrade shop system for storage and skills.
"""

class UpgradeShop:
    def __init__(self):
        self.upgrades = {
            "small_chest": {
                "cost": 15,
                "name": "Small Chest",
                "description": "Increases home storage by +10 items",
                "purchased": False,
            },
            "large_chest": {
                "cost": 40,
                "name": "Large Chest",
                "description": "Increases home storage by +20 items",
                "purchased": False,
                "requires": "small_chest",  # Must buy small first
            },
            "appraisal_skill": {
                "cost": 15,
                "name": "Appraisal Skill",
                "description": "Reveals scam probability for NPC deals",
                "purchased": False,
            },
        }
    
    def get_available_upgrades(self):
        """Get list of upgrades that can be purchased."""
        available = []
        for key, upgrade in self.upgrades.items():
            if upgrade["purchased"]:
                continue
            
            # Check requirements
            if "requires" in upgrade:
                if not self.upgrades[upgrade["requires"]]["purchased"]:
                    continue
            
            available.append({
                "key": key,
                **upgrade
            })
        
        return available
    
    def can_purchase(self, upgrade_key, player_gold):
        """Check if player can afford and is eligible for upgrade."""
        if upgrade_key not in self.upgrades:
            return False, "Unknown upgrade"
        
        upgrade = self.upgrades[upgrade_key]
        
        if upgrade["purchased"]:
            return False, "Already purchased"
        
        if "requires" in upgrade:
            if not self.upgrades[upgrade["requires"]]["purchased"]:
                return False, f"Requires {upgrade['requires']} first"
        
        if player_gold < upgrade["cost"]:
            return False, f"Not enough gold (need {upgrade['cost']})"
        
        return True, "OK"
    
    def purchase_upgrade(self, upgrade_key, player_gold):
        """
        Purchase an upgrade.
        Returns: (success: bool, cost: int, message: str)
        """
        can_buy, msg = self.can_purchase(upgrade_key, player_gold)
        
        if not can_buy:
            return False, 0, msg
        
        upgrade = self.upgrades[upgrade_key]
        cost = upgrade["cost"]
        
        self.upgrades[upgrade_key]["purchased"] = True
        
        return True, cost, f"Purchased {upgrade['name']}!"