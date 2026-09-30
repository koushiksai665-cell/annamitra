from fastapi import APIRouter
from logistics import validate_food_temperature, HOT_FOOD_MIN_TEMP, COLD_FOOD_MAX_TEMP

router = APIRouter(prefix="/api/v1/logistics", tags=["Logistics Helpers"])

@router.get("/safety-thresholds")
def get_safety_thresholds():
    return {
        "hot_food_min_celsius": HOT_FOOD_MIN_TEMP,
        "cold_food_max_celsius": COLD_FOOD_MAX_TEMP,
        "disclaimer": "Operational safeguard thresholds. Do not present as substitute for statutory regulations."
    }
