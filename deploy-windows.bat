@echo off
REM Quick Deployment Script for Pharmacy CRM (Windows)

echo.
echo ========================================
echo  Pharmacy CRM - Deployment Preparation
echo ========================================
echo.

REM Step 1: Install backend dependencies
echo [1/5] Installing backend dependencies...
cd backend
pip install -r requirements.txt
cd ..

REM Step 2: Install frontend dependencies
echo [2/5] Installing frontend dependencies...
cd frontend
call npm install
cd ..

REM Step 3: Build frontend
echo [3/5] Building frontend...
cd frontend
call npm run build
cd ..

REM Step 4: Initialize database
echo [4/5] Initializing database...
cd backend
python -c "from app.database import init_db; init_db()"
python seed_data.py
python add_sample_sales.py
cd ..

REM Step 5: Show deployment options
echo.
echo [5/5] Build complete!
echo.
echo ========================================
echo  Deployment Options:
echo ========================================
echo.
echo  1. Docker (Local Testing):
echo     docker-compose up -d
echo.
echo  2. Render (Free Cloud Hosting):
echo     - Push to GitHub
echo     - Deploy from https://render.com
echo     - Uses render.yaml automatically
echo.
echo  3. Production (PostgreSQL):
echo     docker-compose -f docker-compose.prod.yml up -d
echo.
echo  For detailed instructions, see DEPLOYMENT.md
echo.
pause
