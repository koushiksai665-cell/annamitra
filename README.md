# 🍱 Annamitra (अन्नमित्र)

**Urban Surplus Food Rescue & Redistribution Platform**  
*Optimized for Institutional Kitchens, Hostels, PGs, and Events in Bengaluru*

---

## 🌟 Overview
**Annamitra** bridges the gap between institutional food surplus (colleges, hostel messes, commercial PGs, banquet halls) and vulnerable urban beneficiaries (hospital patient caretakers, transit shelters, community kitchens).

The platform combines real-time urgency scoring, geospatial clustering (1.5 km proximity grouping), food safety temperature verification, and institutional sustainability reporting (NAAC/NIRF social responsibility dossiers).

---

## 🚀 Key Features

- **Urgent Expiry Scoring Engine**: Dynamic multi-factor scoring (up to 50 pts for time to expiry, 30 pts for quantity, 20 pts for distance).
- **Proximity Batch Clustering**: Auto-clusters active donations within a 1.5 km radius into consolidated single-trip volunteer pickup routes.
- **Beneficiary Matching**: Algorithmically recommends the nearest eligible distribution point with sufficient holding capacity.
- **Food Safety Safeguards**: Validates temperature at pickup (hot holding $\ge 60^\circ\text{C}$, cold chain $\le 10^\circ\text{C}$) to guarantee food hygiene.
- **NAAC / CSR Social Responsibility Reporting**: One-click generation of official audit PDF certificates detailing kilograms rescued, meals served, carbon avoided, and waste management savings.
- **Interactive Multi-Role UI**: Role switching between Institutional Donor, Volunteer, Receiver NGO, and Administrator with live OpenStreetMap/Leaflet integration.

---

## 🏗️ Architecture & Tech Stack

- **Backend**: Python 3.12+, FastAPI, SQLAlchemy, SQLite, Pydantic v2
- **PDF Generation**: ReportLab
- **Frontend**: Vanilla JavaScript (ES6+), Tailwind CSS, Lucide Icons, Leaflet.js (OpenStreetMap), Chart.js
- **Algorithms**: Haversine distance matrix, greedy radius clustering, priority decay scoring

---

## 📁 Repository Structure

```
annamitra/
├── main.py                 # FastAPI application, REST endpoints & static server
├── models.py               # SQLAlchemy ORM models
├── schemas.py              # Pydantic request/response schemas
├── database.py             # Database engine & session configuration
├── clustering.py           # Haversine distance, priority scoring & route clustering
├── logistics.py            # Food safety temperature validation engine
├── pdf_generator.py        # NAAC / NIRF audit PDF certificate generator
├── auth.py                 # Role authorization & redirect helpers
├── seed.py                 # Comprehensive seed data for Bengaluru
├── requirements.txt        # Python package dependencies
├── routes/
│   └── logistics.py        # Sub-router for logistics and safety thresholds
└── static/
    ├── index.html          # Single Page Application dashboard
    ├── script.js           # Client-side state management & live counters
    └── style.css           # Custom styles & animations
```

---

## 🛠️ Getting Started

### 1. Clone or Open the Repository
```bash
git clone https://github.com/koushiksai665-cell/annamitra.git
cd annamitra
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize & Seed Database
```bash
python seed.py
```

### 4. Run the Application
```bash
uvicorn main:app --reload --port 8000
```

### 5. Access Dashboards & APIs
- **Web App**: [http://localhost:8000](http://localhost:8000)
- **Interactive API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative Docs (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
