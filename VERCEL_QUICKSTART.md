# 🚀 Deploy to Vercel - Quick Start

## Files Already Created ✅

- `vercel.json` - Vercel configuration
- `backend/api/index.py` - Serverless backend entry point
- `backend/app/database.py` - Updated for PostgreSQL support
- `DEPLOY_VERCEL.md` - Complete deployment guide

---

## Deploy in 3 Steps (5 minutes)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login
```bash
vercel login
```
Opens browser → Login with GitHub

### Step 3: Deploy
```bash
# From project root
vercel --prod
```

**That's it!** Your app will be live at `https://your-project.vercel.app`

---

## ⚙️ Vercel Dashboard Settings

After first deploy, go to **Vercel Dashboard → Your Project → Settings**:

### Build Settings

| Setting | Value |
|---------|-------|
| **Framework Preset** | `Vite` |
| **Root Directory** | `./` |
| **Build Command** | `npm run build --prefix frontend` |
| **Output Directory** | `frontend/dist` |
| **Install Command** | `npm install` |

### Environment Variables

Add these in **Settings → Environment Variables**:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` |

**To get a free PostgreSQL database:**
1. Go to https://vercel.com/storage/postgres
2. Create database
3. Copy connection string
4. Add to Vercel env as `DATABASE_URL`

---

## Test Your Deployment

```bash
# Get your Vercel URL from deployment output
# Example: https://pharmacy-crm.vercel.app

# Test health
curl https://your-app.vercel.app/health

# Test API
curl https://your-app.vercel.app/api/inventory

# Test frontend
# Open in browser: https://your-app.vercel.app
```

---

## Troubleshooting

### Build Fails
```bash
# Check logs
vercel logs

# Common fix: Clear cache and redeploy
vercel --prod --force
```

### API Returns 500
- Check function logs: `vercel logs --follow`
- Ensure `DATABASE_URL` is set in Vercel env
- First deploy needs DB migration

### Database Errors
```bash
# Pull env locally
vercel env pull

# Run migrations
python -c "from app.database import init_db; init_db()"
```

---

## Auto-Deploy from Git

1. **Vercel Dashboard** → **Add New Project**
2. **Import Git Repository**
3. Select your repo
4. Configure:
   - **Framework**: Vite
   - **Root Directory**: `./`
   - **Build Command**: `npm run build --prefix frontend`
   - **Output Directory**: `frontend/dist`
5. **Deploy**

Now every `git push` auto-deploys!

---

## Commands Reference

```bash
vercel login          # Login to Vercel
vercel               # Deploy to preview
vercel --prod        # Deploy to production
vercel logs          # View logs
vercel logs --follow # Live logs
vercel open          # Open dashboard
vercel env pull      # Get env locally
```

---

## Cost: FREE! 🎉

**Vercel Hobby Plan (Free):**
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Serverless functions (10s timeout)
- ✅ Automatic HTTPS
- ✅ Global CDN

---

## Next Steps

1. ✅ Deploy with `vercel --prod`
2. ✅ Set up database (Vercel Postgres or Neon)
3. ✅ Add `DATABASE_URL` to Vercel env
4. ✅ Test all features
5. ✅ Connect custom domain (optional)

**Full guide:** See [DEPLOY_VERCEL.md](DEPLOY_VERCEL.md)
