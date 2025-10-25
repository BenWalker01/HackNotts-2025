
#LATER ON WE WANT TO RANDOMIZE IT (INITIALLY AT THE BEGINNING OF A GAME) 

ITEMS = {
    # Light, cheap staples; goes bad in a few days
    "wheat":   {"category": "agricultural", "base_price": 2,  "weight": 0.5, "perishable_days": 4},

    # Heavy materials; never perish
    "iron":    {"category": "crafted",      "base_price": 5,  "weight": 1.0, "perishable_days": None},
    "wood":    {"category": "crafted",      "base_price": 3,  "weight": 1.2, "perishable_days": None},

    # Mid-tier textiles; don’t perish
    "cloth":   {"category": "textile",      "base_price": 7,  "weight": 0.5, "perishable_days": None},
    "leather": {"category": "textile",      "base_price": 8,  "weight": 0.7, "perishable_days": None},

    # Premium pocket goods; light; mostly non-perishable
    "spices":  {"category": "luxury",       "base_price": 15, "weight": 0.1, "perishable_days": None},
    "salt":    {"category": "luxury",       "base_price": 10, "weight": 0.2, "perishable_days": None},

    # Processed drink; moderately heavy; short shelf life
    "ale":     {"category": "processed",    "base_price": 6,  "weight": 0.6, "perishable_days": 3},
}


VENDORS = {
    "Farmer Hal":      {"target_stock": {"wheat": 40, "ale": 12, "salt": 6}},
    "Blacksmith Greta":{"target_stock": {"iron": 30, "wood": 20, "leather": 10}},
    "Merchant Sven":   {"target_stock": {"cloth": 16, "leather": 10, "salt": 10}},
    "Trader Zara":     {"target_stock": {"spices": 8, "cloth": 10, "salt": 12, "ale": 8}},
}
