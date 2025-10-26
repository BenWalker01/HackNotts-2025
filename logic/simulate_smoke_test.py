from logic.market_api import *
from logic.market_api import force_event
from logic.market_api import list_events

def line(title=""):
    print("\n" + ("-" * 60))
    if title:
        print(title)

def show_player():
    s = get_player_state()
    print(f"Player: gold={s['gold']}  weight={s['weight']:.1f}/{s['capacity']:.1f}  inv={s['inventory']}")

def main():
    init()

    s = get_storage_info()
    ps = get_player_state()
    print("Carry (from Market):", f"{ps['weight']:.1f}/{ps['capacity']:.1f}")
    print("Home storage:", s["home_used"], "/", s["home_capacity"])


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

    # 4) Event impact + restock over several days (news vs rumors)
    line("Event impact over 3 days (Ale, Cloth, Wheat) + restock")
    print("Zara spices stock (start):", get_vendor_stock(zara).get("spices", 0))
    for i in range(1, 3 + 1):
        day = advance_day()
        print(f" Day {i} news:", day["news"])
        print(f" Day {i} rumors:", [r["text"] for r in day["rumors"]])
        for r in day["rumors"]:
            flag = "✓" if r.get("matches_event") else "?"
            print(f"   rumor {flag}: {r['text']} (truth roll: {r['is_true']})")
        print("  Hal ale price:",  get_quote_buy(hal,  "ale",   1))
        print("  Sven cloth price:",get_quote_buy(sven, "cloth", 1))
        print("  Hal wheat price:", get_quote_buy(hal,  "wheat", 1))
        print("  Zara spices stock:", get_vendor_stock(zara).get("spices", 0))

    # 5) Force a specific event and show effects + rumor alignment
    line("Force 'festival' (debug)")
    print("Available events:", list_events())
    force_event(None)
    base = {
        "ale":   get_quote_buy(hal,  "ale",   1),  # expect ~7 at Hal
        "cloth": get_quote_buy(sven, "cloth", 1),  # ~8–9 depending on margins/events
        "spices":get_quote_buy(zara, "spices",1)   # ~17–19 depending on margins
    }

    force_event("festival")
    print(" Forced festival.")

    after = {
        "ale":   get_quote_buy(hal,  "ale",   1),  # expect 9 (6 * 1.20 * 1.10 * 1.12 → ceil 9)
        "cloth": get_quote_buy(sven, "cloth", 1),  # small bump
        "spices":get_quote_buy(zara, "spices",1)   # visible bump (luxury + item/category)
    }

    print("Prices baseline → festival:", base, "→", after)

    day = advance_day()
    print("News:", day["news"])
    print("Rumors:", [r["text"] for r in day["rumors"]])

    # Optional: clear the lock again
    force_event(None)

    line("Done")
    show_player()

if __name__ == "__main__":
    main()
