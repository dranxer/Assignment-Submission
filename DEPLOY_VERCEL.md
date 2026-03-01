# Deploy Pharmacy CRM to Vercel (Full Stack)

## Overview

This guide deploys **both frontend and backend** on Vercel:
- **Frontend**: Vite React app (static files)
- **Backend**: FastAPI as Vercel Serverless Functions (Python)

---

## ⚡ Quick Deploy (5 minutes)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy
```bash
# From project root
vercel
```

Answer the questions:
- **Set up and deploy?** `Y`
- **Which scope?** (select your account)
- **Link to existing project?** `N`
- **Project name?** `pharmacy-crm`
- **Directory?** `./`
- **Override settings?** `N`

### Step 4: Production Deploy
```bash
vercel --prod
```

---

## 📁 Project Structure for Vercel

```
SwasthiQ/
├── vercel.json                 # Vercel configuration
├── backend/
│   ├── api/
│   │   └── index.py           # Serverless entry point
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── schemas.py
│   │   ├── routes_dashboard.py
│   │   ├── routes_inventory.py
│   │   └── routes_sales.py
│   └── requirements.txt
└── frontend/
    ├── src/
    ├── package.json
    └── vite.config.js
```

---

## 🔧 Configuration Files

### 1. `vercel.json` (Already created)

Defines build and routing rules:
- Frontend builds to static files
- Backend routes to Python serverless function
- All `/api/*` requests go to backend

### 2. `backend/api/index.py` (Already created)

Serverless entry point that imports all routes.

---

## 🗄️ Database Options

### Option 1: Vercel Postgres (Recommended)

1. Go to Vercel Dashboard → Storage → **Create Database**
2. Select **Postgres**
3. Connect to your project
4. Vercel auto-injects `POSTGRES_URL` env variable

Update `backend/app/database.py`:
```python
import os

DATABASE_URL = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL", "sqlite:///./pharmacy.db")
```

### Option 2: External Database (Neon, Supabase, Railway)

**Neon (Free Postgres):**
1. Go to https://neon.tech
2. Create free account
3. Create project → Get connection string
4. Add to Vercel env: `DATABASE_URL`

**Supabase (Free Postgres):**
1. Go to https://supabase.com
2. Create project
3. Get connection string (Settings → Database)
4. Add to Vercel env: `DATABASE_URL`

### Option 3: SQLite (Not Recommended for Production)

SQLite works locally but **won't persist** on Vercel (serverless is stateless).

Use only for testing!

---

## 🌍 Environment Variables

In Vercel Dashboard → Project → Settings → Environment Variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://...` | Production |
| `POSTGRES_URL` | (from Vercel Postgres) | Production |
| `CORS_ORIGINS` | `*` | All |

Add via CLI:
```bash
vercel env add DATABASE_URL
vercel env add POSTGRES_URL
```

---

## 🚀 Deploy Commands

### Local Testing
```bash
# Test Vercel build locally
vercel dev
```

Opens at: http://localhost:3000

### Deploy to Preview
```bash
vercel
```

### Deploy to Production
```bash
vercel --prod
```

---

## 📊 Vercel Dashboard Settings

After first deploy, configure in Vercel Dashboard:

### Build & Development Settings
```
Framework Preset: Vite
Root Directory: ./
Build Command: npm run build --prefix frontend
Output Directory: frontend/dist
Install Command: npm install
```

### Git Integration
```
✅ Connect Git Repository
✅ Auto-Deploy on push to main branch
```

### Environment Variables
```
DATABASE_URL = postgresql://user:pass@host:5432/db
POSTGRES_URL = (if using Vercel Postgres)
```

---

## 🧪 Test Deployment

### 1. Test Backend API
```bash
curl https://your-app.vercel.app/api/health
curl https://your-app.vercel.app/api/inventory
curl https://your-app.vercel.app/api/dashboard/summary
```

### 2. Test Frontend
Open: `https://your-app.vercel.app`

### 3. Test Full Integration
- Dashboard loads ✅
- Add medicine ✅
- Record sale ✅

---

## ⚠️ Important Notes

### Serverless Limitations

| Limitation | Impact | Solution |
|------------|--------|----------|
| **Cold starts** | First request slow (~5s) | Use Vercel Pro or keep-walive |
| **Max duration** | 10s (Hobby), 60s (Pro) | Optimize queries |
| **Stateless** | No file persistence | Use external DB |
| **Memory** | 1024 MB | Optimize imports |

### Database Migrations

On first deploy, run migrations:
```bash
# In Vercel Settings → Deploy Hooks
# Or manually via Vercel CLI:
vercel env pull
python -c "from app.database import init_db; init_db()"
```

### Cold Start Mitigation

Add `backend/api/warmup.py`:
```python
def handler(event, context):
    return {"statusCode": 200, "body": "Warm"}
```

Set up uptime monitoring (UptimeRobot) to ping every 5 min.

---

## 🔍 Troubleshooting

### Build Fails
```bash
# Check build logs
vercel logs

# Common issues:
# - Missing requirements.txt
# - Wrong Python version
# - Import errors
```

### API Returns 500
```bash
# Check function logs
vercel logs --follow

# Common issues:
# - Database connection failed
# - Missing environment variables
# - Import errors
```

### Frontend Shows but API Doesn't Work
- Check `vercel.json` routes
- Verify API calls use `/api/` prefix
- Check CORS settings

### Database Errors
- Ensure `DATABASE_URL` is set in Vercel env
- Use connection pooling for serverless
- Test connection locally first

---

## 💰 Vercel Pricing

### Hobby (Free)
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Serverless functions (10s timeout)
- ❌ No custom domains (only .vercel.app)
- ❌ No environment variables in preview

### Pro ($20/month)
- ✅ Everything in Hobby
- ✅ Custom domains
- ✅ 60s timeout
- ✅ More team features

---

## 📈 Monitoring

### Vercel Dashboard
- **Analytics**: Traffic, bandwidth
- **Functions**: Invocation count, errors
- **Deployments**: Build logs, status

### External Tools
- **Sentry**: Error tracking
- **UptimeRobot**: Uptime monitoring
- **Vercel Speed Insights**: Performance

---

## 🎯 Quick Commands Reference

```bash
# Login
vercel login

# Deploy preview
vercel

# Deploy production
vercel --prod

# View logs
vercel logs

# Follow logs (live)
vercel logs --follow

# List deployments
vercel ls

# Add environment variable
vercel env add DATABASE_URL

# Pull env locally
vercel env pull

# Open dashboard
vercel open
```

---

## ✅ Deployment Checklist

- [ ] Install Vercel CLI
- [ ] Login to Vercel
- [ ] Create `backend/api/index.py`
- [ ] Create `vercel.json`
- [ ] Set up database (Vercel Postgres or Neon)
- [ ] Add environment variables
- [ ] Deploy: `vercel --prod`
- [ ] Test API endpoints
- [ ] Test frontend
- [ ] Connect custom domain (optional)
- [ ] Enable auto-deploy from Git

---

## 🎉 You're Done!

Your full-stack Pharmacy CRM is now deployed on Vercel!

**URLs:**
- Frontend: `https://your-app.vercel.app`
- Backend API: `https://your-app.vercel.app/api`
- API Docs: `https://your-app.vercel.app/docs`

---

## 📚 Resources

- **Vercel Python Docs:** https://vercel.com/docs/runtimes/official-runtimes/python
- **Vercel Static Build:** https://vercel.com/docs/frameworks/vite
- **Vercel Environment Variables:** https://vercel.com/docs/environment-variables
- **Vercel Postgres:** https://vercel.com/docs/storage/vercel-postgres
