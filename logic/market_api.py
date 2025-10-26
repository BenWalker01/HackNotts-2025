from .trading_logic import Market
from .storage_system import StorageManager
from .npc_deals import NPCDealManager
from .progression import ProgressionTracker
from .upgrades import UpgradeShop
from .difficulty import DIFFICULTIES

_market = None
_storage = None
_npc_deals = None
_progression = None
_upgrades = None
_world = None
_curr_diff_key = "merchant"

def init(seed: int | None = 44, difficulty: str = "merchant"):
    global _market, _storage, _npc_deals, _progression, _upgrades, _world, _curr_diff_key
    if difficulty not in DIFFICULTIES:
        raise ValueError(f"Unknown difficulty '{difficulty}'")
    _curr_diff_key = difficulty
    if _world is None:
        tune = DIFFICULTIES[difficulty]
        _world = _GameWorld(seed=seed, tune=tune)
        # point API globals at the tuned world
        _market = _world.market
        _storage = _world.storage
        _npc_deals = _world.deals
        _progression = _world.progress
        _upgrades = _world.upgrades

class _GameWorld:
    def __init__(self, seed=None, tune=None):
        from .trading_logic import Market
        from .storage_system import StorageManager
        from .progression import ProgressionTracker
        from .upgrades import UpgradeShop
        from .npc_deals import NPCDealManager

        self.market = Market(seed=seed, tune=tune)
        self.storage = StorageManager(seed=seed, tune=tune)
        self.progress = ProgressionTracker()
        self.upgrades = UpgradeShop()
        self.deals = NPCDealManager(seed=seed, tune=tune)

def reset_world():
    """Wipe everything so the next init() creates a brand-new tuned world."""
    global _world, _market, _storage, _npc_deals, _progression, _upgrades
    _world = _market = _storage = _npc_deals = _progression = _upgrades = None

def get_difficulty():
    return _curr_diff_key


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

def get_player_state():
    return _market.get_player_summary()

def force_event(key: str | None):
    """Debug: force an event by key (or None to clear)."""
    return _market.force_event(key)

def list_events():
    """Debug: list available event keys."""
    return _market.list_event_keys()

def get_buy_snapshot(vendor: str):
    stock = get_vendor_stock(vendor)
    rows = []
    for item, qty in stock.items():
        if qty <= 0: 
            continue
        rows.append({
            "item": item,
            "qty": qty,
            "buy_price": get_quote_buy(vendor, item, 1),
            "weight": _market._item_weight(item)
        })
    # Sort by category then name if you like; here we keep as-is
    return rows

def get_sell_snapshot(vendor: str):
    inv = get_player_state()["inventory"]
    rows = []
    for item, qty in inv.items():
        rows.append({
            "item": item,
            "qty": qty,
            "sell_price": get_quote_sell(vendor, item, 1),
            "weight": _market._item_weight(item)
        })
    return rows

def get_today_news_and_rumours():
    return {"news": _market.get_news_today(), "rumors": _market.get_rumors_today()}


""" NEW API ADDITIONS BELOW (AMR)"""

def get_storage_info():
    ps = _market.get_player_summary()  # gold, weight, capacity, inventory
    return {
        "home_capacity": _storage.get_total_home_capacity(),
        "home_used": _storage.get_home_storage_used(),
        "home_remaining": _storage.get_home_storage_remaining(),
        "home_storage": dict(_storage.home_storage),
        "guard_active": _storage.guard_service_active,
        # weight-based carry (source of truth = Market)
        "carrying_capacity": ps["capacity"],
        "carrying_used": ps["weight"],
        "carrying_remaining": max(0.0, ps["capacity"] - ps["weight"]),
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
    weight = _market._item_weight(item) * qty
    ps = _market.get_player_summary()
    new_weight = ps["weight"] + weight
    if new_weight > ps["capacity"]:
        raise ValueError(f"Inventory too heavy ({new_weight:.1f}/{ps['capacity']:.1f})")
    _storage.retrieve_item(item, qty)
    _market.player_inv[item] = _market.player_inv.get(item, 0) + qty
    return True

def hire_guard():
    """Hire guard service for 2 gold."""
    cost = _storage.hire_guard(_market.player_gold, cost=_storage.guard_cost)
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
    
    news = _market.get_news_today()
    rumors = _market.get_rumors_today()
    
    return {
        "news": news,
        "rumors": rumors,    
        "theft": {"occurred": theft_occurred, "stolen": stolen_items, "loss_value": loss},
        "new_deal": _npc_deals.get_active_deal() is not None,
        "status": _progression.get_game_status(_market.player_gold)
    }
