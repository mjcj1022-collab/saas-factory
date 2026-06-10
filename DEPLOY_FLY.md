# Deploy to Fly.io — SaaS Factory

## Step 1 — Install Fly CLI (PowerShell, run as admin)
```powershell
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```
Then restart your terminal.

## Step 2 — Sign up and login (free, no card required)
```powershell
fly auth signup
# or if you have an account:
fly auth login
```

## Step 3 — Clone the repo locally
```powershell
cd C:\Users\mjeffreys\Desktop
git clone https://github.com/mjcj1022-collab/saas-factory.git
cd saas-factory
```

## Step 4 — Create Postgres database (free)
```powershell
fly postgres create --name saas-factory-db --region dfw --vm-size shared-cpu-1x --volume-size 1
```
Save the connection string it outputs — you'll need it.

## Step 5 — Create Redis (free via Upstash)
```powershell
fly ext upstash redis create --name saas-factory-redis
```
Save the Redis URL it outputs.

## Step 6 — Create the app
```powershell
fly apps create saas-factory-api
```

## Step 7 — Set environment variables
```powershell
fly secrets set `
  DJANGO_SETTINGS_MODULE=config.settings_prod `
  SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))") `
  DEBUG=False `
  ALLOWED_HOSTS=".fly.dev,localhost" `
  DATABASE_URL="<paste postgres URL from step 4>" `
  REDIS_URL="<paste redis URL from step 5>" `
  ADMIN_EMAIL="admin@saas-factory.app" `
  ADMIN_PASSWORD="<choose a strong password>" `
  OPENAI_API_KEY="sk-..." `
  ANTHROPIC_API_KEY="sk-ant-..." `
  STRIPE_SECRET_KEY="sk_live_..." `
  --app saas-factory-api
```

## Step 8 — Deploy
```powershell
fly deploy --app saas-factory-api --config fly.toml
```
Takes 3-5 minutes. Watch logs:
```powershell
fly logs --app saas-factory-api
```

## Step 9 — Get your URL
```powershell
fly status --app saas-factory-api
```
Your app will be live at: https://saas-factory-api.fly.dev

## Step 10 — Verify
```powershell
curl https://saas-factory-api.fly.dev/health/
# Should return: {"status": "ok", ...}
```

Admin panel: https://saas-factory-api.fly.dev/admin/

## Deploy Celery Worker (optional — needed for AI tasks)
```powershell
fly apps create saas-factory-celery
fly secrets set DATABASE_URL="<postgres url>" REDIS_URL="<redis url>" SECRET_KEY="<same key>" DJANGO_SETTINGS_MODULE=config.settings_prod --app saas-factory-celery
fly deploy --app saas-factory-celery --config fly.worker.toml
```

## Frontend — Vercel (free, no card)
```powershell
npm install -g vercel
cd frontend
vercel --prod
# When prompted: set VITE_API_URL=https://saas-factory-api.fly.dev/api
```

## After deploy — set CORS
```powershell
fly secrets set CORS_ALLOWED_ORIGINS="https://your-app.vercel.app" --app saas-factory-api
```
