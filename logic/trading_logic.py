from economy_bootstrap import ITEMS, VENDORS

class Market:
    def __init__(self):
        self.items = ITEMS
        self.vendors = {name: {"stock": {product: max(1, quantity//2) for product, quantity in data["target_stock"].items()}} for name, data in VENDORS.items()}
        self.player_gold = 60
        self.player_inv = {}

        self.margin_sell = 0.15  # vendor markup
        self.margin_buy  = 0.10  # vendor buys cheaper

    def quote_buy(self, vendor, item, qty=1):
        if item not in self.items: raise ValueError(f"Unknown item '{item}'")
        base = self.items[item]["base_price"]
        return int(round(base * (1 + self.margin_sell) * qty))

    def quote_sell(self, vendor, item, qty=1):
        if item not in self.items: raise ValueError(f"Unknown item '{item}'")
        base = self.items[item]["base_price"]
        return int(round(base * (1 - self.margin_buy) * qty))

    def buy(self, vendor, item, qty):
        stock = self.vendors[vendor]["stock"].get(item, 0)
        if stock < qty: raise ValueError("Vendor out of stock")
        cost = self.quote_buy(vendor, item, qty)
        if self.player_gold < cost: raise ValueError("Not enough gold")
        self.player_gold -= cost
        self.vendors[vendor]["stock"][item] -= qty
        self.player_inv[item] = self.player_inv.get(item, 0) + qty
        return cost

    def sell(self, vendor, item, qty):
        if self.player_inv.get(item, 0) < qty: raise ValueError("Not enough to sell")
        revenue = self.quote_sell(vendor, item, qty)
        self.player_inv[item] -= qty
        if self.player_inv[item] == 0: del self.player_inv[item]
        self.vendors[vendor]["stock"][item] = self.vendors[vendor]["stock"].get(item, 0) + qty
        self.player_gold += revenue
        return revenue

market= Market()
print(market.vendors)