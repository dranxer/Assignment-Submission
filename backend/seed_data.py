"""
Seed script to populate the database with sample data for testing.
Run this after starting the backend for the first time.
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Medicine, Sale, PurchaseOrder, MedicineStatus, Base, get_db


def seed_database():
    """Populate database with sample pharmacy data"""
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal = Session(bind=engine)
    
    try:
        # Check if data already exists
        if db.query(Medicine).count() > 0:
            print("Database already seeded. Skipping...")
            return
        
        # Sample medicines
        medicines_data = [
            {
                "name": "Paracetamol 500mg",
                "generic_name": "Paracetamol",
                "category": "Analgesic",
                "batch_no": "PAR-2024-001",
                "expiry_date": datetime(2026, 12, 1),
                "quantity": 150,
                "cost_price": 2.50,
                "mrp": 5.00,
                "supplier": "MediCorp Pharmaceuticals"
            },
            {
                "name": "Amoxicillin 250mg",
                "generic_name": "Amoxicillin",
                "category": "Antibiotic",
                "batch_no": "AMX-2024-002",
                "expiry_date": datetime(2026, 6, 15),
                "quantity": 80,
                "cost_price": 8.00,
                "mrp": 15.00,
                "supplier": "PharmaLife Inc"
            },
            {
                "name": "Ibuprofen 400mg",
                "generic_name": "Ibuprofen",
                "category": "Analgesic",
                "batch_no": "IBU-2024-003",
                "expiry_date": datetime(2026, 9, 20),
                "quantity": 120,
                "cost_price": 3.00,
                "mrp": 7.50,
                "supplier": "MediCorp Pharmaceuticals"
            },
            {
                "name": "Cetirizine 10mg",
                "generic_name": "Cetirizine",
                "category": "Antihistamine",
                "batch_no": "CET-2024-004",
                "expiry_date": datetime(2026, 3, 10),
                "quantity": 200,
                "cost_price": 1.50,
                "mrp": 4.00,
                "supplier": "HealthFirst Distributors"
            },
            {
                "name": "Omeprazole 20mg",
                "generic_name": "Omeprazole",
                "category": "Antacid",
                "batch_no": "OMP-2024-005",
                "expiry_date": datetime(2026, 8, 25),
                "quantity": 90,
                "cost_price": 4.00,
                "mrp": 10.00,
                "supplier": "PharmaLife Inc"
            },
            {
                "name": "Metformin 500mg",
                "generic_name": "Metformin",
                "category": "Antidiabetic",
                "batch_no": "MET-2024-006",
                "expiry_date": datetime(2026, 11, 30),
                "quantity": 5,
                "cost_price": 2.00,
                "mrp": 6.00,
                "supplier": "MediCorp Pharmaceuticals"
            },
            {
                "name": "Atorvastatin 10mg",
                "generic_name": "Atorvastatin",
                "category": "Cardiovascular",
                "batch_no": "ATV-2024-007",
                "expiry_date": datetime(2026, 7, 15),
                "quantity": 8,
                "cost_price": 5.00,
                "mrp": 12.00,
                "supplier": "HealthFirst Distributors"
            },
            {
                "name": "Aspirin 75mg",
                "generic_name": "Aspirin",
                "category": "Cardiovascular",
                "batch_no": "ASP-2024-008",
                "expiry_date": datetime(2025, 12, 31),
                "quantity": 300,
                "cost_price": 1.00,
                "mrp": 3.00,
                "supplier": "PharmaLife Inc"
            },
            {
                "name": "Azithromycin 500mg",
                "generic_name": "Azithromycin",
                "category": "Antibiotic",
                "batch_no": "AZI-2024-009",
                "expiry_date": datetime(2026, 4, 20),
                "quantity": 0,
                "cost_price": 10.00,
                "mrp": 25.00,
                "supplier": "MediCorp Pharmaceuticals"
            },
            {
                "name": "Prednisone 5mg",
                "generic_name": "Prednisone",
                "category": "Corticosteroid",
                "batch_no": "PRD-2024-010",
                "expiry_date": datetime(2026, 10, 5),
                "quantity": 45,
                "cost_price": 3.50,
                "mrp": 8.00,
                "supplier": "HealthFirst Distributors"
            },
            {
                "name": "Vitamin D3 1000IU",
                "generic_name": "Cholecalciferol",
                "category": "Supplement",
                "batch_no": "VTD-2024-011",
                "expiry_date": datetime(2027, 1, 15),
                "quantity": 250,
                "cost_price": 2.00,
                "mrp": 6.00,
                "supplier": "Wellness Supplies Co"
            },
            {
                "name": "Pantoprazole 40mg",
                "generic_name": "Pantoprazole",
                "category": "Antacid",
                "batch_no": "PNT-2024-012",
                "expiry_date": datetime(2026, 5, 28),
                "quantity": 3,
                "cost_price": 4.50,
                "mrp": 11.00,
                "supplier": "PharmaLife Inc"
            }
        ]
        
        # Create medicines
        medicines = []
        for med_data in medicines_data:
            medicine = Medicine(**med_data)
            db.add(medicine)
            medicines.append(medicine)
        
        db.commit()
        
        # Update status for all medicines
        for med in medicines:
            if med.expiry_date < datetime.utcnow():
                med.status = MedicineStatus.EXPIRED.value
            elif med.quantity == 0:
                med.status = MedicineStatus.OUT_OF_STOCK.value
            elif med.quantity < 10:
                med.status = MedicineStatus.LOW_STOCK.value
            else:
                med.status = MedicineStatus.ACTIVE.value
        
        db.commit()
        
        # Sample sales (today's sales)
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        sales_data = [
            {"medicine_id": 1, "medicine_name": "Paracetamol 500mg", "quantity": 10, "amount": 50.00, "sale_date": today + timedelta(hours=9)},
            {"medicine_id": 2, "medicine_name": "Amoxicillin 250mg", "quantity": 5, "amount": 75.00, "sale_date": today + timedelta(hours=10)},
            {"medicine_id": 3, "medicine_name": "Ibuprofen 400mg", "quantity": 8, "amount": 60.00, "sale_date": today + timedelta(hours=11)},
            {"medicine_id": 4, "medicine_name": "Cetirizine 10mg", "quantity": 15, "amount": 60.00, "sale_date": today + timedelta(hours=12)},
            {"medicine_id": 5, "medicine_name": "Omeprazole 20mg", "quantity": 6, "amount": 60.00, "sale_date": today + timedelta(hours=13)},
            {"medicine_id": 8, "medicine_name": "Aspirin 75mg", "quantity": 20, "amount": 60.00, "sale_date": today + timedelta(hours=14)},
            {"medicine_id": 10, "medicine_name": "Prednisone 5mg", "quantity": 4, "amount": 32.00, "sale_date": today + timedelta(hours=15)},
            {"medicine_id": 11, "medicine_name": "Vitamin D3 1000IU", "quantity": 12, "amount": 72.00, "sale_date": today + timedelta(hours=16)},
        ]
        
        for sale_data in sales_data:
            sale = Sale(**sale_data)
            db.add(sale)
        
        db.commit()
        
        # Sample purchase orders
        purchase_orders_data = [
            {
                "medicine_id": 9,
                "medicine_name": "Azithromycin 500mg",
                "quantity": 50,
                "cost": 500.00,
                "expected_delivery": datetime.utcnow() + timedelta(days=7),
                "status": "Pending"
            },
            {
                "medicine_id": 6,
                "medicine_name": "Metformin 500mg",
                "quantity": 100,
                "cost": 200.00,
                "expected_delivery": datetime.utcnow() + timedelta(days=5),
                "status": "Pending"
            },
            {
                "medicine_id": 7,
                "medicine_name": "Atorvastatin 10mg",
                "quantity": 75,
                "cost": 375.00,
                "expected_delivery": datetime.utcnow() + timedelta(days=3),
                "status": "Pending"
            },
            {
                "medicine_id": 12,
                "medicine_name": "Pantoprazole 40mg",
                "quantity": 60,
                "cost": 270.00,
                "expected_delivery": datetime.utcnow() + timedelta(days=4),
                "status": "Pending"
            }
        ]
        
        for po_data in purchase_orders_data:
            po = PurchaseOrder(**po_data)
            db.add(po)
        
        db.commit()
        
        print("[OK] Database seeded successfully!")
        print(f"   - {len(medicines)} medicines added")
        print(f"   - {len(sales_data)} sales records added")
        print(f"   - {len(purchase_orders_data)} purchase orders added")
        print("\nStatus breakdown:")
        print(f"   - Active: {db.query(Medicine).filter(Medicine.status == MedicineStatus.ACTIVE.value).count()}")
        print(f"   - Low Stock: {db.query(Medicine).filter(Medicine.status == MedicineStatus.LOW_STOCK.value).count()}")
        print(f"   - Out of Stock: {db.query(Medicine).filter(Medicine.status == MedicineStatus.OUT_OF_STOCK.value).count()}")
        
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
