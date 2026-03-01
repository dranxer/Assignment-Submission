# Deploy Pharmacy CRM to Netlify + Render

## Overview

| Component | Platform | Why |
|-----------|----------|-----|
| **Frontend** | Netlify | Free, fast CDN, auto-deploy from Git |
| **Backend** | Render | Free PostgreSQL, auto-deploy from Git |

---

## Step 1: Deploy Backend on Render

### 1.1 Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/pharmacy-crm.git
git push -u origin main
```

### 1.2 Deploy on Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click **New +** → **Blueprint**
4. Click **Connect a repository**
5. Select your `pharmacy-crm` repo
6. Render will detect `render.yaml` and show:
   - **pharmacy-backend** (Web Service)
   - **pharmacy-db** (PostgreSQL Database)
7. Click **Apply**

### 1.3 Wait for Deployment
- Backend will deploy at: `https://pharmacy-crm-xxxx.onrender.com`
- Database connection is automatic
- Health check at `/health`

### 1.4 Copy Backend URL
After deployment, copy your backend URL (e.g., `https://pharmacy-crm-xxxx.onrender.com`)

---

## Step 2: Deploy Frontend on Netlify

### Option A: Netlify CLI (Recommended)

#### 2.1 Install Netlify CLI
```bash
npm install -g netlify-cli
```

#### 2.2 Login to Netlify
```bash
netlify login
```

#### 2.3 Create `netlify.toml` in frontend folder
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/api/*"
  to = "https://pharmacy-crm-xxxx.onrender.com/api/:splat"
  status = 200
  headers = { X-From = "Netlify" }
```

#### 2.4 Deploy
```bash
cd frontend
netlify init
netlify deploy --prod
```

### Option B: Netlify UI (Alternative)

#### 2.1 Build Locally
```bash
cd frontend
npm install
npm run build
```

#### 2.2 Drag & Drop
1. Go to https://app.netlify.com/drop
2. Drag the `frontend/dist` folder
3. Site is deployed instantly!

#### 2.3 Configure Build Settings
In Netlify Dashboard:
- **Build command**: `npm run build`
- **Publish directory**: `dist`

#### 2.4 Add Redirects
Create `frontend/public/_redirects`:
```
/api/*  https://pharmacy-crm-xxxx.onrender.com/api/:splat  200
```

---

## Step 3: Update Environment Variables

### Frontend (Netlify)

In Netlify Dashboard → Site Settings → Environment Variables:

```
VITE_API_URL=https://pharmacy-crm-xxxx.onrender.com
```

Or create `.env.production` in frontend folder:
```env
VITE_API_URL=https://pharmacy-crm-xxxx.onrender.com
```

### Backend (Render)

In Render Dashboard → Environment:

```
CORS_ORIGINS=https://your-site.netlify.app,http://localhost:5173
DATABASE_URL=(auto-set from database)
```

---

## Step 4: Test Deployment

### 1. Test Backend
```bash
curl https://pharmacy-crm-xxxx.onrender.com/health
curl https://pharmacy-crm-xxxx.onrender.com/api/inventory
```

### 2. Test Frontend
Open your Netlify URL (e.g., `https://pharmacy-crm-xxxx.netlify.app`)

### 3. Test Full Integration
- Dashboard should load with real data
- Add medicine → should save to backend
- Record sale → should update inventory

---

## Alternative: Netlify Functions (Backend on Netlify Too)

If you want **everything on Netlify**:

### Create `frontend/netlify/functions/api.js`
```javascript
const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  const path = event.path.replace('/.netlify/functions/api', '/api');
  const backendUrl = 'https://pharmacy-crm-xxxx.onrender.com';
  
  const response = await fetch(`${backendUrl}${path}`, {
    method: event.httpMethod,
    headers: event.headers,
    body: event.body,
  });
  
  return {
    statusCode: response.status,
    body: await response.text(),
  };
};
```

### Update `netlify.toml`
```toml
[build]
  command = "npm run build"
  publish = "dist"

[functions]
  directory = "netlify/functions"

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/api/:splat"
  status = 200
```

---

## Netlify vs Vercel

| Feature | Netlify | Vercel |
|---------|---------|--------|
| **Free Tier** | ✅ Generous | ✅ Generous |
| **CDN** | ✅ Global | ✅ Global |
| **Functions** | ✅ Netlify Functions | ✅ Serverless Functions |
| **Redirects** | ✅ Easy config | ✅ Easy config |
| **Preview Deploys** | ✅ Every branch | ✅ Every branch |
| **Form Handling** | ✅ Built-in | ❌ Third-party |
| **Best For** | Static sites + JAMstack | Next.js apps |

**Verdict:** Both work great! Netlify has better free tier for static sites.

---

## Troubleshooting

### CORS Errors
**Backend (Render):**
```
CORS_ORIGINS=https://your-site.netlify.app
```

### API Calls Failing
**Check redirects in `netlify.toml`:**
```toml
[[redirects]]
  from = "/api/*"
  to = "https://your-backend.onrender.com/api/:splat"
  status = 200
```

### Build Fails
**Netlify build logs:**
```bash
netlify logs
```

**Common fixes:**
- Node version: Add `.nvmrc` with `18`
- Clear cache: `netlify deploy --prod --clearCache`

---

## Cost Breakdown

| Service | Plan | Cost |
|---------|------|------|
| **Netlify** | Free | $0/month |
| **Render** | Free | $0/month |
| **Total** | | **$0/month** 🎉 |

### Render Free Tier Limits
- Web service: 750 hours/month (free tier sleeps after 15 min inactivity)
- Database: 1 GB storage
- Bandwidth: Unlimited

### Netlify Free Tier Limits
- Bandwidth: 100 GB/month
- Build minutes: 300 minutes/month
- Sites: Unlimited

---

## Quick Commands

```bash
# Deploy to Netlify
cd frontend
netlify deploy --prod

# Check deployment status
netlify status

# Open site in browser
netlify open

# View logs
netlify logs

# Redeploy
netlify deploy --prod --dir=dist
```

---

## Final URLs

After deployment:
- **Frontend:** `https://pharmacy-crm.netlify.app`
- **Backend:** `https://pharmacy-crm.onrender.com`
- **API Docs:** `https://pharmacy-crm.onrender.com/docs`

🎉 **Your Pharmacy CRM is live!**
