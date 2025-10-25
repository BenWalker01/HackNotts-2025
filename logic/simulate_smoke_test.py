from api_facade import *

init()
v = "Trader Zara"

print("Vendors:", get_vendors())
print("Zara stock (start):", get_vendor_stock(v))
print("Buy 1 spices:", get_quote_buy(v, "spices", 1))
spent = buy(v, "spices", 1); print("Spent:", spent, "→ gold", get_player_state()["gold"])
earned = sell(v, "spices", 1); print("Earned:", earned, "→ gold", get_player_state()["gold"])

print("\nAdvance day…")
rumors = advance_day()
print("Rumors:", rumors)
print("Zara stock (after):", get_vendor_stock(v))
