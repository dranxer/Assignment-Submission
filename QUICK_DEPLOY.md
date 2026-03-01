# 🚀 Quick Deploy Reference

## Fastest Way: Netlify + Render (5 minutes)

### 1️⃣ Deploy Backend (Render)
```bash
# Push to GitHub first
git init
git add .
git commit -m "Deploy"
git remote add origin YOUR_REPO_URL
git push -u origin main
```

Then:
1. Go to https://render.com
2. **New +** → **Blueprint**
3. Connect GitHub repo
4. Wait for deploy ✅

**Copy your backend URL:** `https://your-app.onrender.com`

---

### 2️⃣ Deploy Frontend (Netlify)
```bash
cd frontend

# Update netlify.toml - replace YOUR_BACKEND_URL
# Then deploy:
npm install -g netlify-cli
netlify login
netlify init
netlify deploy --prod
```

**Your frontend URL:** `https://your-app.netlify.app`

---

### 3️⃣ Update CORS (Render Dashboard)
```
Environment Variables → Add:
CORS_ORIGINS = https://your-app.netlify.app
```

---

### 4️⃣ Test
Open `https://your-app.netlify.app` ✅

---

## Alternative: One-Command Deploy (Docker)
```bash
docker-compose up -d
```
Opens at: http://localhost

---

## Cost: $0/month 🎉

| Service | Plan | Limits |
|---------|------|--------|
| Netlify | Free | 100GB bandwidth |
| Render | Free | 750 hours/month, 1GB DB |

---

## Files Already Created ✅

- `frontend/netlify.toml` - Netlify config
- `frontend/public/_redirects` - API redirects
- `render.yaml` - Render blueprint
- `docker-compose.yml` - Docker setup
- `DEPLOY_NETLIFY.md` - Detailed guide

---

## Need Help?

- **Netlify Docs:** https://docs.netlify.com
- **Render Docs:** https://render.com/docs
- **Troubleshooting:** See DEPLOYMENT.md
