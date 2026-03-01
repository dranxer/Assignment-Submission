"""Add sample sales data for today"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Sale, Medicine, PurchaseOrder, get_db

db = Session(bind=engine)
today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

# Clear existing sales
db.query(Sale).delete()

# Sample sales (today's sales)
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

# Clear existing purchase orders and add new ones
db.query(PurchaseOrder).delete()

purchase_orders_data = [
    {"medicine_id": 9, "medicine_name": "Azithromycin 500mg", "quantity": 50, "cost": 500.00, "expected_delivery": today + timedelta(days=7), "status": "Pending"},
    {"medicine_id": 6, "medicine_name": "Metformin 500mg", "quantity": 100, "cost": 200.00, "expected_delivery": today + timedelta(days=5), "status": "Pending"},
    {"medicine_id": 7, "medicine_name": "Atorvastatin 10mg", "quantity": 75, "cost": 375.00, "expected_delivery": today + timedelta(days=3), "status": "Pending"},
    {"medicine_id": 12, "medicine_name": "Pantoprazole 40mg", "quantity": 60, "cost": 270.00, "expected_delivery": today + timedelta(days=4), "status": "Pending"},
]

for po_data in purchase_orders_data:
    po = PurchaseOrder(**po_data)
    db.add(po)

db.commit()
print(f"Added {len(sales_data)} sales and {len(purchase_orders_data)} purchase orders for today!")
db.close()
