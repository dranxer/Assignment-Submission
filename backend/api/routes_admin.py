import sys
import os

# Add backend folder to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import APIRouter
from app.database import SessionLocal, Medicine, Sale, PurchaseOrder, MedicineStatus, Base
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/admin", tags=["admin"])

@router.post("/seed")
def seed_database():
    """Seed database with sample data"""
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Medicine).count() > 0:
            return {"status": "skipped", "message": "Database already seeded"}
        
        today = datetime.utcnow()
        
        # Sample medicines with status
        medicines_data = [
            {"name": "Paracetamol 500mg", "generic_name": "Paracetamol", "category": "Analgesic", "batch_no": "PAR-2024-001", "expiry_date": datetime(2026, 12, 1), "quantity": 150, "cost_price": 2.50, "mrp": 5.00, "supplier": "MediCorp Pharmaceuticals", "status": "Active"},
            {"name": "Amoxicillin 250mg", "generic_name": "Amoxicillin", "category": "Antibiotic", "batch_no": "AMX-2024-002", "expiry_date": datetime(2026, 6, 15), "quantity": 80, "cost_price": 8.00, "mrp": 15.00, "supplier": "PharmaLife Inc", "status": "Active"},
            {"name": "Ibuprofen 400mg", "generic_name": "Ibuprofen", "category": "Analgesic", "batch_no": "IBU-2024-003", "expiry_date": datetime(2026, 9, 20), "quantity": 120, "cost_price": 3.00, "mrp": 7.50, "supplier": "MediCorp Pharmaceuticals", "status": "Active"},
            {"name": "Cetirizine 10mg", "generic_name": "Cetirizine", "category": "Antihistamine", "batch_no": "CET-2024-004", "expiry_date": datetime(2026, 3, 10), "quantity": 200, "cost_price": 1.50, "mrp": 4.00, "supplier": "HealthFirst Distributors", "status": "Active"},
            {"name": "Omeprazole 20mg", "generic_name": "Omeprazole", "category": "Antacid", "batch_no": "OMP-2024-005", "expiry_date": datetime(2026, 8, 25), "quantity": 90, "cost_price": 4.00, "mrp": 10.00, "supplier": "PharmaLife Inc", "status": "Active"},
            {"name": "Metformin 500mg", "generic_name": "Metformin", "category": "Antidiabetic", "batch_no": "MET-2024-006", "expiry_date": datetime(2026, 11, 30), "quantity": 5, "cost_price": 2.00, "mrp": 6.00, "supplier": "MediCorp Pharmaceuticals", "status": "Low Stock"},
            {"name": "Atorvastatin 10mg", "generic_name": "Atorvastatin", "category": "Cardiovascular", "batch_no": "ATV-2024-007", "expiry_date": datetime(2026, 7, 15), "quantity": 8, "cost_price": 5.00, "mrp": 12.00, "supplier": "HealthFirst Distributors", "status": "Low Stock"},
            {"name": "Aspirin 75mg", "generic_name": "Aspirin", "category": "Cardiovascular", "batch_no": "ASP-2024-008", "expiry_date": datetime(2025, 12, 31), "quantity": 300, "cost_price": 1.00, "mrp": 3.00, "supplier": "PharmaLife Inc", "status": "Expired"},
            {"name": "Azithromycin 500mg", "generic_name": "Azithromycin", "category": "Antibiotic", "batch_no": "AZI-2024-009", "expiry_date": datetime(2026, 4, 20), "quantity": 0, "cost_price": 10.00, "mrp": 25.00, "supplier": "MediCorp Pharmaceuticals", "status": "Out of Stock"},
            {"name": "Prednisone 5mg", "generic_name": "Prednisone", "category": "Corticosteroid", "batch_no": "PRD-2024-010", "expiry_date": datetime(2026, 10, 5), "quantity": 45, "cost_price": 3.50, "mrp": 8.00, "supplier": "HealthFirst Distributors", "status": "Active"},
            {"name": "Vitamin D3 1000IU", "generic_name": "Cholecalciferol", "category": "Supplement", "batch_no": "VTD-2024-011", "expiry_date": datetime(2027, 1, 15), "quantity": 250, "cost_price": 2.00, "mrp": 6.00, "supplier": "Wellness Supplies Co", "status": "Active"},
            {"name": "Pantoprazole 40mg", "generic_name": "Pantoprazole", "category": "Antacid", "batch_no": "PNT-2024-012", "expiry_date": datetime(2026, 5, 28), "quantity": 3, "cost_price": 4.50, "mrp": 11.00, "supplier": "PharmaLife Inc", "status": "Low Stock"},
        ]
        
        for med_data in medicines_data:
            db.add(Medicine(**med_data))
        db.commit()
        
        return {"status": "success", "medicines": len(medicines_data)}
    
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
