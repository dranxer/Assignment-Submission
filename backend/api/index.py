import sys
import os

# Add backend folder to Python path for Vercel serverless
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.routes_dashboard import router as dashboard_router
from app.routes_inventory import router as inventory_router
from app.routes_sales import router as sales_router
from api.routes_admin import router as admin_router

# Initialize database tables (lazy - only on first request)
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"DB init error: {e}")

init_db()

app = FastAPI(title="Pharmacy CRM API", version="1.0.0")

# CORS - allow all origins for serverless
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard_router)
app.include_router(inventory_router)
app.include_router(sales_router)
app.include_router(admin_router)


@app.get("/")
def read_root():
    return {"message": "Pharmacy CRM API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    try:
        # Test database connection
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "healthy", "db": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
