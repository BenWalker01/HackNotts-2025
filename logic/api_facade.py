from trading_logic import Market

_market = None

def init(seed: int | None = None):
    # no seed used yet, but kept for future
    global _market
    if _market is None:
        _market = Market()

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
    return {
        "gold": _market.player_gold,
        "inventory": dict(_market.player_inv),
    }
