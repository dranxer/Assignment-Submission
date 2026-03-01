from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
import os

# Support multiple database URLs for different platforms
DATABASE_URL = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL", "sqlite:///./pharmacy.db")

# For Vercel serverless, use connection args only for SQLite
if "sqlite" in DATABASE_URL:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL (production, Vercel, etc.)
    engine = create_engine(DATABASE_URL)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MedicineStatus(str, enum.Enum):
    ACTIVE = "Active"
    LOW_STOCK = "Low Stock"
    EXPIRED = "Expired"
    OUT_OF_STOCK = "Out of Stock"


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    generic_name = Column(String)
    category = Column(String)
    batch_no = Column(String)
    expiry_date = Column(DateTime)
    quantity = Column(Integer, default=0)
    cost_price = Column(Float)
    mrp = Column(Float)
    supplier = Column(String)
    status = Column(String, default=MedicineStatus.ACTIVE.value)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, index=True)
    medicine_name = Column(String)
    quantity = Column(Integer)
    amount = Column(Float)
    sale_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"

    id = Column(Integer, primary_key=True, index=True)
    medicine_id = Column(Integer, index=True)
    medicine_name = Column(String)
    quantity = Column(Integer)
    cost = Column(Float)
    order_date = Column(DateTime, default=datetime.utcnow)
    expected_delivery = Column(DateTime)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    Base.metadata.create_all(bind=engine)
