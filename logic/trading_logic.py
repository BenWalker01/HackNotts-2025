import json
import os
import random
from economy_bootstrap import ITEMS, VENDORS

class Market:
    def __init__(self):
        self.items = ITEMS
        self.vendors = {
            name: {
                "stock": {
                    product: max(1, quantity//2)
                    for product, quantity in data["target_stock"].items()
                }
            } for name, data in VENDORS.items()
        }
        self.player_gold = 60
        self.player_inv = {}

        self.margin_sell = 0.15  # vendor markup
        self.margin_buy  = 0.10  # vendor buys cheaper

        self.rng = random.Random(42)
        self._events = self._load_events("events_seeds.json")

    # ---------- validation helpers ----------
    def _require_vendor(self, vendor: str):
        if vendor not in self.vendors:
            raise ValueError(f"Unknown vendor '{vendor}'")

    def _require_item(self, item: str):
        if item not in self.items:
            raise ValueError(f"Unknown item '{item}'")
        
    # ---------- quoting ----------
    def quote_buy(self, vendor, item, qty=1) -> int:
        self._require_vendor(vendor)
        self._require_item(item)
        base = self.items[item]["base_price"]
        return int(round(base * (1 + self.margin_sell) * qty))

    def quote_sell(self, vendor, item, qty=1) -> int:
        self._require_vendor(vendor)
        self._require_item(item)
        base = self.items[item]["base_price"]
        return int(round(base * (1 - self.margin_buy) * qty))

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

market= Market()
print(market.vendors)