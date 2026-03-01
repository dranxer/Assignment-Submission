#!/bin/bash
# Quick Deployment Script for Pharmacy CRM

echo "🚀 Pharmacy CRM - Deployment Preparation"
echo "========================================"
echo ""

# Check if running on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "⚠️  Windows detected. Run deploy-windows.bat instead."
    exit 1
fi

# Step 1: Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Step 2: Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

# Step 3: Build frontend
echo "🔨 Building frontend..."
cd frontend
npm run build
cd ..

# Step 4: Initialize database
echo "💾 Initializing database..."
cd backend
python -c "from app.database import init_db; init_db()"
python seed_data.py
python add_sample_sales.py
cd ..

# Step 5: Show deployment options
echo ""
echo "✅ Build complete!"
echo ""
echo "📋 Deployment Options:"
echo ""
echo "  1. Docker (Local Testing):"
echo "     docker-compose up -d"
echo ""
echo "  2. Render (Free Cloud Hosting):"
echo "     - Push to GitHub"
echo "     - Deploy from https://render.com"
echo "     - Uses render.yaml automatically"
echo ""
echo "  3. Production (PostgreSQL):"
echo "     docker-compose -f docker-compose.prod.yml up -d"
echo ""
echo "📖 For detailed instructions, see DEPLOYMENT.md"
echo ""
