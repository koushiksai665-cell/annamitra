import sys
import os
from datetime import datetime, timedelta, timezone

# Ensure script directory is on python path and handle Windows console utf-8
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from database import engine, SessionLocal
import models
from clustering import calculate_priority_score

def seed_database():
    print("[*] Rebuilding database tables...")
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    print("[*] Populating database with realistic urban seed data for Bengaluru...")

    # 1. Institutions
    bmsit = models.Institution(
        name="BMSIT College Mess",
        type="College Mess",
        AISHE_code="C-12890",
        verification_status="VERIFIED",
        address="Doddaballapur Main Road, Avalahalli, Yelahanka, Bengaluru, KA 560064",
        latitude=13.1332,
        longitude=77.5684
    )
    rvce = models.Institution(
        name="RVCE Mega Mess",
        type="Hostel Mess",
        AISHE_code="C-12345",
        verification_status="VERIFIED",
        address="Mysore Road, RV Vidyaniketan, Bengaluru, KA 560059",
        latitude=12.9237,
        longitude=77.4987
    )
    pg_cluster = models.Institution(
        name="Koramangala PG Cluster",
        type="Commercial PG",
        AISHE_code=None,
        verification_status="VERIFIED",
        address="80 Feet Road, 5th Block Koramangala, Bengaluru, KA 560095",
        latitude=12.9352,
        longitude=77.6245
    )
    event_kitchen = models.Institution(
        name="Bengaluru Event Kitchen",
        type="Event Organizer",
        AISHE_code=None,
        verification_status="VERIFIED",
        address="100 Feet Road, Indiranagar, Bengaluru, KA 560038",
        latitude=12.9719,
        longitude=77.6412
    )

    db.add_all([bmsit, rvce, pg_cluster, event_kitchen])
    db.commit()

    # 2. Distribution Points
    dp_hospital = models.DistributionPoint(
        name="Hospital Caretaker Food Hub",
        type="Hospital Caretakers",
        address="Lady Curzon Rd, Shivaji Nagar, Bengaluru, KA 560001",
        latitude=12.9832,
        longitude=77.6019,
        capacity_kg=500.0,
        cold_storage_available=True,
        verification_status="VERIFIED"
    )
    dp_shelter = models.DistributionPoint(
        name="Majestic Community Shelter",
        type="Railway Shelter",
        address="Kempegowda, Sevashrama, Bengaluru, KA 560023",
        latitude=12.9781,
        longitude=77.5695,
        capacity_kg=350.0,
        cold_storage_available=False,
        verification_status="VERIFIED"
    )
    dp_kitchen = models.DistributionPoint(
        name="Koramangala Community Kitchen",
        type="Community Kitchen",
        address="8th Block Koramangala, Bengaluru, KA 560095",
        latitude=12.9380,
        longitude=77.6200,
        capacity_kg=400.0,
        cold_storage_available=True,
        verification_status="VERIFIED"
    )
    dp_fridge = models.DistributionPoint(
        name="Community Fridge Hub",
        type="Community Fridge",
        address="4th Block Jayanagar, Bengaluru, KA 560011",
        latitude=12.9298,
        longitude=77.5833,
        capacity_kg=150.0,
        cold_storage_available=True,
        verification_status="VERIFIED"
    )

    db.add_all([dp_hospital, dp_shelter, dp_kitchen, dp_fridge])
    db.commit()

    # 3. Users
    pwd_hash = "demo123"  # Standard demo password

    # Donors
    u_bmsit = models.User(
        name="BMSIT College Mess",
        email="mess@bmsit.in",
        password=pwd_hash,
        role=models.UserRole.DONOR,
        phone="+91-9880112233",
        verification_status="VERIFIED",
        institution_id=bmsit.id
    )
    u_rvce = models.User(
        name="RVCE Mega Mess",
        email="mess@rvce.in",
        password=pwd_hash,
        role=models.UserRole.DONOR,
        phone="+91-9880223344",
        verification_status="VERIFIED",
        institution_id=rvce.id
    )
    u_pg = models.User(
        name="Koramangala PG Cluster",
        email="pg@koramangala.in",
        password=pwd_hash,
        role=models.UserRole.DONOR,
        phone="+91-9880334455",
        verification_status="VERIFIED",
        institution_id=pg_cluster.id
    )
    u_event = models.User(
        name="Bengaluru Event Kitchen",
        email="events@bengaluru.in",
        password=pwd_hash,
        role=models.UserRole.DONOR,
        phone="+91-9880445566",
        verification_status="VERIFIED",
        institution_id=event_kitchen.id
    )

    # Receivers
    u_rec_hospital = models.User(
        name="Hospital Caretaker Food Hub",
        email="caretakers@bowring.org",
        password=pwd_hash,
        role=models.UserRole.RECEIVER,
        phone="+91-9845112233",
        verification_status="VERIFIED"
    )
    u_rec_shelter = models.User(
        name="Majestic Community Shelter",
        email="shelter@majestic.org",
        password=pwd_hash,
        role=models.UserRole.RECEIVER,
        phone="+91-9845223344",
        verification_status="VERIFIED"
    )
    u_rec_kitchen = models.User(
        name="Koramangala Community Kitchen",
        email="kitchen@koramangala.org",
        password=pwd_hash,
        role=models.UserRole.RECEIVER,
        phone="+91-9845334455",
        verification_status="VERIFIED"
    )
    u_rec_fridge = models.User(
        name="Community Fridge Hub",
        email="fridge@jayanagar.org",
        password=pwd_hash,
        role=models.UserRole.RECEIVER,
        phone="+91-9845445566",
        verification_status="VERIFIED"
    )

    # Volunteers
    u_vol_ravi = models.User(
        name="Ravi Kumar",
        email="ravi.volunteer@annamitra.org",
        password=pwd_hash,
        role=models.UserRole.VOLUNTEER,
        phone="+91-9740112233",
        verification_status="VERIFIED"
    )
    u_vol_priya = models.User(
        name="Priya Singh",
        email="priya.volunteer@annamitra.org",
        password=pwd_hash,
        role=models.UserRole.VOLUNTEER,
        phone="+91-9740223344",
        verification_status="VERIFIED"
    )
    u_vol_amit = models.User(
        name="Amit Patel",
        email="amit.volunteer@annamitra.org",
        password=pwd_hash,
        role=models.UserRole.VOLUNTEER,
        phone="+91-9740334455",
        verification_status="VERIFIED"
    )

    # Admin
    u_admin = models.User(
        name="Dr. Ananya Sharma",
        email="admin@annamitra.org",
        password=pwd_hash,
        role=models.UserRole.ADMIN,
        phone="+91-9800000001",
        verification_status="VERIFIED"
    )

    db.add_all([
        u_bmsit, u_rvce, u_pg, u_event,
        u_rec_hospital, u_rec_shelter, u_rec_kitchen, u_rec_fridge,
        u_vol_ravi, u_vol_priya, u_vol_amit,
        u_admin
    ])
    db.commit()

    # 4. Historical Past Completed Donations (to give authentic ~3,200 kg & ~12,300 meals in metrics)
    now = datetime.utcnow()
    print("[*] Generating realistic historical rescue logs for past 30 days...")

    historical_records = [
        ("Paneer Rice & Sambar", "LUNCH", "VEG", 32.0, 110, rvce.id, u_rvce.id, u_rec_shelter.id, u_vol_ravi.id),
        ("Dal Makhani & Roti", "DINNER", "VEG", 28.0, 95, bmsit.id, u_bmsit.id, u_rec_hospital.id, u_vol_priya.id),
        ("Lemon Rice & Curd Rice", "LUNCH", "VEG", 22.0, 80, pg_cluster.id, u_pg.id, u_rec_kitchen.id, u_vol_amit.id),
        ("Veg Biryani & Raitha", "DINNER", "VEG", 45.0, 150, event_kitchen.id, u_event.id, u_rec_hospital.id, u_vol_ravi.id),
        ("Mixed Vegetable Khichdi", "LUNCH", "VEG", 30.0, 100, rvce.id, u_rvce.id, u_rec_shelter.id, u_vol_priya.id),
        ("Chapati & Chana Masala", "DINNER", "VEG", 35.0, 120, bmsit.id, u_bmsit.id, u_rec_fridge.id, u_vol_amit.id),
        ("Jeera Rice & Rajma", "LUNCH", "VEG", 26.0, 90, pg_cluster.id, u_pg.id, u_rec_kitchen.id, u_vol_ravi.id),
        ("South Indian Meals Platter", "LUNCH", "VEG", 40.0, 130, event_kitchen.id, u_event.id, u_rec_hospital.id, u_vol_priya.id),
    ]

    # Generate past batches to reach target metrics: ~3,240 kg, ~12,450 meals, and ~480 donations
    total_target_batches = 480
    avg_kg_per_batch = 3240.0 / total_target_batches  # ~6.75 kg
    avg_meals_per_batch = int(12450 / total_target_batches)  # ~26 meals

    for i in range(total_target_batches, 0, -1):
        day_offset = (i % 60) + 1
        item = historical_records[i % len(historical_records)]
        food_name, meal, diet, _, _, inst_id, d_id, r_id, v_id = item
        don_time = now - timedelta(days=day_offset, minutes=(i * 13) % 720)
        
        # Vary slightly around averages
        batch_kg = round(avg_kg_per_batch + ((i % 7) - 3) * 0.8, 1)
        batch_meals = int(avg_meals_per_batch + ((i % 11) - 5))

        past_don = models.FoodDonation(
            donor_id=d_id,
            institution_id=inst_id,
            food_name=food_name,
            meal_type=meal,
            dietary_type=diet,
            quantity_kg=batch_kg,
            servings=batch_meals,
            preparation_time=don_time - timedelta(hours=3),
            pickup_deadline=don_time,
            pickup_location="Campus Kitchen Dispatch Bay",
            latitude=12.9237 if inst_id == rvce.id else (13.1332 if inst_id == bmsit.id else 12.9352),
            longitude=77.4987 if inst_id == rvce.id else (77.5684 if inst_id == bmsit.id else 77.6245),
            status=models.DonationStatus.COMPLETED,
            priority_score=65.0,
            safety_confirmed=True,
            created_at=don_time - timedelta(hours=2)
        )
        db.add(past_don)
        db.flush()

        deliv = models.Delivery(
            donation_id=past_don.id,
            volunteer_id=v_id,
            receiver_id=r_id,
            pickup_time=don_time - timedelta(minutes=45),
            pickup_temperature=65.0 + (i % 5),
            delivery_time=don_time - timedelta(minutes=15),
            received_quantity_kg=past_don.quantity_kg,
            status="COMPLETED",
            pickup_latitude=past_don.latitude,
            pickup_longitude=past_don.longitude,
            delivery_latitude=12.9832,
            delivery_longitude=77.6019,
            proof="https://annamitra.org/proofs/delivery_verified.jpg",
            notes="Delivered successfully to facility supervisor. High quality affirmed."
        )
        db.add(deliv)

        imp = models.ImpactLog(
            donation_id=past_don.id,
            food_saved_kg=past_don.quantity_kg,
            meals_served=past_don.servings,
            co2e_avoided=round(past_don.quantity_kg * 2.5, 2),
            waste_cost_saved=round(past_don.quantity_kg * 4.0, 2),
            created_at=don_time
        )
        db.add(imp)

    db.commit()

    # 5. Live Active Donations in Various States (Ready for Demo Exploration)
    print("[*] Creating live active donations in AVAILABLE, CLAIMED, IN_TRANSIT, EXPIRED states...")

    # Active Donation 1: AVAILABLE from RVCE (Veg Pulao, 20 kg, 70 servings, expires in 2.5 hours)
    p_score1 = calculate_priority_score(20.0, now + timedelta(hours=2, minutes=30), rvce.latitude, rvce.longitude)
    don_avail1 = models.FoodDonation(
        donor_id=u_rvce.id,
        institution_id=rvce.id,
        food_name="Vegetable Pulao & Onion Raitha",
        meal_type="LUNCH",
        dietary_type="VEG",
        quantity_kg=20.0,
        servings=70,
        preparation_time=now - timedelta(hours=1),
        pickup_deadline=now + timedelta(hours=2, minutes=30),
        pickup_location="RVCE Campus Mess Gate 2, Mysore Road",
        latitude=rvce.latitude,
        longitude=rvce.longitude,
        status=models.DonationStatus.AVAILABLE,
        priority_score=p_score1["score"],
        safety_confirmed=True,
        created_at=now - timedelta(minutes=30)
    )

    # Active Donation 2: AVAILABLE from Koramangala PG (Dal Rice, 15 kg, 50 servings, expires in 1.5 hours)
    p_score2 = calculate_priority_score(15.0, now + timedelta(hours=1, minutes=30), pg_cluster.latitude, pg_cluster.longitude)
    don_avail2 = models.FoodDonation(
        donor_id=u_pg.id,
        institution_id=pg_cluster.id,
        food_name="Steamed Rice & Sambhar Dal",
        meal_type="LUNCH",
        dietary_type="VEG",
        quantity_kg=15.0,
        servings=50,
        preparation_time=now - timedelta(hours=1, minutes=15),
        pickup_deadline=now + timedelta(hours=1, minutes=30),
        pickup_location="80 Feet Road, 5th Block Koramangala",
        latitude=pg_cluster.latitude,
        longitude=pg_cluster.longitude,
        status=models.DonationStatus.AVAILABLE,
        priority_score=p_score2["score"],
        safety_confirmed=True,
        created_at=now - timedelta(minutes=45)
    )

    # Active Donation 3: AVAILABLE from Event Kitchen (URGENT! 40 mins remaining)
    p_score3 = calculate_priority_score(35.0, now + timedelta(minutes=40), event_kitchen.latitude, event_kitchen.longitude)
    don_avail3 = models.FoodDonation(
        donor_id=u_event.id,
        institution_id=event_kitchen.id,
        food_name="Paneer Butter Masala & Roti",
        meal_type="LUNCH",
        dietary_type="VEG",
        quantity_kg=35.0,
        servings=110,
        preparation_time=now - timedelta(hours=2),
        pickup_deadline=now + timedelta(minutes=40),
        pickup_location="100 Feet Road, Indiranagar",
        latitude=event_kitchen.latitude,
        longitude=event_kitchen.longitude,
        status=models.DonationStatus.AVAILABLE,
        priority_score=p_score3["score"],
        safety_confirmed=True,
        created_at=now - timedelta(minutes=50)
    )

    # Active Donation 4: CLAIMED by Majestic Shelter (awaiting volunteer pickup)
    p_score4 = calculate_priority_score(24.0, now + timedelta(hours=1, minutes=45), rvce.latitude, rvce.longitude)
    don_claimed = models.FoodDonation(
        donor_id=u_rvce.id,
        institution_id=rvce.id,
        food_name="South Indian Bisibelebath",
        meal_type="LUNCH",
        dietary_type="VEG",
        quantity_kg=24.0,
        servings=80,
        preparation_time=now - timedelta(hours=1, minutes=30),
        pickup_deadline=now + timedelta(hours=1, minutes=45),
        pickup_location="RVCE Campus Mess Gate 2",
        latitude=rvce.latitude,
        longitude=rvce.longitude,
        status=models.DonationStatus.CLAIMED,
        priority_score=p_score4["score"],
        safety_confirmed=True,
        created_at=now - timedelta(minutes=40)
    )
    db.add_all([don_avail1, don_avail2, don_avail3, don_claimed])
    db.flush()

    deliv_claimed = models.Delivery(
        donation_id=don_claimed.id,
        receiver_id=u_rec_shelter.id,
        status="CLAIMED",
        pickup_latitude=don_claimed.latitude,
        pickup_longitude=don_claimed.longitude,
        delivery_latitude=dp_shelter.latitude,
        delivery_longitude=dp_shelter.longitude
    )
    db.add(deliv_claimed)

    # Active Donation 5: IN_TRANSIT (Volunteer Priya is delivering to Community Fridge)
    p_score5 = calculate_priority_score(18.0, now + timedelta(hours=1), pg_cluster.latitude, pg_cluster.longitude)
    don_transit = models.FoodDonation(
        donor_id=u_pg.id,
        institution_id=pg_cluster.id,
        food_name="Curd Rice & Vegetable Upma",
        meal_type="BREAKFAST",
        dietary_type="VEG",
        quantity_kg=18.0,
        servings=60,
        preparation_time=now - timedelta(hours=2),
        pickup_deadline=now + timedelta(hours=1),
        pickup_location="5th Block Koramangala",
        latitude=pg_cluster.latitude,
        longitude=pg_cluster.longitude,
        status=models.DonationStatus.IN_TRANSIT,
        priority_score=p_score5["score"],
        safety_confirmed=True,
        created_at=now - timedelta(hours=1, minutes=15)
    )
    db.add(don_transit)
    db.flush()

    deliv_transit = models.Delivery(
        donation_id=don_transit.id,
        volunteer_id=u_vol_priya.id,
        receiver_id=u_rec_fridge.id,
        pickup_time=now - timedelta(minutes=20),
        pickup_temperature=64.0,
        status="IN_TRANSIT",
        pickup_latitude=don_transit.latitude,
        pickup_longitude=don_transit.longitude,
        delivery_latitude=dp_fridge.latitude,
        delivery_longitude=dp_fridge.longitude,
        notes="Picked up in insulated carrier, transit via EV scooter."
    )
    db.add(deliv_transit)

    # Active Donation 6: EXPIRED (From yesterday to demonstrate automatic expiry enforcement)
    don_expired = models.FoodDonation(
        donor_id=u_event.id,
        institution_id=event_kitchen.id,
        food_name="Morning Idli & Chutney",
        meal_type="BREAKFAST",
        dietary_type="VEG",
        quantity_kg=14.0,
        servings=45,
        preparation_time=now - timedelta(days=1, hours=6),
        pickup_deadline=now - timedelta(days=1, hours=2),
        pickup_location="Indiranagar Event Hall",
        latitude=event_kitchen.latitude,
        longitude=event_kitchen.longitude,
        status=models.DonationStatus.EXPIRED,
        priority_score=0.0,
        safety_confirmed=True,
        created_at=now - timedelta(days=1, hours=6)
    )
    db.add(don_expired)

    db.commit()

    # Calculate and print current total impact metrics
    all_imp = db.query(models.ImpactLog).all()
    total_kg = sum(i.food_saved_kg for i in all_imp)
    total_meals = sum(i.meals_served for i in all_imp)
    total_co2e = sum(i.co2e_avoided for i in all_imp)
    total_waste_fee = sum(i.waste_cost_saved for i in all_imp)

    print("\n" + "="*60)
    print("✅ ANNAMITRA SEEDING COMPLETE!")
    print(f"📊 Total Rescued Food Saved: {total_kg:,.1f} kg")
    print(f"🍱 Total Nutritious Meals Served: {total_meals:,} meals")
    print(f"🌱 Total CO2e Avoided: {total_co2e:,.1f} kg CO2e")
    print(f"💰 Total Waste Fee Saved: ₹ {total_waste_fee:,.2f}")
    print("="*60)
    print("Demo Accounts Ready:")
    print("  • Donor: BMSIT College Mess (mess@bmsit.in / demo123)")
    print("  • Receiver: Hospital Caretaker Food Hub (caretakers@bowring.org / demo123)")
    print("  • Volunteer: Ravi Kumar (ravi.volunteer@annamitra.org / demo123)")
    print("  • Admin: Dr. Ananya Sharma (admin@annamitra.org / demo123)")
    print("="*60 + "\n")

if __name__ == "__main__":
    seed_database()
