# Pharmacy CRM – SwasthiQ SDE Intern Assignment

A complete Pharmacy Management System with a FastAPI backend and React frontend, featuring real-time API integration, proper data validation, and a clean CRM-style UI.

## 📌 Overview

This project implements a simplified Pharmacy Module consisting of:

- **Dashboard Page** – Sales overview with key metrics
- **Inventory Page** – Full CRUD operations for medicine management

### Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | FastAPI (Python) |
| Frontend | React (Vite) |
| Database | SQLite (default) / PostgreSQL |
| API Client | Axios |
| Routing | React Router |
| Styling | Tailwind CSS |

## 🏗 Architecture

```
┌─────────────────┐
│  Frontend       │
│  (React + Vite) │
└────────┬────────┘
         │ REST APIs (JSON)
         ▼
┌─────────────────┐
│  Backend        │
│  (FastAPI)      │
└────────┬────────┘
         │ SQLAlchemy ORM
         ▼
┌─────────────────┐
│  Database       │
│  (SQLite/PG)    │
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Initialize database and seed sample data
python seed_data.py

# Start the server
uvicorn app.main:app --reload
```

Backend will run on: **http://localhost:8000**

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on: **http://localhost:5173**

## 📊 API Documentation

### Base URL
```
http://localhost:8000/api
```

### Dashboard APIs

#### 1. Get Dashboard Summary
```http
GET /api/dashboard/summary
```

**Response:**
```json
{
  "today_sales": 124580.00,
  "items_sold": 156,
  "low_stock_count": 12,
  "purchase_orders": 96250.00
}
```

| Field | Type | Description |
|-------|------|-------------|
| today_sales | float | Total revenue today |
| items_sold | int | Number of items sold today |
| low_stock_count | int | Items with quantity < 10 |
| purchase_orders | float | Total value of pending orders |

---

#### 2. Get Recent Sales
```http
GET /api/dashboard/recent-sales?limit=10
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| limit | int | 10 | Number of records (1-100) |

**Response:**
```json
[
  {
    "id": 1,
    "invoice": "INV-2024-0001",
    "amount": 2500.00
  },
  {
    "id": 2,
    "invoice": "INV-2024-0002",
    "amount": 1750.50
  }
]
```

---

### Inventory APIs

#### 1. List All Medicines
```http
GET /api/inventory?search=para&status=Active
```

**Query Parameters:**
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| search | string | "" | Search by name or category |
| status | string | "" | Filter by status |

**Response:**
```json
[
  {
    "id": 1,
    "name": "Paracetamol 500mg",
    "generic_name": "Paracetamol",
    "category": "Analgesic",
    "batch_no": "PAR-2024-001",
    "expiry_date": "2026-12-01T00:00:00",
    "quantity": 150,
    "cost_price": 2.50,
    "mrp": 5.00,
    "supplier": "MediCorp Pharmaceuticals",
    "status": "Active",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
]
```

---

#### 2. Get Medicine by ID
```http
GET /api/inventory/{id}
```

**Response:** Same as above (single object)

**Errors:**
- `404` – Medicine not found

---

#### 3. Create Medicine
```http
POST /api/inventory
Content-Type: application/json

{
  "name": "Paracetamol 500mg",
  "generic_name": "Paracetamol",
  "category": "Analgesic",
  "batch_no": "PAR-2024-001",
  "quantity": 50,
  "cost_price": 2.50,
  "mrp": 5.00,
  "expiry_date": "2026-12-01T00:00:00",
  "supplier": "MediCorp Pharmaceuticals"
}
```

**Required Fields:** name, generic_name, category, batch_no, quantity, mrp, expiry_date

**Response:** Created medicine object

**Errors:**
- `400` – Validation error (e.g., past expiry date)

---

#### 4. Update Medicine
```http
PUT /api/inventory/{id}
Content-Type: application/json

{
  "name": "Paracetamol 500mg (Updated)",
  "quantity": 100,
  "mrp": 5.50
}
```

**Response:** Updated medicine object

**Errors:**
- `404` – Medicine not found

---

#### 5. Update Medicine Status
```http
PATCH /api/inventory/{id}/status
Content-Type: application/json

{
  "status": "Out of Stock"
}
```

**Valid Status Values:** Active, Low Stock, Expired, Out of Stock

**Response:** Updated medicine object

**Errors:**
- `404` – Medicine not found

---

#### 6. Delete Medicine
```http
DELETE /api/inventory/{id}
```

**Response:** `204 No Content`

**Errors:**
- `404` – Medicine not found

---

#### 7. Get Inventory Summary
```http
GET /api/inventory/summary
```

**Response:**
```json
{
  "total_items": 150,
  "active_stock": 120,
  "low_stock": 18,
  "total_value": 45000.00
}
```

---

## 🔒 Data Consistency Strategy

### Status Auto-Calculation

The system automatically calculates medicine status based on:

| Condition | Status |
|-----------|--------|
| `expiry_date < today` | Expired |
| `quantity == 0` | Out of Stock |
| `quantity < 10` | Low Stock |
| `quantity >= 10` AND valid expiry | Active |

### Validation Rules

1. **Quantity Validation**: Must be non-negative integer
2. **Expiry Date**: Cannot be in the past
3. **Price Validation**: Must be non-negative floats
4. **Unique Name**: Medicine names must be unique

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK – Successful GET/PUT/PATCH |
| 201 | Created – Successful POST |
| 204 | No Content – Successful DELETE |
| 400 | Bad Request – Validation error |
| 404 | Not Found – Resource doesn't exist |

### Transaction Safety

All database operations use transactions to ensure:
- Atomicity (all-or-nothing updates)
- Consistency (database remains valid)
- Isolation (concurrent operations don't interfere)

## 🎨 Frontend Design Philosophy

### Component Architecture

```
src/
├── api/
│   └── axios.js          # API client configuration
├── components/
│   ├── Sidebar.jsx       # Navigation sidebar
│   ├── SummaryCard.jsx   # Dashboard metric cards
│   ├── StatusBadge.jsx   # Status indicator badges
│   ├── SalesList.jsx     # Recent sales list
│   ├── InventoryTable.jsx # Medicine table
│   └── MedicineForm.jsx  # Add medicine form
├── pages/
│   ├── Dashboard.jsx     # Dashboard page
│   └── Inventory.jsx     # Inventory management
├── App.jsx               # Main app with routing
├── main.jsx              # Entry point
└── styles.css            # Global styles
```

### UI Components

- **Summary Cards**: Display key metrics with icons
- **Status Badges**: Color-coded status indicators
- **Data Tables**: Sortable, filterable lists
- **Forms**: Validated input with error handling

### State Management

- React Hooks (`useState`, `useEffect`)
- Local component state for forms
- API data fetched on mount and refresh

### Error Handling

- Loading states with spinners
- Error messages with retry buttons
- Form validation with user feedback

## 📁 Project Structure

```
SwasthiQ/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── database.py          # DB models & connection
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── routes_dashboard.py  # Dashboard endpoints
│   │   └── routes_inventory.py  # Inventory endpoints
│   ├── seed_data.py             # Sample data seeder
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── api/axios.js         # API client
│   │   ├── components/          # Reusable UI components
│   │   ├── pages/               # Page components
│   │   ├── App.jsx              # Main app
│   │   ├── main.jsx             # Entry point
│   │   └── styles.css           # Styles
│   ├── package.json
│   └── README.md
└── README.md                    # This file
```

## 🌍 Deployment

### Quick Deploy Options

#### Option 1: Render (Recommended - Free)
1. Push code to GitHub
2. Go to https://render.com and create account
3. Click **New +** → **Blueprint**
4. Connect your GitHub repo
5. Render auto-deploys using `render.yaml`

**Live URLs:**
- Backend: `https://your-app.onrender.com`
- Frontend: `https://your-app-web.onrender.com`

#### Option 2: Docker Deployment
```bash
# Development (SQLite)
docker-compose up -d

# Production (PostgreSQL)
docker-compose -f docker-compose.prod.yml up -d
```

#### Option 3: Vercel (Frontend) + Render (Backend)
1. Deploy backend on Render (see Option 1)
2. Deploy frontend on Vercel:
   ```bash
   cd frontend
   npm run build
   # Connect to Vercel with VITE_API_URL env variable
   ```

### Environment Variables

**Backend (`.env`):**
```bash
DATABASE_URL=sqlite:///./pharmacy.db
# For production:
# DATABASE_URL=postgresql://user:pass@host:5432/dbname
CORS_ORIGINS=https://your-frontend.com
SECRET_KEY=your-secret-key
```

**Frontend (`.env.production`):**
```bash
VITE_API_URL=https://your-backend-api.com
```

### Pre-Deployment Checklist
- [ ] Update `DATABASE_URL` for production (PostgreSQL)
- [ ] Set `CORS_ORIGINS` to your frontend domain
- [ ] Generate a secure `SECRET_KEY`
- [ ] Test all API endpoints
- [ ] Build frontend for production

📖 **See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions**

## 🧪 Testing

### Backend

```bash
# Test API endpoints manually
curl http://localhost:8000/api/dashboard/summary

# Or use the interactive docs
# Open http://localhost:8000/docs
```

### Frontend

```bash
# Run development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📝 API Contract Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/summary` | GET | Get dashboard metrics |
| `/api/dashboard/recent-sales` | GET | Get recent sales |
| `/api/inventory` | GET | List medicines |
| `/api/inventory` | POST | Create medicine |
| `/api/inventory/{id}` | GET | Get medicine |
| `/api/inventory/{id}` | PUT | Update medicine |
| `/api/inventory/{id}/status` | PATCH | Update status |
| `/api/inventory/{id}` | DELETE | Delete medicine |
| `/api/inventory/summary` | GET | Inventory summary |

## ✅ Features Checklist

- [x] FastAPI backend with REST APIs
- [x] React frontend with Vite
- [x] Real API integration (no mocks)
- [x] Dashboard with sales metrics
- [x] Inventory CRUD operations
- [x] Search and filter functionality
- [x] Status auto-calculation
- [x] Data validation
- [x] Clean CRM-style UI
- [x] Responsive design
- [x] Error handling
- [x] Loading states
- [x] Comprehensive README

## 📄 License

This project is created for SwasthiQ SDE Intern Assignment.

---

**Built with ❤️ using FastAPI + React**
