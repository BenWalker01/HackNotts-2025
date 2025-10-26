# logic/difficulty.py
from dataclasses import dataclass

@dataclass(frozen=True)
class DiffTuning:
    starting_gold: int
    capacity: float
    # economy
    event_scale: float         # scales how strong events are (1.0 = as-is)
    restock_frac: float        # fraction of vendor target used for daily restock step
    # vendor behavior (applied on top of vendor margins)
    margin_sell_add: float     # extra markup vendor charges the player
    margin_buy_add: float      # extra discount vendor takes when buying from player
    # risk & world
    theft_threshold: int
    theft_chance: float
    guard_cost: int
    # social
    rumor_truth_shift: float   # + makes rumors more often true, - more false
    deal_win_bias_pp: int      # percentage points added/subtracted to NPC deal success

DIFFICULTIES = {
    "peasant": DiffTuning(
        starting_gold=80, capacity=30.0,
        event_scale=0.85, restock_frac=0.35,
        margin_sell_add=-0.01, margin_buy_add=-0.01,
        theft_threshold=120, theft_chance=0.02, guard_cost=1,
        rumor_truth_shift=+0.15, deal_win_bias_pp=+10
    ),
    "merchant": DiffTuning(   # default / current behavior-ish
        starting_gold=60, capacity=20.0,
        event_scale=1.00, restock_frac=0.25,
        margin_sell_add=0.00, margin_buy_add=0.00,
        theft_threshold=80, theft_chance=0.04, guard_cost=2,
        rumor_truth_shift=0.00, deal_win_bias_pp=0
    ),
    "guildmaster": DiffTuning(
        starting_gold=55, capacity=18.0,
        event_scale=1.20, restock_frac=0.18,
        margin_sell_add=+0.02, margin_buy_add=+0.02,
        theft_threshold=70, theft_chance=0.06, guard_cost=3,
        rumor_truth_shift=-0.10, deal_win_bias_pp=-5
    ),
    "king": DiffTuning(
        starting_gold=50, capacity=15.0,
        event_scale=1.35, restock_frac=0.12,
        margin_sell_add=+0.04, margin_buy_add=+0.04,
        theft_threshold=60, theft_chance=0.08, guard_cost=4,
        rumor_truth_shift=-0.15, deal_win_bias_pp=-10
    ),
}
