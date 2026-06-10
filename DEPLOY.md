# Deployment Guide — SaaS Factory

## Stack
- **Backend**: Railway (Django + Celery + Postgres + Redis)
- **Frontend**: Vercel (React/Vite)
- **Payments**: Stripe
- **AI**: OpenAI + Anthropic

---

## Step 1 — Railway Backend

### 1a. Install Railway CLI
```powershell
npm install -g @railway/cli
railway login
```

### 1b. Create project
```powershell
cd C:\Users\mjeffreys\Desktop\saas-factory   # wherever you extracted the zip
railway init
# Name it: saas-factory
```

### 1c. Add Postgres + Redis
```powershell
railway add --plugin postgresql
railway add --plugin redis
```

### 1d. Set environment variables
```powershell
railway variables set DJANGO_SETTINGS_MODULE=config.settings_prod
railway variables set DEBUG=False
railway variables set ALLOWED_HOSTS=".railway.app,.vercel.app,localhost"

# Generate a secret key (run this, copy output, paste below)
python -c "import secrets; print(secrets.token_urlsafe(50))"
railway variables set SECRET_KEY=<paste_generated_key>

# Your API keys
railway variables set OPENAI_API_KEY=sk-...
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set STRIPE_SECRET_KEY=sk_live_...
railway variables set STRIPE_WEBHOOK_SECRET=whsec_...

# Admin user for first login
railway variables set ADMIN_EMAIL=admin@yourdomain.com
railway variables set ADMIN_PASSWORD=<strong_password>
```

### 1e. Deploy
```powershell
railway up
```

Wait ~3 minutes. Check logs:
```powershell
railway logs
```

### 1f. Get your backend URL
```powershell
railway domain
# Example output: saas-factory-production.up.railway.app
```

---

## Step 2 — Vercel Frontend

### 2a. Install Vercel CLI
```powershell
npm install -g vercel
```

### 2b. Update API URL
Edit `frontend/.env.production`:
```
VITE_API_URL=https://YOUR_RAILWAY_URL/api
```

### 2c. Deploy
```powershell
cd frontend
vercel login
vercel --prod
```

When prompted:
- Link to existing project? **No**
- Project name: `saas-factory`
- Directory: `.` (current)
- Override settings? **No**

Note the Vercel URL (e.g. `saas-factory.vercel.app`)

### 2d. Update CORS on Railway
```powershell
railway variables set CORS_ALLOWED_ORIGINS=https://saas-factory.vercel.app
```

---

## Step 3 — Stripe Setup

### 3a. Create products and prices
```powershell
cd ..  # back in saas-factory root
$env:STRIPE_SECRET_KEY="sk_live_..."
python scripts/setup_stripe.py
```

This outputs price IDs — paste them into `config/settings_prod.py`.

### 3b. Set up webhook
In Stripe Dashboard → Webhooks → Add endpoint:
- URL: `https://YOUR_RAILWAY_URL/webhooks/stripe/`
- Events: `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.paid`

Copy the webhook signing secret → set in Railway:
```powershell
railway variables set STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## Step 4 — Verify

```powershell
# Health check
curl https://YOUR_RAILWAY_URL/health/

# Admin panel
# Open: https://YOUR_RAILWAY_URL/admin/
# Login with ADMIN_EMAIL / ADMIN_PASSWORD

# Frontend
# Open: https://saas-factory.vercel.app
```

---

## Step 5 — Custom Domain (optional)

### Backend (Railway)
Railway Dashboard → Settings → Domains → Add custom domain

### Frontend (Vercel)
Vercel Dashboard → Settings → Domains → Add domain

---

## Celery Worker (Railway)

Add a second service in Railway Dashboard:
- Source: same GitHub repo
- Start command: `celery -A config worker -l INFO -c 4`
- Set same env vars as the web service

---

## Quick reference

| Service | URL |
|---------|-----|
| Backend API | `https://YOUR_RAILWAY_URL/api/` |
| Admin | `https://YOUR_RAILWAY_URL/admin/` |
| Health | `https://YOUR_RAILWAY_URL/health/` |
| Frontend | `https://saas-factory.vercel.app` |
| Stripe webhook | `https://YOUR_RAILWAY_URL/webhooks/stripe/` |
