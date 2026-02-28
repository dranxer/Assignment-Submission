import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <div className="w-64 bg-slate-800 text-white min-h-screen flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h3 className="text-lg font-semibold">💊 Pharmacy CRM</h3>
      </div>
      
      <nav className="flex-1 py-4">
        <Link
          to="/"
          className={`flex items-center gap-3 px-6 py-3 text-sm transition-colors border-l-4 ${
            isActive("/")
              ? "bg-slate-700 border-blue-500 text-white"
              : "border-transparent text-slate-400 hover:bg-slate-700 hover:text-white"
          }`}
        >
          <span>📊</span>
          Dashboard
        </Link>
        <Link
          to="/inventory"
          className={`flex items-center gap-3 px-6 py-3 text-sm transition-colors border-l-4 ${
            isActive("/inventory")
              ? "bg-slate-700 border-blue-500 text-white"
              : "border-transparent text-slate-400 hover:bg-slate-700 hover:text-white"
          }`}
        >
          <span>📦</span>
          Inventory
        </Link>
      </nav>

      <div className="p-4 border-t border-slate-700 text-center">
        <p className="text-sm font-medium">SwasthiQ</p>
        <p className="text-xs text-slate-500 mt-1">v1.0.0</p>
      </div>
    </div>
  );
}
