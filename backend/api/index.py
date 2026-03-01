from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes_dashboard import router as dashboard_router
from app.routes_inventory import router as inventory_router
from app.routes_sales import router as sales_router
import os

# Initialize database
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


@app.get("/")
def read_root():
    return {"message": "Pharmacy CRM API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
