import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String, Integer, Float, Boolean, DateTime, ForeignKey, 
    Text, Enum as SQLEnum
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class UserRole(str, enum.Enum):
    DONOR = "DONOR"
    RECEIVER = "RECEIVER"
    VOLUNTEER = "VOLUNTEER"
    ADMIN = "ADMIN"

class MealType(str, enum.Enum):
    BREAKFAST = "BREAKFAST"
    LUNCH = "LUNCH"
    DINNER = "DINNER"
    SNACKS = "SNACKS"

class DietaryType(str, enum.Enum):
    VEG = "VEG"
    NON_VEG = "NON_VEG"

class DonationStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    CLAIMED = "CLAIMED"
    VOLUNTEER_ASSIGNED = "VOLUNTEER_ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"

class DeliveryStatus(str, enum.Enum):
    CLAIMED = "CLAIMED"
    ASSIGNED = "ASSIGNED"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    COMPLETED = "COMPLETED"


class Institution(Base):
    __tablename__ = "institutions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)  # College, Hostel, PG, Restaurant, Event Organizer
    AISHE_code: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(50), default="VERIFIED")
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    users: Mapped[List["User"]] = relationship(back_populates="institution")
    donations: Mapped[List["FoodDonation"]] = relationship(back_populates="institution")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), nullable=False)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)
    verification_status: Mapped[str] = mapped_column(String(50), default="VERIFIED")
    institution_id: Mapped[Optional[int]] = mapped_column(ForeignKey("institutions.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    institution: Mapped[Optional["Institution"]] = relationship(back_populates="users")
    donations: Mapped[List["FoodDonation"]] = relationship(back_populates="donor", foreign_keys="FoodDonation.donor_id")
    volunteer_deliveries: Mapped[List["Delivery"]] = relationship(back_populates="volunteer", foreign_keys="Delivery.volunteer_id")
    receiver_deliveries: Mapped[List["Delivery"]] = relationship(back_populates="receiver", foreign_keys="Delivery.receiver_id")


class FoodDonation(Base):
    __tablename__ = "food_donations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    donor_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    institution_id: Mapped[Optional[int]] = mapped_column(ForeignKey("institutions.id"), nullable=True)
    food_name: Mapped[str] = mapped_column(String(255), nullable=False)
    meal_type: Mapped[str] = mapped_column(String(50), default="LUNCH")
    dietary_type: Mapped[str] = mapped_column(String(50), default="VEG")
    quantity_kg: Mapped[float] = mapped_column(Float, nullable=False)
    servings: Mapped[int] = mapped_column(Integer, nullable=False)
    preparation_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pickup_deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pickup_location: Mapped[str] = mapped_column(String(255), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[DonationStatus] = mapped_column(SQLEnum(DonationStatus), default=DonationStatus.AVAILABLE, index=True)
    priority_score: Mapped[float] = mapped_column(Float, default=50.0)
    safety_confirmed: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    donor: Mapped["User"] = relationship(back_populates="donations", foreign_keys=[donor_id])
    institution: Mapped[Optional["Institution"]] = relationship(back_populates="donations")
    delivery: Mapped[Optional["Delivery"]] = relationship(back_populates="donation", uselist=False)
    impact_log: Mapped[Optional["ImpactLog"]] = relationship(back_populates="donation", uselist=False)


class DistributionPoint(Base):
    __tablename__ = "distribution_points"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(100), nullable=False)  # Hospital Caretakers, Railway Station, Community Kitchen, etc.
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    capacity_kg: Mapped[float] = mapped_column(Float, default=300.0)
    cold_storage_available: Mapped[bool] = mapped_column(Boolean, default=False)
    verification_status: Mapped[str] = mapped_column(String(50), default="VERIFIED")


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    donation_id: Mapped[int] = mapped_column(ForeignKey("food_donations.id"), unique=True, nullable=False)
    volunteer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    receiver_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    
    pickup_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    pickup_temperature: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    delivery_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    received_quantity_kg: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="CLAIMED")
    
    pickup_latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    pickup_longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    delivery_latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    delivery_longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    proof: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    donation: Mapped["FoodDonation"] = relationship(back_populates="delivery")
    volunteer: Mapped[Optional["User"]] = relationship(back_populates="volunteer_deliveries", foreign_keys=[volunteer_id])
    receiver: Mapped[Optional["User"]] = relationship(back_populates="receiver_deliveries", foreign_keys=[receiver_id])


class ImpactLog(Base):
    __tablename__ = "impact_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    donation_id: Mapped[int] = mapped_column(ForeignKey("food_donations.id"), unique=True, nullable=False)
    food_saved_kg: Mapped[float] = mapped_column(Float, nullable=False)
    meals_served: Mapped[int] = mapped_column(Integer, nullable=False)
    co2e_avoided: Mapped[float] = mapped_column(Float, nullable=False)
    waste_cost_saved: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    donation: Mapped["FoodDonation"] = relationship(back_populates="impact_log")
