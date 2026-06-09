# SaaS Factory — Vertical SaaS Platform

A monorepo platform powering 10 vertical SaaS products on a shared infrastructure layer.

## Architecture

```
saas-factory/
├── platform/           # Shared infrastructure
│   ├── organizations/  # Auth, users, multi-tenancy
│   ├── billing/        # Stripe subscriptions, invoices
│   ├── events/         # Domain event bus
│   ├── workflows/      # Visual workflow automation
│   ├── ai/             # Multi-provider AI layer
│   ├── notifications/  # Email, SMS, Slack, Push
│   ├── audit/          # Audit logging
│   ├── feature_flags/  # Feature flag engine
│   ├── analytics/      # KPIs, dashboards
│   └── integrations/   # Third-party connectors
│
├── apps/               # Vertical products
│   ├── rfp/            # 1. AI RFP Response Matrix
│   ├── construction/   # 2. Construction Liaison Platform
│   ├── franchise/      # 3. Franchise Onboarding Hub
│   ├── fleet/          # 4. Fleet Maintenance Optimizer
│   ├── solar/          # 5. Solar Compliance Engine
│   ├── hospitality/    # 6. Guest Relations Integrator
│   ├── venue/          # 7. Venue Operations Hub
│   ├── sourcing/       # 8. Manufacturer Sourcing Pipeline
│   ├── agency/         # 9. Agency Deliverable Matrix
│   └── food/           # 10. Food Supply Connector
│
├── frontend/           # React/TypeScript frontend
├── infrastructure/     # Docker, Nginx configs
└── scripts/            # Dev tooling
```

## Stack

- **Backend**: Django 4.2 + DRF
- **Database**: PostgreSQL 16 + pgvector
- **Queue**: Celery + Redis
- **AI**: OpenAI GPT-4o-mini + Anthropic Claude (routed by task type)
- **Payments**: Stripe
- **Frontend**: React + TypeScript + Tailwind
- **Infra**: Docker Compose → Kubernetes-ready

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/ARCANGEL-22/saas-factory
cd saas-factory
cp .env.example .env
# Fill in OPENAI_API_KEY, STRIPE_SECRET_KEY, etc.

# 2. Start services
docker-compose up -d db redis

# 3. Run backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# 4. Start Celery
celery -A config worker -l INFO
```

## Add a New Vertical

```bash
python scripts/create_vertical.py <name>
```

Scaffolds models, views, URLs, tasks, serializers, and admin in under 5 seconds.

## Products

| # | Product | Target Customer | Price Range |
|---|---------|----------------|-------------|
| 1 | AI RFP Response Matrix | Enterprise vendors | $99–$999/mo |
| 2 | Construction Liaison | GCs, project managers | $199–$2,499/mo |
| 3 | Franchise Onboarding | Franchise brands | $299–$2,999/mo |
| 4 | Fleet Maintenance | Fleet operators | $149–$2,499/mo |
| 5 | Solar Compliance | Solar installers / EPCs | $199–$4,999/mo |
| 6 | Guest Relations | STR operators / PMs | $49–$999/mo |
| 7 | Venue Operations | Event venues | $149–$2,999/mo |
| 8 | Manufacturer Sourcing | CPG / importers | TBD |
| 9 | Agency Deliverable Matrix | Creative agencies | TBD |
| 10 | Food Supply Connector | Farms, distributors | TBD |

## Platform Shared Services

Every vertical automatically inherits:
- Multi-tenant auth with org-scoped data
- Stripe billing with plan enforcement
- Domain event bus (Redis Streams ready)
- Visual workflow automation engine
- AI router (OpenAI / Anthropic / local)
- Notification hub (email, SMS, Slack, push)
- Audit logging (enterprise compliance)
- Feature flags (safe rollouts)
- Analytics + KPI dashboards
- 20+ third-party integrations

## License

Private — all rights reserved.
