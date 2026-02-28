from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.database import get_db, Medicine, Sale, PurchaseOrder
from app.schemas import (
    SalesSummary, MedicineResponse, InventorySummary, SaleResponse,
    PurchaseOrderResponse
)
from pydantic import BaseModel

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


class DashboardSummary(BaseModel):
    today_sales: float
    items_sold: int
    low_stock_count: int
    purchase_orders: float


class RecentSale(BaseModel):
    id: int
    invoice: str
    amount: float


@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary with today's sales, items sold, low stock count, and purchase orders"""
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)

    # Today's sales
    total_sales = db.query(func.sum(Sale.amount)).filter(
        and_(Sale.sale_date >= today, Sale.sale_date < tomorrow)
    ).scalar() or 0.0

    # Items sold today
    items_sold = db.query(func.sum(Sale.quantity)).filter(
        and_(Sale.sale_date >= today, Sale.sale_date < tomorrow)
    ).scalar() or 0

    # Low stock count
    low_stock_count = db.query(func.count(Medicine.id)).filter(
        Medicine.quantity < 10
    ).scalar() or 0

    # Total purchase orders value (pending)
    purchase_orders = db.query(func.sum(PurchaseOrder.cost)).filter(
        PurchaseOrder.status == "Pending"
    ).scalar() or 0.0

    return DashboardSummary(
        today_sales=total_sales,
        items_sold=items_sold,
        low_stock_count=low_stock_count,
        purchase_orders=purchase_orders
    )


@router.get("/recent-sales", response_model=list[RecentSale])
def get_recent_sales(limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    """Get recent sales with invoice numbers"""
    sales = db.query(Sale).order_by(Sale.sale_date.desc()).limit(limit).all()
    return [RecentSale(id=s.id, invoice=f"INV-2024-{s.id:04d}", amount=s.amount) for s in sales]
