import json
import math
import os
import random
from .economy_bootstrap import ITEMS, VENDORS

class Market:
    def __init__(self):
        self.items = ITEMS
        self.vendors = {
            name: {
                "stock": {
                    product: max(0, quantity//2)
                    for product, quantity in data["target_stock"].items()
                }
            } for name, data in VENDORS.items()
        }
        self.player_gold = 60
        self.player_inv = {}

        self.margin_sell = 0.15  # vendor markup
        self.margin_buy  = 0.10  # vendor buys cheaper

        self.rng = random.Random(42)
        events_path = os.path.join(os.path.dirname(__file__), "events_seeds.json")
        self._events = self._load_events(events_path)

        self.player_capacity = 30.0  # simple starting carry capacity (tweak later)

        self._today_event = None

    # ---------- validation helpers ----------
    def _require_vendor(self, vendor: str):
        if vendor not in self.vendors:
            raise ValueError(f"Unknown vendor '{vendor}'")

    def _require_item(self, item: str):
        if item not in self.items:
            raise ValueError(f"Unknown item '{item}'")
        
    def _vendor_margins(self, vendor):
        m = VENDORS[vendor].get("margins", {})
        sell = m.get("sell", self.margin_sell)
        buy  = m.get("buy",  self.margin_buy)
        return sell, buy
    
    def _item_weight(self, item: str) -> float:
    # Expect a "weight" field in ITEMS; default to 0.5 if missing so you can phase this in gradually
        return float(self.items[item].get("weight", 0.5))

    def _current_weight(self) -> float:
        total = 0.0
        for itm, qty in self.player_inv.items():
            total += self._item_weight(itm) * qty
        return total
        
    # ---------- quoting ----------
    def quote_buy(self, vendor, item, qty=1) -> int:
        self._require_vendor(vendor)
        self._require_item(item)
        base = self.items[item]["base_price"]
        m_sell, _ = self._vendor_margins(vendor)
        factor = self._event_multiplier(item)
        return int(math.ceil(base * factor * (1 + m_sell) * qty))

    def quote_sell(self, vendor, item, qty=1) -> int:
        self._require_vendor(vendor)
        self._require_item(item)
        base = self.items[item]["base_price"]
        _, m_buy = self._vendor_margins(vendor)
        factor = self._event_multiplier(item)
        return int(math.floor(base * factor * (1 - m_buy) * qty))

    # ---------- transactions ----------
    def buy(self, vendor, item, qty) -> int:
        self._require_vendor(vendor)
        self._require_item(item)
        stock = self.vendors[vendor]["stock"].get(item, 0)
        if stock < qty:
            raise ValueError("Vendor out of stock")
        cost = self.quote_buy(vendor, item, qty)
        if self.player_gold < cost:
            raise ValueError("Not enough gold")
        new_weight = self._current_weight() + self._item_weight(item) * qty
        if new_weight > self.player_capacity:
            raise ValueError(f"Inventory too heavy ({new_weight:.1f}/{self.player_capacity:.1f})")
        self.player_gold -= cost
        self.vendors[vendor]["stock"][item] = stock - qty
        self.player_inv[item] = self.player_inv.get(item, 0) + qty
        return cost

    def sell(self, vendor, item, qty) -> int:
        self._require_vendor(vendor)
        self._require_item(item)
        if self.player_inv.get(item, 0) < qty:
            raise ValueError("Not enough to sell")
        revenue = self.quote_sell(vendor, item, qty)
        # move goods
        self.player_inv[item] -= qty
        if self.player_inv[item] == 0:
            del self.player_inv[item]
        self.vendors[vendor]["stock"][item] = self.vendors[vendor]["stock"].get(item, 0) + qty
        # pay player
        self.player_gold += revenue
        return revenue
    
    # ---------- progression ----------
    def get_player_summary(self):
        return {
            "gold": self.player_gold,
            "weight": self._current_weight(),
            "capacity": self.player_capacity,
            "inventory": dict(self.player_inv),
        }

    def advance_day(self):
        for v_name, v in self.vendors.items():
            targets = VENDORS[v_name]["target_stock"]
            stock = v["stock"]
            for k, tgt in targets.items():
                have = stock.get(k, 0)
                if have < tgt:
                    step = max(1, int(0.25 * tgt)) # up to ~25% of target
                    stock[k] = min(tgt, have + self.rng.randint(0, step))
        
        evt = self.rng.choice(self._events) if self._events else None
        self._today_event = evt

    def get_news_today(self):
        if not self._today_event:
            return ["All quiet on the trade winds."]
        return [self._today_event.get("text", "Strange quiet in the market…")]

    def get_rumors_today(self):
        # For MVP, just reuse the news so it’s always true and consistent.
        return self.get_news_today()
    
    def _event_multiplier(self, item_key: str) -> float:
        if not self._today_event:
            return 1.0
        it = self.items[item_key]
        cats = self._today_event.get("cat_multipliers", {})
        items = self._today_event.get("item_multipliers", {})
        return float(cats.get(it["category"], 1.0)) * float(items.get(item_key, 1.0))
    
    def _load_events(self, path: str):
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []


if __name__ == "__main__":
    market = Market()
    print(market.vendors)
