import axios from "axios";

// For Vercel deployment, use relative URL (works with vercel.json routes)
const api = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
