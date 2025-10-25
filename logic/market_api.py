from .trading_logic import Market
from storage_system import StorageManager
from npc_deals import NPCDealManager
from progression import ProgressionTracker
from upgrades import UpgradeShop

_market = None
_storage = None
_npc_deals = None
_progression = None
_upgrades = None

def init(seed: int | None = None):
    # no seed used yet, but kept for future
    global _market, _storage, _npc_deals, _progression, _upgrades
    if _market is None:
        _market = Market()
        _storage = StorageManager(seed)
        _npc_deals = NPCDealManager(seed)
        _progression = ProgressionTracker()
        _upgrades = UpgradeShop()


def get_vendors():
    return list(_market.vendors.keys())

def get_vendor_stock(vendor: str):
    return dict(_market.vendors[vendor]["stock"])

def get_quote_buy(vendor: str, item: str, qty: int = 1):
    return _market.quote_buy(vendor, item, qty)

def get_quote_sell(vendor: str, item: str, qty: int = 1):
    return _market.quote_sell(vendor, item, qty)

def buy(vendor: str, item: str, qty: int = 1):
    return _market.buy(vendor, item, qty)

def sell(vendor: str, item: str, qty: int = 1):
    return _market.sell(vendor, item, qty)

def advance_day():
    # B will add this; call safely for now
    if hasattr(_market, "advance_day"):
        _market.advance_day()
    if hasattr(_market, "get_rumors_today"):
        return _market.get_rumors_today()
    return ["All quiet on the trade winds."]

def get_player_state():
    return _market.get_player_summary()

""" NEW API ADDITIONS BELOW (AMR)"""

def get_storage_info():
    return {
        "carrying_capacity": _storage.carrying_capacity,
        "carrying_used": sum(_market.player_inv.values()),
        "carrying_remaining": _storage.get_carrying_remaining(_market.player_inv),
        "home_capacity": _storage.get_total_home_capacity(),
        "home_used": _storage.get_home_storage_used(),
        "home_remaining": _storage.get_home_storage_remaining(),
        "home_storage": dict(_storage.home_storage),
        "guard_active": _storage.guard_service_active,
    }

def store_item(item: str, qty: int):
    """Move item from player inventory to home storage."""
    if _market.player_inv.get(item, 0) < qty:
        raise ValueError("Not enough in inventory")
    
    _storage.store_item(item, qty)
    _market.player_inv[item] -= qty
    if _market.player_inv[item] == 0:
        del _market.player_inv[item]
    
    return True

def retrieve_item(item: str, qty: int):
    """Move item from home storage to player inventory."""
    remaining = _storage.get_carrying_remaining(_market.player_inv)
    if remaining < qty:
        raise ValueError(f"Can only carry {remaining} more items")
    
    _storage.retrieve_item(item, qty)
    _market.player_inv[item] = _market.player_inv.get(item, 0) + qty
    
    return True

def hire_guard():
    """Hire guard service for 2 gold."""
    cost = _storage.hire_guard(_market.player_gold)
    _market.player_gold -= cost
    return cost

# Add API functions for NPC deals
def get_active_deal():
    """Get current tavern deal if available."""
    return _npc_deals.get_active_deal()

def get_deal_appraisal():
    """Get scam probability if appraisal skill purchased."""
    deal = _npc_deals.get_active_deal()
    if not deal:
        return None
    return _npc_deals.reveal_scam_probability(deal)

def accept_deal():
    """Accept current tavern deal."""
    deal = _npc_deals.get_active_deal()
    if not deal:
        raise ValueError("No active deal")
    
    # Calculate price based on deal
    base_price = _market.items[deal["item"]]["base_price"]
    cost = _npc_deals.get_deal_price(deal, base_price)
    
    if _market.player_gold < cost:
        raise ValueError("Not enough gold")
    
    # Process the deal
    result = _npc_deals.accept_deal(deal, _market.player_gold)
    
    # Charge player
    _market.player_gold -= cost
    
    # Give items (actual item if scam)
    item_received = result["actual_item"]
    qty_received = result["quantity"]
    
    # Add to inventory
    _market.player_inv[item_received] = _market.player_inv.get(item_received, 0) + qty_received
    
    # If low_quality scam, mark items somehow (future feature)
    
    return {
        "cost": cost,
        "received_item": item_received,
        "received_qty": qty_received,
        "was_scam": result["is_scam"],
        "scam_type": result.get("scam_type"),
    }

def decline_deal():
    """Decline current tavern deal."""
    _npc_deals.decline_deal()

# Add API functions for progression
def get_game_status():
    """Get current game progress."""
    return _progression.get_game_status(_market.player_gold)

def check_win():
    """Check if player has won."""
    return _progression.check_win_condition(_market.player_gold)

# Add API functions for upgrades
def get_available_upgrades():
    """Get list of purchasable upgrades."""
    return _upgrades.get_available_upgrades()

def purchase_upgrade(upgrade_key: str):
    """Buy an upgrade."""
    success, cost, msg = _upgrades.purchase_upgrade(upgrade_key, _market.player_gold)
    
    if not success:
        raise ValueError(msg)
    
    # Deduct gold
    _market.player_gold -= cost
    
    # Apply upgrade effects
    if upgrade_key == "small_chest":
        _storage.upgrades["small_chest"] = True
    elif upgrade_key == "large_chest":
        _storage.upgrades["large_chest"] = True
    elif upgrade_key == "appraisal_skill":
        _npc_deals.has_appraisal_skill = True
    
    return msg

# Modify advance_day() to include new systems
def advance_day():
    # Existing day advancement
    if hasattr(_market, "advance_day"):
        _market.advance_day()
    
    # Progress day counter
    _progression.advance_day()
    
    # Check for theft
    theft_occurred, stolen_items, loss = _storage.check_theft(_market.items)
    
    # Deactivate guard
    _storage.deactivate_guard()
    
    # Advance NPC deals
    _npc_deals.advance_day()
    
    # Get rumors
    rumors = []
    if hasattr(_market, "get_rumors_today"):
        rumors = _market.get_rumors_today()
    
    # Build event summary
    events = {
        "rumors": rumors,
        "theft": {
            "occurred": theft_occurred,
            "stolen": stolen_items,
            "loss_value": loss,
        },
        "new_deal": _npc_deals.get_active_deal() is not None,
    }
    
    return events
