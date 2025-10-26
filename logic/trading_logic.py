import json
import math
import os
import random
from .economy_bootstrap import ITEMS, VENDORS

class Market:
    def __init__(self, seed: int | None = 44):
        self.items = ITEMS
        self.vendors = {
            name: {
                "stock": {
                    product: max(0, quantity//2)
                    for product, quantity in data["target_stock"].items()
                }
            } for name, data in VENDORS.items()
        }
        self.player_gold = 50
        self.player_inv = {}

        self.margin_sell = 0.15  # vendor markup
        self.margin_buy  = 0.10  # vendor buys cheaper

        self.rng = random.Random(seed if seed is not None else 44)
        events_path = os.path.join(os.path.dirname(__file__), "events_seeds.json")
        self._events = self._load_events(events_path)
        rumors_path = os.path.join(os.path.dirname(__file__), "rumors_seeds.json")
        self._rumors = self._load_json(rumors_path)
        self._today_event = None
        self._rumors_today = [] 

        self.player_capacity = 20

        self._forced_event_lock = False


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
    
    def list_event_keys(self):
        """For debugging: list available event keys."""
        return [e.get("key") for e in self._events]

    def force_event(self, key: str | None):
        """
        Manually set today's event by key (or clear with None).
        When set, advance_day() will keep this event until you clear it.
        """
        if key is None:
            self._today_event = None
            self._forced_event_lock = False
            return None
        for e in self._events:
            if e.get("key") == key:
                self._today_event = e
                self._forced_event_lock = True
                self._rumors_today = self._roll_rumors_today(n=2)
                return key
        raise ValueError(f"Unknown event '{key}'. Available: {', '.join(self.list_event_keys())}")
    
    def _load_json(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                import json as _json
                return _json.load(f)
        except FileNotFoundError:
            return []
        
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
        
        if not self._forced_event_lock:
            self._today_event = self.rng.choice(self._events) if self._events else None
        self._rumors_today = self._roll_rumors_today(n=2)

    def get_news_today(self):
        if not self._today_event:
            return ["All quiet on the trade winds."]
        return [self._today_event.get("text", "Strange quiet in the market…")]
    
    def get_rumors_today(self):
        # Return structured rumors (ui can choose to show text only, or badges for truth/matches_event)
        return self._rumors_today or []

    def _roll_rumors_today(self, n=2):
        """
        Pick up to n rumors. Each rumor is a dict:
        {text, is_true (rolled), matches_event (hint matches today's real event)}
        Rumors do NOT affect prices.
        """
        out = []
        if not self._rumors:
            return out
        pool = self._rumors[:]              # copy
        self.rng.shuffle(pool)

        # 50% chance: inject one rumor that matches today's event (if any exist)
        if self._today_event and self.rng.random() < 0.5:
            k = self._today_event.get("key")
            matching = [r for r in pool if r.get("event_key_hint") == k]
            if matching:
                r = self.rng.choice(matching)
                pool.remove(r)
                out.append({
                    "text": r["text"],
                    "is_true": self.rng.random() < float(r.get("truth_prob", 0.5)),
                    "matches_event": True
                })

        remain = max(0, n - len(out))
        for r in pool[:remain]:
            is_true = self.rng.random() < float(r.get("truth_prob", 0.5))
            matches_event = bool(self._today_event and r.get("event_key_hint") == self._today_event.get("key"))
            out.append({"text": r["text"], "is_true": is_true, "matches_event": matches_event})
        return out

    
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
