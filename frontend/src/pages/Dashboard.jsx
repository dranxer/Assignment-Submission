import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [sales, setSales] = useState([]);
  const [inventorySummary, setInventorySummary] = useState(null);
  const [inventoryData, setInventoryData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("sales");
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [editingMedicine, setEditingMedicine] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    generic_name: "",
    category: "",
    batch_no: "",
    expiry_date: "",
    quantity: 0,
    cost_price: 0,
    mrp: 0,
    supplier: "",
  });

  const fetchMedicines = async () => {
    try {
      const params = {};
      if (searchTerm) params.search = searchTerm;
      if (statusFilter) params.status = statusFilter;
      const res = await api.get("/inventory", { params });
      setInventoryData(res.data);
    } catch (err) {
      console.error("Error fetching medicines:", err);
    }
  };

  useEffect(() => {
    Promise.all([
      api.get("/dashboard/summary"),
      api.get("/dashboard/recent-sales"),
      api.get("/inventory/summary"),
    ])
      .then(([summaryRes, salesRes, inventoryRes]) => {
        setSummary(summaryRes.data);
        setSales(salesRes.data);
        setInventorySummary(inventoryRes.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
    fetchMedicines();
  }, []);

  const handleDelete = async (id, name) => {
    if (window.confirm(`Delete "${name}"?`)) {
      try {
        await api.delete(`/inventory/${id}`);
        fetchMedicines();
      } catch (err) {
        alert("Failed to delete");
      }
    }
  };

  const handleEdit = (med) => {
    setEditingMedicine(med);
    setFormData({
      name: med.name,
      generic_name: med.generic_name,
      category: med.category,
      batch_no: med.batch_no,
      expiry_date: new Date(med.expiry_date).toISOString().split('T')[0],
      quantity: med.quantity,
      cost_price: med.cost_price,
      mrp: med.mrp,
      supplier: med.supplier,
    });
    setShowModal(true);
  };

  const handleAddNew = () => {
    setEditingMedicine(null);
    setFormData({
      name: "",
      generic_name: "",
      category: "",
      batch_no: "",
      expiry_date: "",
      quantity: 0,
      cost_price: 0,
      mrp: 0,
      supplier: "",
    });
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        ...formData,
        expiry_date: new Date(formData.expiry_date).toISOString(),
        quantity: parseInt(formData.quantity),
        cost_price: parseFloat(formData.cost_price),
        mrp: parseFloat(formData.mrp),
      };
      if (editingMedicine) {
        await api.put(`/inventory/${editingMedicine.id}`, payload);
      } else {
        await api.post("/inventory", payload);
      }
      setShowModal(false);
      fetchMedicines();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to save medicine");
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#e5e7eb] flex items-center justify-center p-8">
        <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
          <div className="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-500 font-medium">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="min-h-screen bg-[#e5e7eb] flex items-center justify-center p-8">
        <div className="bg-white rounded-2xl shadow-xl p-12 text-center">
          <p className="text-red-500 mb-4 font-medium">Failed to load dashboard</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#e5e7eb] flex items-start justify-center p-8">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-[980px] p-8">

        {/* HEADER */}
        <div className="flex justify-between items-start mb-7">
          <div>
            <h1 className="text-[22px] font-bold text-[#111827] tracking-tight">Pharmacy CRM</h1>
            <p className="text-[13px] text-[#9ca3af] mt-1">Manage inventory, sales, and purchase orders</p>
          </div>
          <div className="flex gap-2.5">
            <button className="flex items-center gap-1.5 border border-[#d1d5db] bg-white text-[#374151] text-[13px] font-medium px-4 py-2 rounded-lg hover:bg-gray-50">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#374151" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              Export
            </button>
            <button onClick={handleAddNew} className="flex items-center gap-1.5 bg-[#2563eb] text-white text-[13px] font-medium px-4 py-2 rounded-lg border-none hover:bg-blue-700">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round">
                <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Add Medicine
            </button>
          </div>
        </div>

        {/* STAT CARDS */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          {/* Today's Sales */}
          <div className="bg-white border border-[#f3f4f6] rounded-[14px] p-[18px] shadow-[0_1px_4px_rgba(0,0,0,0.05)]">
            <div className="flex items-center justify-between mb-3.5">
              <div className="w-[42px] h-[42px] bg-[#16a34a] rounded-[10px] flex items-center justify-center">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="12" y1="1" x2="12" y2="23"/>
                  <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                </svg>
              </div>
              <span className="bg-[#f0fdf4] text-[#16a34a] text-[11.5px] font-medium px-2.5 py-1 rounded-[20px] flex items-center gap-1">
                <svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="#16a34a" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="18 15 12 9 6 15"/>
                </svg>
                +12.5%
              </span>
            </div>
            <div className="text-[26px] font-bold text-[#111827] tracking-tighter">₹{summary.today_sales?.toFixed(2) || '0.00'}</div>
            <div className="text-[12.5px] text-[#9ca3af]">Today's Sales</div>
          </div>

          {/* Items Sold */}
          <div className="bg-white border border-[#f3f4f6] rounded-[14px] p-[18px] shadow-[0_1px_4px_rgba(0,0,0,0.05)]">
            <div className="flex items-center justify-between mb-3.5">
              <div className="w-[42px] h-[42px] bg-[#2563eb] rounded-[10px] flex items-center justify-center">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
                  <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
                </svg>
              </div>
              <span className="bg-[#eff6ff] text-[#2563eb] text-[11.5px] font-medium px-2.5 py-1 rounded-[20px]">32 Orders</span>
            </div>
            <div className="text-[26px] font-bold text-[#111827] tracking-tighter">{summary.items_sold || 0}</div>
            <div className="text-[12.5px] text-[#9ca3af]">Items Sold Today</div>
          </div>

          {/* Low Stock */}
          <div className="bg-white border border-[#f3f4f6] rounded-[14px] p-[18px] shadow-[0_1px_4px_rgba(0,0,0,0.05)]">
            <div className="flex items-center justify-between mb-3.5">
              <div className="w-[42px] h-[42px] bg-[#f97316] rounded-[10px] flex items-center justify-center">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                  <line x1="12" y1="9" x2="12" y2="13"/>
                  <line x1="12" y1="17" x2="12.01" y2="17"/>
                </svg>
              </div>
              <span className="bg-[#fff7ed] text-[#ea580c] text-[11.5px] font-medium px-2.5 py-1 rounded-[20px]">Action Needed</span>
            </div>
            <div className="text-[26px] font-bold text-[#111827] tracking-tighter">{summary.low_stock_count || 0}</div>
            <div className="text-[12.5px] text-[#9ca3af]">Low Stock Items</div>
          </div>

          {/* Purchase Orders */}
          <div className="bg-white border border-[#f3f4f6] rounded-[14px] p-[18px] shadow-[0_1px_4px_rgba(0,0,0,0.05)]">
            <div className="flex items-center justify-between mb-3.5">
              <div className="w-[42px] h-[42px] bg-[#9333ea] rounded-[10px] flex items-center justify-center">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/>
                  <polyline points="3.27 6.96 12 12.01 20.73 6.96"/>
                  <line x1="12" y1="22.08" x2="12" y2="12"/>
                </svg>
              </div>
              <span className="bg-[#faf5ff] text-[#9333ea] text-[11.5px] font-medium px-2.5 py-1 rounded-[20px]">5 Pending</span>
            </div>
            <div className="text-[26px] font-bold text-[#111827] tracking-tighter">₹{summary.purchase_orders?.toFixed(2) || '0.00'}</div>
            <div className="text-[12.5px] text-[#9ca3af]">Purchase Orders</div>
          </div>
        </div>

        {/* PANEL WITH TABS */}
        <div className="bg-white border border-[#f3f4f6] rounded-[14px] shadow-[0_1px_4px_rgba(0,0,0,0.04)] overflow-hidden">
          
          {/* TABS BAR */}
          <div className="flex items-center justify-between px-5 py-0 border-b border-[#f3f4f6]">
            <div className="flex">
              <button
                onClick={() => setActiveTab("sales")}
                className={`flex items-center gap-1.5 text-[13px] font-medium px-4 py-3.5 border-b-2 transition-colors ${
                  activeTab === "sales" 
                    ? "text-[#111827] border-[#2563eb] font-semibold" 
                    : "text-[#6b7280] border-transparent hover:text-[#374151]"
                }`}
              >
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
                  <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
                </svg>
                Sales
              </button>
              <button
                onClick={() => setActiveTab("purchase")}
                className={`flex items-center gap-1.5 text-[13px] font-medium px-4 py-3.5 border-b-2 transition-colors ${
                  activeTab === "purchase" 
                    ? "text-[#111827] border-[#2563eb] font-semibold" 
                    : "text-[#6b7280] border-transparent hover:text-[#374151]"
                }`}
              >
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                  <line x1="3" y1="6" x2="21" y2="6"/>
                  <path d="M16 10a4 4 0 0 1-8 0"/>
                </svg>
                Purchase
              </button>
              <button
                onClick={() => setActiveTab("inventory")}
                className={`flex items-center gap-1.5 text-[13px] font-medium px-4 py-3.5 border-b-2 transition-colors ${
                  activeTab === "inventory" 
                    ? "text-[#111827] border-[#2563eb] font-semibold" 
                    : "text-[#6b7280] border-transparent hover:text-[#374151]"
                }`}
              >
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="2" y="7" width="20" height="14" rx="2"/>
                  <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>
                </svg>
                Inventory
              </button>
            </div>
            <div className="flex gap-2">
              <button className="flex items-center gap-1 bg-[#2563eb] text-white text-[12.5px] font-medium px-3.5 py-1.5 rounded-[7px] border-none">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round">
                  <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                New Sale
              </button>
              <button className="flex items-center gap-1 bg-white text-[#374151] text-[12.5px] font-medium px-3.5 py-1.5 rounded-[7px] border border-[#e5e7eb]">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#374151" strokeWidth="2.5" strokeLinecap="round">
                  <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                </svg>
                New Purchase
              </button>
            </div>
          </div>

          {/* SALES PANE */}
          {activeTab === "sales" && (
            <div className="p-5 pb-2">
              {/* Make a Sale */}
              <div className="bg-gradient-to-br from-[#eff6ff] to-[#f0fdf4] rounded-[12px] p-[18px_20px_16px] mb-6">
                <h3 className="text-[14.5px] font-semibold text-[#111827] mb-1">Make a Sale</h3>
                <p className="text-[12.5px] text-[#9ca3af] mb-3.5">Select medicines from inventory</p>
                <div className="flex gap-2 items-center">
                  <input 
                    className="h-[38px] border border-[#e5e7eb] rounded-[8px] px-3.5 text-[13px] text-[#374151] bg-white outline-none w-[155px]" 
                    placeholder="Patient Id" 
                  />
                  <div className="relative flex-1">
                    <svg className="absolute left-2.5 top-1/2 -translate-y-1/2" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
                    </svg>
                    <input 
                      className="w-full h-[38px] border border-[#e5e7eb] rounded-[8px] pl-8 pr-3.5 text-[13px] bg-white outline-none" 
                      placeholder="Search medicines..." 
                    />
                  </div>
                  <button className="h-[38px] px-5 bg-[#2563eb] text-white text-[13px] font-semibold border-none rounded-[8px]">Enter</button>
                  <button className="h-[38px] px-7 bg-[#dc2626] text-white text-[13px] font-semibold border-none rounded-[8px] ml-1.5">Bill</button>
                </div>
              </div>

              {/* Recent Sales */}
              <h3 className="text-[15px] font-bold text-[#111827] mb-3">Recent Sales</h3>
              
              {sales.length === 0 ? (
                <div className="text-center py-10 text-[#9ca3af]">No recent sales</div>
              ) : (
                sales.map((sale) => (
                  <div key={sale.id} className="flex items-center justify-between py-3.5 border-b border-[#f9fafb] last:border-b-0 last:pb-1.5">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-[#16a34a] rounded-[10px] flex items-center justify-center flex-shrink-0">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                          <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
                          <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
                        </svg>
                      </div>
                      <div>
                        <div className="text-[13.5px] font-semibold text-[#111827]">{sale.invoice}</div>
                        <div className="text-[12px] text-[#9ca3af] mt-0.5">Customer Walk-in &bull; 1 items &bull; Cash</div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3.5">
                      <span className="text-[14px] font-bold text-[#111827]">₹{sale.amount?.toFixed(2)}</span>
                      <span className="text-[12px] text-[#9ca3af]">{new Date().toISOString().split('T')[0]}</span>
                      <span className="bg-[#f0fdf4] text-[#16a34a] text-[11.5px] font-medium px-3 py-1 rounded-[20px] border border-[#bbf7d0]">Completed</span>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* PURCHASE PANE */}
          {activeTab === "purchase" && (
            <div className="p-5 pb-2">
              <div className="text-center py-[60px] text-[#9ca3af]">
                <svg className="mx-auto mb-4" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/>
                  <line x1="3" y1="6" x2="21" y2="6"/>
                  <path d="M16 10a4 4 0 0 1-8 0"/>
                </svg>
                <p className="text-[14px]">No purchase orders yet. Click <strong>New Purchase</strong> to create one.</p>
              </div>
            </div>
          )}

          {/* INVENTORY PANE */}
          {activeTab === "inventory" && (
            <div className="p-5 pb-2">
              {/* Inventory Overview */}
              <div className="bg-gradient-to-br from-[#eff6ff] to-[#f0fdf4] rounded-[12px] p-[18px_22px_20px] mb-6">
                <h3 className="text-[14px] font-semibold text-[#111827] mb-[18px]">Inventory Overview</h3>
                <div className="grid grid-cols-4">
                  <div>
                    <div className="flex items-center gap-1 text-[11.5px] text-[#9ca3af] mb-1.5">
                      Total Items
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#2563eb" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
                      </svg>
                    </div>
                    <div className="text-[26px] font-bold text-[#111827] tracking-tighter">{inventorySummary?.total_items || 0}</div>
                  </div>
                  <div>
                    <div className="flex items-center gap-1 text-[11.5px] text-[#9ca3af] mb-1.5">
                      Active Stock
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#16a34a" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                        <polyline points="20 6 9 17 4 12"/>
                      </svg>
                    </div>
                    <div className="text-[26px] font-bold text-[#111827] tracking-tighter">{inventorySummary?.active_stock || 0}</div>
                  </div>
                  <div>
                    <div className="flex items-center gap-1 text-[11.5px] text-[#9ca3af] mb-1.5">
                      Low Stock
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#f97316" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                        <line x1="12" y1="9" x2="12" y2="13"/>
                        <line x1="12" y1="17" x2="12.01" y2="17"/>
                      </svg>
                    </div>
                    <div className="text-[26px] font-bold text-[#111827] tracking-tighter">{inventorySummary?.low_stock || 0}</div>
                  </div>
                  <div>
                    <div className="flex items-center gap-1 text-[11.5px] text-[#9ca3af] mb-1.5">
                      Total Value
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9333ea" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                        <line x1="12" y1="1" x2="12" y2="23"/>
                        <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
                      </svg>
                    </div>
                    <div className="text-[26px] font-bold text-[#111827] tracking-tighter">₹{inventorySummary?.total_value?.toFixed(2) || '0.00'}</div>
                  </div>
                </div>
              </div>

              {/* Section Header */}
              <div className="flex justify-between items-center mb-3.5">
                <h3 className="text-[15px] font-bold text-[#111827]">Complete Inventory</h3>
                <div className="flex gap-2">
                  <button className="flex items-center gap-1.5 text-[12.5px] font-medium text-[#374151] border border-[#e5e7eb] bg-white px-3.5 py-1.5 rounded-[7px]">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#374151" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
                    </svg>
                    Filter
                  </button>
                  <button className="flex items-center gap-1.5 text-[12.5px] font-medium text-[#374151] border border-[#e5e7eb] bg-white px-3.5 py-1.5 rounded-[7px]">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#374151" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                      <polyline points="7 10 12 15 17 10"/>
                      <line x1="12" y1="15" x2="12" y2="3"/>
                    </svg>
                    Export
                  </button>
                </div>
              </div>

              {/* Inventory Table Placeholder */}
              <div className="flex gap-2 mb-4">
                <input
                  type="text"
                  placeholder="Search medicines..."
                  value={searchTerm}
                  onChange={(e) => { setSearchTerm(e.target.value); fetchMedicines(); }}
                  className="flex-1 h-[38px] border border-[#e5e7eb] rounded-[8px] px-3.5 text-[13px] bg-white outline-none"
                />
                <select
                  value={statusFilter}
                  onChange={(e) => { setStatusFilter(e.target.value); fetchMedicines(); }}
                  className="h-[38px] border border-[#e5e7eb] rounded-[8px] px-3.5 text-[13px] bg-white outline-none"
                >
                  <option value="">All Status</option>
                  <option value="Active">Active</option>
                  <option value="Low Stock">Low Stock</option>
                  <option value="Expired">Expired</option>
                  <option value="Out of Stock">Out of Stock</option>
                </select>
                <button onClick={fetchMedicines} className="h-[38px] px-4 bg-[#2563eb] text-white text-[13px] font-semibold rounded-[8px] border-none">
                  Refresh
                </button>
              </div>

              {inventoryData.length === 0 ? (
                <div className="text-center py-10 text-[#9ca3af]">
                  <p>No medicines found</p>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-sm border-collapse">
                    <thead>
                      <tr className="border-b-[1.5px] border-[#f3f4f6]">
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Medicine Name</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Generic Name</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Category</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Batch No</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Expiry Date</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Quantity</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Cost Price</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">MRP</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Supplier</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Status</th>
                        <th className="text-left text-[10.5px] font-bold text-[#9ca3af] tracking-wider uppercase py-2 px-3">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {inventoryData.map((med) => (
                        <tr key={med.id} className="border-b border-[#f9fafb] last:border-b-0">
                          <td className="py-3.5 px-3 text-[13px] font-medium text-[#111827]">{med.name}</td>
                          <td className="py-3.5 px-3 text-[13px] text-[#374151]">{med.generic_name}</td>
                          <td className="py-3.5 px-3 text-[13px] text-[#374151]">{med.category}</td>
                          <td className="py-3.5 px-3 text-[13px] text-[#374151] font-mono text-xs">{med.batch_no}</td>
                          <td className="py-3.5 px-3 text-[13px] text-[#374151]">{new Date(med.expiry_date).toLocaleDateString()}</td>
                          <td className="py-3.5 px-3">
                            <span className={med.quantity < 10 ? "text-[#f97316] font-semibold" : "text-[#374151]"}>
                              {med.quantity}
                            </span>
                          </td>
                          <td className="py-3.5 px-3 text-[13px] text-[#374151]">₹{med.cost_price?.toFixed(2)}</td>
                          <td className="py-3.5 px-3 text-[13px] text-[#374151] font-medium">₹{med.mrp?.toFixed(2)}</td>
                          <td className="py-3.5 px-3 text-[13px] text-[#374151] text-xs">{med.supplier}</td>
                          <td className="py-3.5 px-3">
                            <StatusBadge status={med.status} />
                          </td>
                          <td className="py-3.5 px-3">
                            <div className="flex gap-1.5">
                              <button
                                onClick={() => handleEdit(med)}
                                className="px-2 py-1 text-xs bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                              >
                                ✏️
                              </button>
                              <button
                                onClick={() => handleDelete(med.id, med.name)}
                                className="px-2 py-1 text-xs bg-red-100 text-red-700 rounded hover:bg-red-200"
                              >
                                🗑
                              </button>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>

        {/* ADD/EDIT MEDICINE MODAL */}
        {showModal && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold text-gray-800">
                  {editingMedicine ? "Edit Medicine" : "Add New Medicine"}
                </h2>
              </div>

              <form onSubmit={handleSubmit} className="p-6">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Medicine Name *</label>
                    <input
                      type="text"
                      name="name"
                      value={formData.name}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                      placeholder="e.g., Paracetamol 500mg"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Generic Name *</label>
                    <input
                      type="text"
                      name="generic_name"
                      value={formData.generic_name}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                      placeholder="e.g., Acetaminophen"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Category *</label>
                    <input
                      type="text"
                      name="category"
                      value={formData.category}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                      placeholder="e.g., Analgesic"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Batch No *</label>
                    <input
                      type="text"
                      name="batch_no"
                      value={formData.batch_no}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                      placeholder="e.g., PAR-2024-001"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Expiry Date *</label>
                    <input
                      type="date"
                      name="expiry_date"
                      value={formData.expiry_date}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Quantity *</label>
                    <input
                      type="number"
                      name="quantity"
                      value={formData.quantity}
                      onChange={handleInputChange}
                      required
                      min="0"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Cost Price *</label>
                    <input
                      type="number"
                      name="cost_price"
                      value={formData.cost_price}
                      onChange={handleInputChange}
                      required
                      min="0"
                      step="0.01"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">MRP *</label>
                    <input
                      type="number"
                      name="mrp"
                      value={formData.mrp}
                      onChange={handleInputChange}
                      required
                      min="0"
                      step="0.01"
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">Supplier *</label>
                    <input
                      type="text"
                      name="supplier"
                      value={formData.supplier}
                      onChange={handleInputChange}
                      required
                      className="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-400 outline-none"
                      placeholder="e.g., MediCorp Pharmaceuticals"
                    />
                  </div>
                </div>

                <div className="flex gap-3 mt-6 pt-4 border-t">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    {editingMedicine ? "Update Medicine" : "Add Medicine"}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function StatusBadge({ status }) {
  const styles = {
    Active: "bg-[#f0fdf4] text-[#16a34a] border border-[#bbf7d0]",
    "Low Stock": "bg-[#fefce8] text-[#ca8a04] border border-[#fde68a]",
    Expired: "bg-[#fff1f2] text-[#e11d48] border border-[#fecdd3]",
    "Out of Stock": "bg-[#f9fafb] text-[#6b7280] border border-[#e5e7eb]",
  };

  return (
    <span className={`text-[11.5px] font-medium px-[11px] py-1 rounded-[20px] inline-block whitespace-nowrap ${styles[status] || styles["Out of Stock"]}`}>
      {status}
    </span>
  );
}
