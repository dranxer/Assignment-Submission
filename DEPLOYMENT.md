# Deployment Guide - Pharmacy CRM

## Quick Deployment Options

### Option 1: Netlify + Render (Free - Recommended) ⭐
**Best for:** Production-ready free hosting, fast CDN

- **Frontend:** Netlify (Free, 100GB bandwidth)
- **Backend:** Render (Free PostgreSQL)

📖 **See [DEPLOY_NETLIFY.md](DEPLOY_NETLIFY.md) for step-by-step guide**

### Option 2: Render All-in-One (Free)
**Best for:** Simplest deployment, single platform

- Deploy both frontend & backend on Render using `render.yaml`

### Option 3: Vercel + Render (Free)
**Best for:** React-optimized hosting

- **Frontend:** Vercel (Free, optimized for React)
- **Backend:** Render (Free PostgreSQL)

### Option 4: Docker + VPS
**Best for:** Full control, production deployment

---

## Option 1: Deploy on Render (Easiest)

### Step 1: Prepare Backend for Render

1. **Create `render.yaml`** (already created for you)
2. **Update database** to use PostgreSQL (Render provides free PostgreSQL)
3. **Push code to GitHub**

### Step 2: Deploy

1. Go to https://render.com and sign up
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml` and deploy both frontend & backend

### Step 3: Get Your Live URL
- Backend: `https://your-app-name.onrender.com`
- Frontend: `https://your-app-name-web.onrender.com`

---

## Option 2: Deploy on Railway

### Backend Setup

1. Go to https://railway.app
2. Click **New Project** → **Deploy from GitHub**
3. Select your repository
4. Add PostgreSQL plugin:
   - Click **+ New** → **Database** → **PostgreSQL**
   - Railway auto-injects `DATABASE_URL` environment variable

### Frontend Setup

1. In same project, click **+ New** → **GitHub**
2. Select your repository
3. Set build command: `npm run build`
4. Set start command: `npm run preview`
5. Add environment variable: `VITE_API_URL` = your backend URL

---

## Option 3: Vercel (Frontend) + Render (Backend)

### Backend on Render

1. Follow Option 1 steps for backend only
2. Note your backend URL (e.g., `https://pharmacy-api.onrender.com`)

### Frontend on Vercel

1. Go to https://vercel.com
2. Click **Add New Project** → Import GitHub repo
3. Set environment variable:
   ```
   VITE_API_URL=https://pharmacy-api.onrender.com
   ```
4. Update `frontend/vite.config.js`:
   ```js
   server: {
     proxy: {
       '/api': {
         target: import.meta.env.VITE_API_URL || 'http://localhost:8000',
         changeOrigin: true,
       },
     },
   }
   ```
5. Deploy!

---

## Option 4: Docker Deployment (Advanced)

### Build Docker Images

```bash
# Backend
docker build -t pharmacy-backend ./backend

# Frontend
docker build -t pharmacy-frontend ./frontend
```

### Run with Docker Compose

```bash
docker-compose up -d
```

### Deploy to VPS (DigitalOcean, AWS EC2, etc.)

1. Install Docker on your VPS
2. Copy `docker-compose.yml` to server
3. Run `docker-compose up -d`
4. Set up nginx as reverse proxy
5. Add SSL with Let's Encrypt

---

## Pre-Deployment Checklist

### Backend
- [ ] Change `DATABASE_URL` to PostgreSQL (for production)
- [ ] Set `SECRET_KEY` environment variable
- [ ] Enable CORS for production domain
- [ ] Test all API endpoints

### Frontend
- [ ] Update API base URL to production backend
- [ ] Build for production (`npm run build`)
- [ ] Test production build locally

### Database
- [ ] Migrate from SQLite to PostgreSQL (for production)
- [ ] Run migrations
- [ ] Seed initial data

---

## Environment Variables

### Backend (`.env`)
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://your-frontend-domain.com
```

### Frontend (`.env.production`)
```env
VITE_API_URL=https://your-backend-api.com
```

---

## Post-Deployment Testing

1. **Health Check:**
   ```bash
   curl https://your-backend-url.com/health
   ```

2. **Test API:**
   ```bash
   curl https://your-backend-url.com/api/inventory
   curl https://your-backend-url.com/api/dashboard/summary
   ```

3. **Test Frontend:**
   - Open https://your-frontend-url.com
   - Verify dashboard loads
   - Test adding medicine
   - Test recording a sale

---

## Troubleshooting

### Frontend can't connect to backend
- Check CORS settings in `backend/app/main.py`
- Verify API URL in frontend environment variables

### Database errors
- Ensure `DATABASE_URL` is correctly set
- Run migrations: `python -c "from app.database import init_db; init_db()"`

### Build fails
- Check Node version (use Node 18+)
- Clear `node_modules` and reinstall: `npm ci`

---

## Need Help?

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **Vercel Docs:** https://vercel.com/docs
- **Docker Docs:** https://docs.docker.com
