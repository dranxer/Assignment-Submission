from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from app.database import get_db, Sale, PurchaseOrder, Medicine
from app.schemas import SaleResponse, SaleCreate, PurchaseOrderResponse, PurchaseOrderCreate

router = APIRouter(prefix="/api", tags=["sales", "purchase-orders"])


# ==================== SALES ENDPOINTS ====================

@router.post("/sales", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """Record a new sale"""
    # Verify medicine exists
    medicine = db.query(Medicine).filter(Medicine.id == sale.medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Check stock availability
    if medicine.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock available")
    
    # Create sale record
    db_sale = Sale(
        medicine_id=sale.medicine_id,
        medicine_name=sale.medicine_name,
        quantity=sale.quantity,
        amount=sale.amount,
        sale_date=datetime.utcnow()
    )
    db.add(db_sale)
    
    # Reduce medicine stock
    medicine.quantity -= sale.quantity
    # Update status if needed
    if medicine.quantity == 0:
        medicine.status = "Out of Stock"
    elif medicine.quantity < 10:
        medicine.status = "Low Stock"
    
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.get("/sales", response_model=list[SaleResponse])
def list_sales(
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List recent sales"""
    sales = db.query(Sale).order_by(Sale.sale_date.desc()).limit(limit).all()
    return sales


# ==================== PURCHASE ORDER ENDPOINTS ====================

@router.post("/purchase-orders", response_model=PurchaseOrderResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(po: PurchaseOrderCreate, db: Session = Depends(get_db)):
    """Create a new purchase order"""
    # Verify medicine exists
    medicine = db.query(Medicine).filter(Medicine.id == po.medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Create purchase order
    db_po = PurchaseOrder(
        medicine_id=po.medicine_id,
        medicine_name=po.medicine_name,
        quantity=po.quantity,
        cost=po.cost,
        expected_delivery=po.expected_delivery,
        status=po.status or "Pending",
        order_date=datetime.utcnow()
    )
    db.add(db_po)
    db.commit()
    db.refresh(db_po)
    return db_po


@router.get("/purchase-orders", response_model=list[PurchaseOrderResponse])
def list_purchase_orders(
    status_filter: str = Query("Pending", alias="status"),
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """List purchase orders"""
    query = db.query(PurchaseOrder)
    if status_filter:
        query = query.filter(PurchaseOrder.status == status_filter)
    orders = query.order_by(PurchaseOrder.expected_delivery.asc()).limit(limit).all()
    return orders


@router.patch("/purchase-orders/{po_id}/receive", response_model=PurchaseOrderResponse)
def receive_purchase_order(po_id: int, db: Session = Depends(get_db)):
    """Receive a purchase order and update medicine stock"""
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    # Update medicine stock
    medicine = db.query(Medicine).filter(Medicine.id == po.medicine_id).first()
    if medicine:
        medicine.quantity += po.quantity
        # Update status
        if medicine.quantity >= 10:
            medicine.status = "Active"
    
    # Update purchase order status
    po.status = "Received"
    db.commit()
    db.refresh(po)
    return po


@router.delete("/purchase-orders/{po_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_purchase_order(po_id: int, db: Session = Depends(get_db)):
    """Cancel a purchase order"""
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    db.delete(po)
    db.commit()
    return None
