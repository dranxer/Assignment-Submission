# Pharmacy CRM API - Technical Documentation

## Overview

This REST API provides a complete pharmacy management system built with **FastAPI** (Python) and **SQLAlchemy** ORM. It supports inventory management, sales tracking, and purchase order management with automatic data consistency enforcement.

---

## API Structure

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Inventory Management (`/api/inventory`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/inventory` | List all medicines (supports `?search=` and `?status=` filters) |
| `GET` | `/api/inventory/{id}` | Get a specific medicine by ID |
| `GET` | `/api/inventory/summary` | Get inventory summary statistics |
| `POST` | `/api/inventory` | Add a new medicine |
| `PUT` | `/api/inventory/{id}` | Update an existing medicine |
| `PATCH` | `/api/inventory/{id}/status` | Update medicine status only |
| `DELETE` | `/api/inventory/{id}` | Delete a medicine |

#### 2. Sales Management (`/api/sales`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/sales` | List recent sales (default: 50, max: 500) |
| `POST` | `/api/sales` | Record a new sale |

#### 3. Purchase Orders (`/api/purchase-orders`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/purchase-orders` | List purchase orders (supports `?status=` filter) |
| `POST` | `/api/purchase-orders` | Create a new purchase order |
| `PATCH` | `/api/purchase-orders/{id}/receive` | Receive order and update stock |
| `DELETE` | `/api/purchase-orders/{id}` | Cancel a purchase order |

#### 4. Dashboard (`/api/dashboard`)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/dashboard/summary` | Get dashboard summary (today's sales, items sold, low stock count) |
| `GET` | `/api/dashboard/recent-sales` | Get recent sales with invoice numbers |

---

## Data Consistency Mechanisms

### 1. Automatic Status Management

The API automatically updates medicine status based on business rules:

```python
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
```

**Status Values:**
- `Active` - Quantity ≥ 10 and not expired
- `Low Stock` - Quantity < 10
- `Out of Stock` - Quantity = 0
- `Expired` - Expiry date in the past

This function is called automatically on:
- `GET /api/inventory` (for each medicine)
- `GET /api/inventory/{id}`
- `POST /api/inventory` (before saving)
- `PUT /api/inventory/{id}`

### 2. Transactional Integrity

All write operations use database transactions to ensure atomicity:

```python
@router.post("", response_model=MedicineResponse, status_code=status.HTTP_201_CREATED)
def create_medicine(medicine: MedicineCreate, db: Session = Depends(get_db)):
    # 1. Validate uniqueness
    existing = db.query(Medicine).filter(Medicine.name == medicine.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Medicine already exists")
    
    # 2. Validate expiry date
    if medicine.expiry_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Expiry date cannot be in the past")
    
    # 3. Calculate status
    status_val = calculate_status(medicine.expiry_date, medicine.quantity)
    
    # 4. Create and commit
    db_medicine = Medicine(..., status=status_val)
    db.add(db_medicine)
    db.commit()      # Atomic commit
    db.refresh(db_medicine)
    return db_medicine
```

### 3. Stock Consistency on Sales

When recording a sale, the API ensures stock consistency:

```python
@router.post("/sales", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    # 1. Verify medicine exists
    medicine = db.query(Medicine).filter(Medicine.id == sale.medicine_id).first()
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")

    # 2. Check stock availability (prevent negative stock)
    if medicine.quantity < sale.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock available")

    # 3. Create sale record
    db_sale = Sale(...)
    db.add(db_sale)

    # 4. Reduce medicine stock atomically
    medicine.quantity -= sale.quantity
    
    # 5. Update status if stock level changed
    if medicine.quantity == 0:
        medicine.status = "Out of Stock"
    elif medicine.quantity < 10:
        medicine.status = "Low Stock"

    db.commit()  # Both sale and stock update committed together
    return db_sale
```

### 4. Purchase Order Stock Updates

When receiving a purchase order, stock is automatically increased:

```python
@router.patch("/purchase-orders/{po_id}/receive", response_model=PurchaseOrderResponse)
def receive_purchase_order(po_id: int, db: Session = Depends(get_db)):
    po = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
    if not po:
        raise HTTPException(status_code=404, detail="Purchase order not found")

    # Update medicine stock
    medicine = db.query(Medicine).filter(Medicine.id == po.medicine_id).first()
    if medicine:
        medicine.quantity += po.quantity
        # Auto-update status if stock is now sufficient
        if medicine.quantity >= 10:
            medicine.status = "Active"

    po.status = "Received"
    db.commit()
    return po
```

### 5. Input Validation with Pydantic

All request/response data is validated using Pydantic schemas:

```python
class MedicineBase(BaseModel):
    name: str              # Required string
    generic_name: str      # Required string
    category: str          # Required string
    batch_no: str          # Required string
    expiry_date: datetime  # Validated datetime
    quantity: int          # Validated integer
    cost_price: float      # Validated float
    mrp: float             # Validated float
    supplier: str          # Required string

class MedicineCreate(MedicineBase):
    pass  # Inherits all validation

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    # ... all fields optional for partial updates
```

### 6. Database Constraints

The SQLAlchemy models enforce data integrity at the database level:

```python
class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # UNIQUE constraint
    quantity = Column(Integer, default=0)           # Default value
    status = Column(String, default=MedicineStatus.ACTIVE.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

## Error Handling

The API returns consistent error responses:

| Status Code | Description |
|-------------|-------------|
| `200 OK` | Successful GET/PUT/PATCH request |
| `201 Created` | Successful POST request |
| `204 No Content` | Successful DELETE request |
| `400 Bad Request` | Validation error (duplicate name, insufficient stock, past expiry) |
| `404 Not Found` | Resource not found |
| `500 Internal Server Error` | Unexpected server error |

Error response format:
```json
{
  "detail": "Medicine 'Paracetamol 500mg' already exists"
}
```

---

## Running the API

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### API Documentation

Once running, access interactive documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Database

The API uses SQLite by default (`pharmacy.db`). To initialize:

```bash
python -c "from app.database import init_db; init_db()"
```

To seed sample data:
```bash
python seed_data.py
python add_sample_sales.py
```
