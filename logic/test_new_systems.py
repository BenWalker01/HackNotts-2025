"""
Test script for new systems: storage, deals, progression, upgrades
"""

from .market_api import *

print("=" * 50)
print("INITIALIZING GAME")
print("=" * 50)
init(seed=42)

print("\n📦 STORAGE SYSTEM TEST")
print("-" * 50)
storage_info = get_storage_info()
print(f"Carrying: {storage_info['carrying_used']}/{storage_info['carrying_capacity']}")
print(f"Home: {storage_info['home_used']}/{storage_info['home_capacity']}")

# Buy some items
print("\nBuying 3 wheat...")
buy("Farmer Hal", "wheat", 3)
print(f"Inventory: {get_player_state()['inventory']}")

# Store 2 wheat at home
print("\nStoring 2 wheat at home...")
store_item("wheat", 2)
print(f"Inventory: {get_player_state()['inventory']}")
print(f"Home storage: {get_storage_info()['home_storage']}")

print("\n🏆 PROGRESSION TEST")
print("-" * 50)
status = get_game_status()
print(f"Day {status['current_day']}/{status['max_days']}")
print(f"Gold: {status['player_gold']}/{status['goal_gold']} ({status['progress_percent']}%)")
print(f"Days remaining: {status['days_remaining']}")

print("\n🛒 UPGRADES TEST")
print("-" * 50)
upgrades = get_available_upgrades()
for up in upgrades:
    print(f"- {up['name']}: {up['cost']}g - {up['description']}")

print("\n🎲 NPC DEALS TEST")
print("-" * 50)
# Advance days until deal appears
for i in range(5):
    print(f"\nAdvancing to day {i+2}...")
    events = advance_day()
    
    if events["new_deal"]:
        deal = get_active_deal()
        print(f"\n🎉 DEAL APPEARED!")
        print(f"NPC: {deal['npc_name']}")
        print(f"Description: {deal['description']}")
        print(f"Item: {deal['item']} x{deal['quantity']}")
        print(f"Discount: {deal['discount']*100}%")
        print(f"Is scam?: {deal['is_scam']}")
        break
    
    if events["theft"]["occurred"]:
        print(f"⚠️ THEFT! Lost: {events['theft']['stolen']}")

print("\n" + "=" * 50)
print("TEST COMPLETE")
print("=" * 50)
