"""
Logistics & Safety Validation Engine for Annamitra
Handles food temperature safety thresholds, dispatch logic, and volunteer route validation.
"""
from typing import Dict, Any, Tuple
from clustering import haversine_distance_km, calculate_priority_score, cluster_surplus_batches

# Configurable Food Safety Temperature Thresholds (Celsius)
HOT_FOOD_MIN_TEMP = 60.0   # Hot food must be maintained >= 60°C
COLD_FOOD_MAX_TEMP = 10.0  # Cold food must be maintained <= 10°C

def validate_food_temperature(temp_celsius: float, is_hot_food: bool = True) -> Tuple[bool, str]:
    """
    Validates food temperature against operational safety guidelines.
    Hot food: >= 60°C
    Cold food: <= 10°C
    Returns (is_compliant, warning_message).
    """
    if is_hot_food:
        if temp_celsius < HOT_FOOD_MIN_TEMP:
            return (
                False,
                f"Food Safety Warning: Measured temperature is {temp_celsius}°C, below the recommended threshold of {HOT_FOOD_MIN_TEMP}°C for hot holding."
            )
        return (True, f"Compliant: Hot food maintained safely at {temp_celsius}°C (≥ {HOT_FOOD_MIN_TEMP}°C).")
    else:
        if temp_celsius > COLD_FOOD_MAX_TEMP:
            return (
                False,
                f"Food Safety Warning: Measured temperature is {temp_celsius}°C, exceeding the recommended cold-chain limit of {COLD_FOOD_MAX_TEMP}°C."
            )
        return (True, f"Compliant: Cold food maintained safely at {temp_celsius}°C (≤ {COLD_FOOD_MAX_TEMP}°C).")
