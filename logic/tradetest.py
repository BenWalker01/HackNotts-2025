from trading_logic import Market

m = Market()
vendor = "Trader Zara"

print("Gold:", m.player_gold)
print("Zara stock:", m.vendors[vendor]["stock"])

print("Buy 1 spices quote:", m.quote_buy(vendor, "spices", 1))
spent = m.buy(vendor, "spices", 1)
print("Spent:", spent, "Gold now:", m.player_gold)

print("Player's iventory", m.player_inv)
print("Player's gold ", m.player_gold)

print("Sell 1 spices quote:", m.quote_sell(vendor, "spices", 1))
earned = m.sell(vendor, "spices", 1)
print("Earned:", earned, "Gold now:", m.player_gold)

print("Player's iventory", m.player_inv)
print("Player's gold ", m.player_gold)