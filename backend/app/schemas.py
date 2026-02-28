from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class MedicineBase(BaseModel):
    name: str
    generic_name: str
    category: str
    batch_no: str
    expiry_date: datetime
    quantity: int
    cost_price: float
    mrp: float
    supplier: str


class MedicineCreate(MedicineBase):
    pass


class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    category: Optional[str] = None
    batch_no: Optional[str] = None
    expiry_date: Optional[datetime] = None
    quantity: Optional[int] = None
    cost_price: Optional[float] = None
    mrp: Optional[float] = None
    supplier: Optional[str] = None
    status: Optional[str] = None


class MedicineResponse(MedicineBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    medicine_id: int
    medicine_name: str
    quantity: int
    amount: float


class SaleCreate(SaleBase):
    pass


class SaleResponse(SaleBase):
    id: int
    sale_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class PurchaseOrderBase(BaseModel):
    medicine_id: int
    medicine_name: str
    quantity: int
    cost: float
    expected_delivery: datetime
    status: str = "Pending"


class PurchaseOrderCreate(PurchaseOrderBase):
    pass


class PurchaseOrderResponse(PurchaseOrderBase):
    id: int
    order_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class SalesSummary(BaseModel):
    total_sales: float
    items_sold: int
    low_stock_items: int
    purchase_orders_pending: int


class InventorySummary(BaseModel):
    total_items: int
    active_stock: int
    low_stock: int
    total_value: float
