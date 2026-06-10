# deploy.ps1
# Full deployment script for SaaS Factory
# Run from: C:\Users\mjeffreys\saas-factory\
# Requirements: railway CLI + vercel CLI installed

Write-Host "=== SaaS Factory Deployment ===" -ForegroundColor Cyan

# ── Step 1: Install CLIs if missing ──────────────────────────────────────────
Write-Host "`n[1/6] Checking CLI tools..." -ForegroundColor Yellow

if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Railway CLI..." -ForegroundColor Gray
    npm install -g @railway/cli
}

if (-not (Get-Command vercel -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Vercel CLI..." -ForegroundColor Gray
    npm install -g vercel
}

Write-Host "CLIs ready." -ForegroundColor Green

# ── Step 2: Railway login + project setup ────────────────────────────────────
Write-Host "`n[2/6] Railway setup..." -ForegroundColor Yellow
Write-Host "Logging into Railway (browser will open)..."
railway login

Write-Host "Creating Railway project..."
railway init --name saas-factory

Write-Host "Adding PostgreSQL..."
railway add --plugin postgresql

Write-Host "Adding Redis..."
railway add --plugin redis

# ── Step 3: Set Railway env vars ─────────────────────────────────────────────
Write-Host "`n[3/6] Setting Railway environment variables..." -ForegroundColor Yellow

$SECRET_KEY = -join ((65..90) + (97..122) + (48..57) | Get-Random -Count 50 | ForEach-Object {[char]$_})

railway variables set `
    DJANGO_SETTINGS_MODULE=config.settings_prod `
    SECRET_KEY=$SECRET_KEY `
    DEBUG=False `
    ALLOWED_HOSTS=".railway.app,.onrender.com,localhost"

Write-Host "Core env vars set." -ForegroundColor Green
Write-Host ""
Write-Host "You still need to set these manually in Railway dashboard:" -ForegroundColor Yellow
Write-Host "  OPENAI_API_KEY=sk-..."
Write-Host "  ANTHROPIC_API_KEY=sk-ant-..."
Write-Host "  STRIPE_SECRET_KEY=sk_live_..."
Write-Host "  STRIPE_WEBHOOK_SECRET=whsec_..."
Write-Host "  CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app"

# ── Step 4: Deploy backend to Railway ────────────────────────────────────────
Write-Host "`n[4/6] Deploying backend to Railway..." -ForegroundColor Yellow
railway up --detach

Write-Host "Backend deploying... check status at https://railway.app/dashboard" -ForegroundColor Green

# Get the deployed URL
$BACKEND_URL = railway domain 2>$null
if ($BACKEND_URL) {
    Write-Host "Backend URL: https://$BACKEND_URL" -ForegroundColor Cyan
} else {
    Write-Host "Run 'railway domain' after deployment to get your backend URL" -ForegroundColor Gray
    $BACKEND_URL = "saas-factory-api.railway.app"
}

# ── Step 5: Update frontend API URL ─────────────────────────────────────────
Write-Host "`n[5/6] Configuring frontend..." -ForegroundColor Yellow

$envContent = "VITE_API_URL=https://$BACKEND_URL/api"
Set-Content -Path "frontend\.env.production" -Value $envContent -Encoding UTF8
Write-Host "Frontend API URL set to: https://$BACKEND_URL/api" -ForegroundColor Green

# ── Step 6: Deploy frontend to Vercel ────────────────────────────────────────
Write-Host "`n[6/6] Deploying frontend to Vercel..." -ForegroundColor Yellow

Set-Location frontend

Write-Host "Logging into Vercel..."
vercel login

Write-Host "Deploying to Vercel production..."
vercel --prod --yes `
    -e VITE_API_URL="https://$BACKEND_URL/api"

Set-Location ..

# ── Done ─────────────────────────────────────────────────────────────────────
Write-Host "`n=== Deployment Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Go to https://railway.app/dashboard and set your API keys"
Write-Host "2. Go to https://vercel.com/dashboard and note your frontend URL"
Write-Host "3. Set CORS_ALLOWED_ORIGINS in Railway to your Vercel URL"
Write-Host "4. Set up Stripe webhook: stripe listen --forward-to https://$BACKEND_URL/webhooks/stripe/"
Write-Host "5. Create superuser: railway run python manage.py createsuperuser"
Write-Host ""
Write-Host "Admin panel: https://$BACKEND_URL/admin/" -ForegroundColor Cyan
