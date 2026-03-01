from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from datetime import datetime
from app.database import get_db, Medicine, MedicineStatus
from app.schemas import (
    MedicineCreate, MedicineUpdate, MedicineResponse, InventorySummary
)
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


def update_medicine_status(db: Session, medicine: Medicine):
    """Update medicine status based on quantity and expiry date"""
    if medicine.expiry_date and medicine.expiry_date < datetime.utcnow():
        medicine.status = MedicineStatus.EXPIRED.value
    elif medicine.quantity == 0:
        medicine.status = MedicineStatus.OUT_OF_STOCK.value
    elif medicine.quantity < 10:
        medicine.status = MedicineStatus.LOW_STOCK.value
    else:
        medicine.status = MedicineStatus.ACTIVE.value
    db.add(medicine)
    db.commit()
    db.refresh(medicine)


class StatusUpdate(BaseModel):
    status: str


# Define specific routes FIRST before parameterized routes
@router.get("/summary", response_model=InventorySummary)
def get_inventory_summary(db: Session = Depends(get_db)):
    """Get inventory overview summary"""
    total_items = db.query(func.count(Medicine.id)).scalar() or 0
    active_stock = db.query(func.count(Medicine.id)).filter(
        Medicine.status == MedicineStatus.ACTIVE.value
    ).scalar() or 0
    low_stock = db.query(func.count(Medicine.id)).filter(
        Medicine.status == MedicineStatus.LOW_STOCK.value
    ).scalar() or 0

    total_value = db.query(func.sum(Medicine.mrp * Medicine.quantity)).scalar() or 0.0

    return InventorySummary(
        total_items=total_items,
        active_stock=active_stock,
        low_stock=low_stock,
        total_value=total_value
    )


@router.get("", response_model=list[MedicineResponse])
def list_medicines(
    search: Optional[str] = Query(""),
    status: Optional[str] = Query(""),
    db: Session = Depends(get_db)
):
    """List all medicines with optional search and filtering"""
    query = db.query(Medicine)

    if search:
        query = query.filter(
            or_(
                Medicine.name.ilike(f"%{search}%"),
                Medicine.category.ilike(f"%{search}%")
            )
        )

    if status:
        query = query.filter(Medicine.status == status)

    medicines = query.all()
    # Update status for each medicine before returning
    for med in medicines:
        update_medicine_status(db, med)
    return medicines


@router.get("/{medicine_id}", response_model=MedicineResponse)
def get_medicine(medicine_id: int, db: Session = Depends(get_db)):
    """Get a specific medicine by ID"""
    medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    update_medicine_status(db, medicine)
    return medicine


@router.post("", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    """Add a new medicine to inventory"""
    # Check if medicine with same name already exists
    existing = db.query(Medicine).filter(Medicine.name == medicine.name).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Medicine '{medicine.name}' already exists")

    # Validate expiry date
    if medicine.expiry_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Expiry date cannot be in the past")

    # Determine status based on quantity and expiry
    expiry_date = medicine.expiry_date
    quantity = medicine.quantity
    
    if expiry_date < datetime.utcnow():
        status_val = "Expired"
    elif quantity == 0:
        status_val = "Out of Stock"
    elif quantity < 10:
        status_val = "Low Stock"
    else:
        status_val = "Active"

    db_medicine = Medicine(
        name=medicine.name,
        generic_name=medicine.generic_name,
        category=medicine.category,
        batch_no=medicine.batch_no,
        expiry_date=medicine.expiry_date,
        quantity=medicine.quantity,
        cost_price=medicine.cost_price,
        mrp=medicine.mrp,
        supplier=medicine.supplier,
        status=status_val
    )
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


@router.put("/{medicine_id}", response_model=MedicineResponse)
def update_medicine(
    medicine_id: int,
    medicine_update: MedicineUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing medicine"""
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    update_data = medicine_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_medicine, field, value)

    update_medicine_status(db, db_medicine)
    return db_medicine


@router.patch("/{medicine_id}/status", response_model=MedicineResponse)
def update_medicine_status_endpoint(
    medicine_id: int,
    status_update: StatusUpdate,
    db: Session = Depends(get_db)
):
    """Update medicine status (e.g., mark as Out of Stock)"""
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    db_medicine.status = status_update.status
    if status_update.status == MedicineStatus.OUT_OF_STOCK.value:
        db_medicine.quantity = 0
    db_medicine.updated_at = datetime.utcnow()
    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)
    return db_medicine


@router.delete("/{medicine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medicine(medicine_id: int, db: Session = Depends(get_db)):
    """Delete a medicine from inventory"""
    db_medicine = db.query(Medicine).filter(Medicine.id == medicine_id).first()
    if not db_medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    db.delete(db_medicine)
    db.commit()
    return None
