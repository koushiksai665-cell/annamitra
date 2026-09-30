import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculates great-circle distance between two GPS coordinates in kilometers."""
    R = 6371.0  # Earth's radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def calculate_priority_score(
    quantity_kg: float,
    pickup_deadline: datetime,
    donor_lat: float,
    donor_lon: float,
    ref_lat: float = 12.9716,
    ref_lon: float = 77.5946
) -> Dict[str, Any]:
    """
    Computes priority score (0-100) based on:
    1. Expiry Urgency (up to 50 pts)
    2. Quantity Score (up to 30 pts)
    3. Distance Score (up to 20 pts)
    """
    now = datetime.utcnow()
    # Normalize naive/aware datetime
    if pickup_deadline.tzinfo is not None:
        pickup_deadline = pickup_deadline.replace(tzinfo=None)

    minutes_remaining = (pickup_deadline - now).total_seconds() / 60.0

    if minutes_remaining <= 0:
        return {
            "score": 0.0,
            "badge": "EXPIRED",
            "color": "gray",
            "minutes_remaining": 0,
            "label": "Expired"
        }

    # 1. Expiry Urgency (0-50 pts): Food expiring sooner gets higher points
    # e.g., 30 mins remaining -> 50 - 7.5 = 42.5; 180 mins (3h) -> 50 - 45 = 5 pts
    expiry_urgency = max(5.0, min(50.0, 50.0 - (minutes_remaining / 4.0)))

    # 2. Quantity Score (0-30 pts): larger batches feed more people and need rapid rescue
    quantity_score = min(30.0, max(5.0, quantity_kg * 0.8))

    # 3. Distance Score (0-20 pts): closer to center / distribution point gets priority bonus
    dist = haversine_distance_km(donor_lat, donor_lon, ref_lat, ref_lon)
    distance_score = max(2.0, min(20.0, 20.0 - (dist * 1.5)))

    total_score = round(expiry_urgency + quantity_score + distance_score, 1)

    # Classify into standard badges
    if minutes_remaining <= 60 or total_score >= 70:
        badge = "URGENT"
        color = "red"
    elif minutes_remaining <= 120 or total_score >= 50:
        badge = "HIGH"
        color = "orange"
    elif total_score >= 30:
        badge = "MEDIUM"
        color = "yellow"
    else:
        badge = "LOW"
        color = "green"

    return {
        "score": total_score,
        "badge": badge,
        "color": color,
        "minutes_remaining": int(minutes_remaining),
        "label": f"{badge} ({int(minutes_remaining)}m left)"
    }


def match_best_drop_point(
    cluster_lat: float, 
    cluster_lon: float, 
    drop_points: List[Any],
    required_kg: float = 20.0
) -> Optional[Any]:
    """
    Recommends the nearest suitable beneficiary / distribution point with sufficient capacity.
    """
    if not drop_points:
        return None

    # Filter distribution points with adequate capacity
    eligible = [dp for dp in drop_points if getattr(dp, "capacity_kg", 300.0) >= required_kg]
    if not eligible:
        eligible = drop_points

    return min(
        eligible,
        key=lambda dp: haversine_distance_km(cluster_lat, cluster_lon, dp.latitude, dp.longitude)
    )


def cluster_surplus_batches(
    donations: List[Any],
    drop_points: List[Any] = None,
    max_radius_km: float = 1.5
) -> List[Dict[str, Any]]:
    """
    Groups active food donations within ~1.5 km radius into consolidated volunteer routes.
    Example: Route #12: Pickup 1 -> College Mess, Pickup 2 -> Koramangala PG -> Drop Point
    """
    if not donations:
        return []

    clusters = []
    visited_ids = set()

    for idx, base_don in enumerate(donations):
        if base_don.id in visited_ids:
            continue

        base_lat = base_don.latitude
        base_lon = base_don.longitude
        donor_name = getattr(base_don.donor, "name", "Institutional Donor")
        inst_name = getattr(base_don.institution, "name", donor_name) if hasattr(base_don, "institution") and base_don.institution else donor_name

        route_id = 100 + len(clusters) + 1
        current_cluster = {
            "route_id": f"Route #{route_id}",
            "center_name": inst_name,
            "center_lat": base_lat,
            "center_lon": base_lon,
            "donation_ids": [base_don.id],
            "total_weight_kg": round(base_don.quantity_kg, 1),
            "total_servings": base_don.servings,
            "pickups": [
                {
                    "donation_id": base_don.id,
                    "food_name": base_don.food_name,
                    "donor_name": inst_name,
                    "location": base_don.pickup_location,
                    "quantity_kg": base_don.quantity_kg,
                    "servings": base_don.servings,
                    "latitude": base_lat,
                    "longitude": base_lon
                }
            ],
            "donor_names": [inst_name]
        }
        visited_ids.add(base_don.id)

        # Look for neighbor donations within max_radius_km
        for cand in donations:
            if cand.id in visited_ids:
                continue

            dist = haversine_distance_km(base_lat, base_lon, cand.latitude, cand.longitude)
            if dist <= max_radius_km:
                c_donor = getattr(cand.donor, "name", "Donor")
                c_name = getattr(cand.institution, "name", c_donor) if hasattr(cand, "institution") and cand.institution else c_donor
                current_cluster["donation_ids"].append(cand.id)
                current_cluster["total_weight_kg"] = round(current_cluster["total_weight_kg"] + cand.quantity_kg, 1)
                current_cluster["total_servings"] += cand.servings
                current_cluster["donor_names"].append(c_name)
                current_cluster["pickups"].append({
                    "donation_id": cand.id,
                    "food_name": cand.food_name,
                    "donor_name": c_name,
                    "location": cand.pickup_location,
                    "quantity_kg": cand.quantity_kg,
                    "servings": cand.servings,
                    "latitude": cand.latitude,
                    "longitude": cand.longitude
                })
                visited_ids.add(cand.id)

        # Match best drop point
        best_drop = match_best_drop_point(
            base_lat, base_lon, drop_points or [], current_cluster["total_weight_kg"]
        )

        drop_info = None
        total_dist = 0.0
        if best_drop:
            drop_info = {
                "id": best_drop.id,
                "name": best_drop.name,
                "type": best_drop.type,
                "address": best_drop.address,
                "latitude": best_drop.latitude,
                "longitude": best_drop.longitude
            }
            # Calculate total route distance
            legs_dist = 0.0
            prev_lat, prev_lon = base_lat, base_lon
            for p in current_cluster["pickups"][1:]:
                legs_dist += haversine_distance_km(prev_lat, prev_lon, p["latitude"], p["longitude"])
                prev_lat, prev_lon = p["latitude"], p["longitude"]
            legs_dist += haversine_distance_km(prev_lat, prev_lon, best_drop.latitude, best_drop.longitude)
            total_dist = round(legs_dist, 1)
        else:
            total_dist = 2.5

        current_cluster["recommended_drop_point"] = drop_info
        current_cluster["estimated_distance_km"] = max(total_dist, 1.2)
        clusters.append(current_cluster)

    return clusters
