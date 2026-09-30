from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

# User Schemas
class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: Optional[str] = "supabase_managed"
    role: str = "DONOR"
    phone: Optional[str] = ""
    institution_id: Optional[int] = None
    institution_name: Optional[str] = None
    supabase_uid: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    phone: str
    verification_status: str
    institution_id: Optional[int] = None
    institution_name: Optional[str] = None
    supabase_uid: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Institution Schemas
class InstitutionResponse(BaseModel):
    id: int
    name: str
    type: str
    AISHE_code: Optional[str] = None
    verification_status: str
    latitude: float
    longitude: float
    address: str

    class Config:
        from_attributes = True

# Distribution Point Schemas
class DistributionPointCreate(BaseModel):
    name: str
    type: str
    address: str
    latitude: float
    longitude: float
    capacity_kg: float = 300.0
    cold_storage_available: bool = False

class DistributionPointResponse(BaseModel):
    id: int
    name: str
    type: str
    address: str
    latitude: float
    longitude: float
    capacity_kg: float
    cold_storage_available: bool
    verification_status: str

    class Config:
        from_attributes = True

# Donation Schemas
class FoodDonationCreate(BaseModel):
    donor_id: Optional[int] = None
    food_name: str = Field(..., example="Vegetable Rice & Dal")
    meal_type: str = Field("LUNCH", example="LUNCH")
    dietary_type: str = Field("VEG", example="VEG")
    quantity_kg: float = Field(..., gt=0, example=30.0)
    servings: int = Field(..., gt=0, example=100)
    preparation_time: Optional[datetime] = None
    pickup_deadline_hours: Optional[float] = Field(2.0, description="Hours until pickup deadline")
    pickup_deadline: Optional[datetime] = None
    pickup_location: str = Field(..., example="BMSIT Campus Mess Gate 1")
    latitude: Optional[float] = 13.1332
    longitude: Optional[float] = 77.5684
    safety_confirmed: bool = True

class FoodDonationResponse(BaseModel):
    id: int
    donor_id: int
    donor_name: Optional[str] = None
    institution_id: Optional[int] = None
    institution_name: Optional[str] = None
    food_name: str
    meal_type: str
    dietary_type: str
    quantity_kg: float
    servings: int
    preparation_time: datetime
    pickup_deadline: datetime
    pickup_location: str
    latitude: float
    longitude: float
    status: str
    priority_score: float
    priority_badge: Optional[str] = "MEDIUM"
    priority_color: Optional[str] = "yellow"
    minutes_remaining: Optional[int] = 120
    distance_km: Optional[float] = None
    safety_confirmed: bool
    created_at: datetime

    class Config:
        from_attributes = True

class DonationClaimRequest(BaseModel):
    receiver_id: Optional[int] = None
    destination_point_id: Optional[int] = None
    notes: Optional[str] = None

# Delivery Schemas
class DeliveryPickupRequest(BaseModel):
    volunteer_id: Optional[int] = None
    temperature_celsius: float = Field(..., description="Food temperature in Celsius measured at pickup")
    is_hot_food: bool = True
    proof: Optional[str] = None
    notes: Optional[str] = None

class DeliveryDeliverRequest(BaseModel):
    proof: Optional[str] = None
    notes: Optional[str] = None

class DeliveryConfirmRequest(BaseModel):
    received_quantity_kg: float = Field(..., gt=0, description="Actual kilograms verified by receiver")
    meals_distributed: int = Field(..., gt=0, description="Actual meals distributed to beneficiaries")
    notes: Optional[str] = None

class DeliveryResponse(BaseModel):
    id: int
    donation_id: int
    volunteer_id: Optional[int] = None
    volunteer_name: Optional[str] = None
    receiver_id: Optional[int] = None
    receiver_name: Optional[str] = None
    pickup_time: Optional[datetime] = None
    pickup_temperature: Optional[float] = None
    delivery_time: Optional[datetime] = None
    received_quantity_kg: Optional[float] = None
    status: str
    pickup_latitude: Optional[float] = None
    pickup_longitude: Optional[float] = None
    delivery_latitude: Optional[float] = None
    delivery_longitude: Optional[float] = None
    proof: Optional[str] = None
    notes: Optional[str] = None
    donation: Optional[FoodDonationResponse] = None

    class Config:
        from_attributes = True

# Impact Log & Summary
class ImpactSummaryResponse(BaseModel):
    meals_rescued: int
    food_saved_kg: float
    successful_donations: int
    people_served: int
    completed_deliveries: int
    co2e_avoided_kg: float
    waste_cost_saved_inr: float
    co2_factor: float = 2.5
    cost_factor: float = 4.0
    notice: str = "Estimated prototype metrics based on 1kg food diverted = 2.5kg CO2e and Rs.4 municipal wet waste savings."
