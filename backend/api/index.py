import sys
import os

# Add backend folder to Python path for Vercel serverless
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes_dashboard import router as dashboard_router
from app.routes_inventory import router as inventory_router
from app.routes_sales import router as sales_router

# Initialize database tables
Base.metadata.create_all(bind=engine)

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


@app.get("/")
def read_root():
    return {"message": "Pharmacy CRM API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
