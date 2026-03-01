from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes_dashboard import router as dashboard_router
from app.routes_inventory import router as inventory_router
from app.routes_sales import router as sales_router
import os

app = FastAPI(title="Pharmacy CRM API", version="1.0.0")

# CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

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
