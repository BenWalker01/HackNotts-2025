
#LATER ON WE WANT TO RANDOMIZE IT (INITIALLY AT THE BEGINNING OF A GAME) 

ITEMS = {
    "wheat":  {"category": "agricultural", "base_price": 2},
    "iron":   {"category": "crafted",      "base_price": 5},
    "cloth":  {"category": "textile",      "base_price": 7},
    "spices": {"category": "luxury",       "base_price": 15},
    "ale":    {"category": "processed",    "base_price": 6},
    "wood":   {"category": "crafted",      "base_price": 3},
    "leather":{"category": "textile",      "base_price": 8},
    "salt":   {"category": "luxury",       "base_price": 10},
}

VENDORS = {
    "Farmer Hal":      {"target_stock": {"wheat": 40, "ale": 12, "salt": 6}},
    "Blacksmith Greta":{"target_stock": {"iron": 30, "wood": 20, "leather": 10}},
    "Merchant Sven":   {"target_stock": {"cloth": 16, "leather": 10, "salt": 10}},
    "Trader Zara":     {"target_stock": {"spices": 8, "cloth": 10, "salt": 12, "ale": 8}},
}
