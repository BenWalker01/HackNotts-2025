from logic.api_facade import *

def line(title=""):
    print("\n" + ("-" * 60))
    if title:
        print(title)

def show_player():
    s = get_player_state()
    print(f"Player: gold={s['gold']}  weight={s['weight']:.1f}/{s['capacity']:.1f}  inv={s['inventory']}")

def main():
    init()

    vendors = get_vendors()
    print("Vendors:", vendors)
    show_player()

    # Pick the usual suspects (rename here if you change vendor names)
    hal   = "Farmer Hal"
    greta = "Blacksmith Greta"
    sven  = "Merchant Sven"
    zara  = "Trader Zara"

    # 1) Vendor margin check on ALE (qty=1 and qty=5 to beat rounding)
    line("Ale price check (vendor margins)")
    print(" Hal buy 1 ale:", get_quote_buy(hal, "ale", 1))
    print(" Zara buy 1 ale:", get_quote_buy(zara, "ale", 1))
    print(" Hal buy 5 ale:", get_quote_buy(hal, "ale", 5))
    print(" Zara buy 5 ale:", get_quote_buy(zara, "ale", 5))

    # 2) Classic buy→sell spread (Spices @Zara)
    line("Spices spread @Zara")
    q_buy = get_quote_buy(zara, "spices", 1)
    print(" Quote buy 1:", q_buy)
    spent = buy(zara, "spices", 1)
    print(" Spent:", spent); show_player()
    q_sell = get_quote_sell(zara, "spices", 1)
    print(" Quote sell 1:", q_sell)
    earned = sell(zara, "spices", 1)
    print(" Earned:", earned); show_player()

    # 3) Capacity test (Iron @Greta) — buy small batches until blocked
    line("Capacity test with Iron @Greta")
    try:
        while True:
            spent = buy(greta, "iron", 2)
            print(f" Bought 2 iron (spent {spent})")
            show_player()
    except Exception as e:
        print(" Expected stop:", e)

    # 4) Event impact + restock over several days
    line("Event impact over 3 days (Ale, Cloth, Wheat) + restock")
    print("Zara spices stock (start):", get_vendor_stock(zara).get("spices", 0))
    for day in range(1, 4):
        rumors = advance_day()
        print(f" Day {day} rumors:", rumors)
        print("  Hal ale price:",  get_quote_buy(hal,  "ale",   1))
        print("  Sven cloth price:",get_quote_buy(sven, "cloth", 1))
        print("  Hal wheat price:", get_quote_buy(hal,  "wheat", 1))
        print("  Zara spices stock:", get_vendor_stock(zara).get("spices", 0))

    # 5) (Optional) Force a specific event if the facade exposes a debug hook
    if "_force_event" in globals():
        line("Force 'festival' (if supported by facade)")
        try:
            _force_event("festival")  # only works if you added it in api_facade
            print(" Forced festival.")
            print("  Hal ale price (festival):", get_quote_buy(hal, "ale", 1))
            print("  Sven cloth price (festival):", get_quote_buy(sven, "cloth", 1))
            print("  Zara spices price (festival):", get_quote_buy(zara, "spices", 1))
        except Exception as e:
            print(" Debug force not available:", e)

    line("Done")
    show_player()

if __name__ == "__main__":
    main()
