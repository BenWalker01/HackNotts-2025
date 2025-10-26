
#LATER ON WE WANT TO RANDOMIZE IT (INITIALLY AT THE BEGINNING OF A GAME) 

ITEMS = {
    # Light, cheap staples; goes bad in a few days
    "wheat":   {"category": "agricultural", "base_price": 2,  "weight": 0.5, "perishable_days": 4},

    # Heavy materials; never perish
    "iron":    {"category": "crafted", "base_price": 5, "weight": 2.2, "perishable_days": None},
    "wood":    {"category": "crafted", "base_price": 3, "weight": 1.2, "perishable_days": None},

    # Mid-tier textiles; don’t perish
    "cloth":   {"category": "textile", "base_price": 7, "weight": 0.5, "perishable_days": None},
    "leather": {"category": "textile", "base_price": 8, "weight": 0.7, "perishable_days": None},

    # Premium pocket goods; light; mostly non-perishable
    "spices":  {"category": "luxury", "base_price": 15, "weight": 0.1, "perishable_days": None},
    "salt":    {"category": "luxury", "base_price": 10, "weight": 0.2, "perishable_days": None},

    # Processed drink; moderately heavy; short shelf life
    "ale":     {"category": "processed", "base_price": 6, "weight": 0.6, "perishable_days": 3},

    # --- Weapons / Armor (crafted) ---
    "sword":        {"category": "crafted",  "base_price": 25, "weight": 2.5, "perishable_days": None},
    "dagger":       {"category": "crafted",  "base_price": 12, "weight": 0.8, "perishable_days": None},
    "shield":       {"category": "crafted",  "base_price": 18, "weight": 3.0, "perishable_days": None},
    "chainmail":    {"category": "crafted",  "base_price": 38, "weight": 8.0, "perishable_days": None},
    # Lighter “fantasy steel” set—pricey but not too heavy
    "plate_armor":  {"category": "crafted",  "base_price": 55, "weight": 10.0, "perishable_days": None},

    # --- Hunting / Supplies ---
    "bow":          {"category": "crafted",  "base_price": 16, "weight": 1.2, "perishable_days": None},
    "arrows":       {"category": "crafted",  "base_price": 6,  "weight": 0.6, "perishable_days": None},

    # --- Alchemy / Special ---
    "herbs":        {"category": "special",  "base_price": 7,  "weight": 0.2, "perishable_days": 5},
    "potions":      {"category": "special",  "base_price": 22, "weight": 0.3, "perishable_days": None},

    # --- Lux curios (fantasy) ---
    "dragon_scales":{"category": "luxury",   "base_price": 80, "weight": 0.5, "perishable_days": None},
    "mana_crystal": {"category": "luxury",   "base_price": 45, "weight": 0.3, "perishable_days": None},
    "rune_stone":   {"category": "special",  "base_price": 28, "weight": 1.0, "perishable_days": None},
}


VENDORS = {
    "Farmer Hal":      {"target_stock": {"wheat": 40, "ale": 12, "salt": 6}, "margins": {"sell": 0.12, "buy": 0.08}},
    "Blacksmith Greta":{"target_stock": {"iron": 30, "wood": 20, "leather": 10}, "margins": {"sell": 0.14, "buy": 0.10}},
    "Merchant Sven":   {"target_stock": {"cloth": 16, "leather": 10, "salt": 10}, "margins": {"sell": 0.18, "buy": 0.12}},
    "Trader Zara":     {"target_stock": {"spices": 8, "cloth": 10, "salt": 12, "ale": 8}, "margins": {"sell": 0.22, "buy": 0.15}},
    "Armorer Alric":   {"target_stock": {"chainmail": 5, "plate_armor": 2, "shield": 5}, "margins": {"sell": 0.20, "buy": 0.14}},
    "Alchemist Mira":  {"target_stock": {"herbs": 18, "potions": 10, "rune_stone": 4}, "margins": {"sell": 0.19, "buy": 0.12}},
}
