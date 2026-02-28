# Pharmacy CRM Frontend

React-based frontend for the Pharmacy Management System with Tailwind CSS styling.

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS** - Utility-first CSS framework

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

The app will be available at: http://localhost:5173

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── api/
│   └── axios.js          # API client configuration
├── components/
│   └── Sidebar.jsx       # Navigation sidebar
├── pages/
│   ├── Dashboard.jsx     # Dashboard with sales metrics
│   └── Inventory.jsx     # Inventory management
├── App.jsx               # Main app with routing
├── main.jsx              # Entry point
└── index.css             # Tailwind directives
```

## Tailwind Configuration

The project uses Tailwind CSS for styling with the following configuration:

```javascript
// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

## API Configuration

The API client is configured in `src/api/axios.js`:

```javascript
const api = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});
```

For production deployment, update the `baseURL` to your backend URL.

## Features

### Dashboard

- Today's sales overview with colored metric cards
- Items sold count
- Low stock alerts
- Purchase orders summary
- Recent sales list with invoice numbers
- "Make a Sale" section with patient ID and medicine search

### Inventory

- View all medicines in a clean table
- Add new medicines (via API)
- Update medicine details
- Mark as out of stock
- Delete medicines
- Search by name or category
- Filter by status (Active, Low Stock, Expired, Out of Stock)
- Real-time status badges

## Components

### Sidebar
Navigation component with links to Dashboard and Inventory pages.
Features active state highlighting and clean hover effects.

### Dashboard
- **Metric Cards**: Four colored cards showing key metrics with icons
- **Tabs**: Sales, Purchase, Inventory navigation
- **Make Sale Section**: Blue-tinted section for quick sales
- **Recent Sales**: List of recent transactions with status badges

### Inventory
- **Overview Cards**: Summary of total items, active stock, low stock, and total value
- **Filters**: Search input and status dropdown
- **Table**: Full inventory with sortable columns and action buttons
- **Status Badges**: Color-coded pills for each status type

## Styling

The application uses Tailwind CSS with:
- Soft gray background (`bg-[#f5f7fb]`)
- White rounded cards with shadows
- Colored metric cards (green, blue, orange, purple)
- Status pills (green for Active, yellow for Low Stock, red for Expired, gray for Out of Stock)
- Hover effects and transitions
- Responsive grid layouts

## Color Palette

| Color | Usage |
|-------|-------|
| `bg-blue-600` | Primary buttons, active states |
| `bg-green-100/text-green-600` | Active status, completed sales |
| `bg-yellow-100/text-yellow-600` | Low stock warnings |
| `bg-red-100/text-red-600` | Expired items, delete actions |
| `bg-gray-100/text-gray-600` | Out of stock, secondary text |
| `bg-slate-800` | Sidebar background |

## Environment Variables

Create a `.env` file for environment-specific configuration:

```
VITE_API_URL=http://localhost:8000/api
```

## License

SwasthiQ SDE Intern Assignment
