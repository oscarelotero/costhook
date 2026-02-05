# Costhook Roadmap

## Phase 1: Core Infrastructure

### Backend
- [x] User model and profile endpoints (GET/PATCH /api/v1/users/me)
- [x] Provider model (id, user_id, type, name, credentials, status, created_at)
- [x] Provider CRUD endpoints (POST/GET/PATCH/DELETE /api/v1/providers)
- [x] Secure credentials storage (encrypt API keys at rest)
- [x] Cost record model (id, provider_id, amount, currency, service, period_start, period_end, metadata)
- [x] Cost records endpoints (GET /api/v1/costs with filters)
- [x] JWT verification via JWKS (asymmetric ES256 keys, no shared secret)

### Frontend
- [x] User settings page (profile, password change)
- [x] Provider management page (list, add, edit, delete providers)
- [x] Add provider form with type-specific fields
- [x] Provider connection status indicator

### Database
- [x] Initial Alembic migration for users extension (profile fields)
- [x] Migration for providers table
- [x] Migration for cost_records table
- [x] Enable RLS on all tables

---

## Phase 2: First Provider Integrations (Supabase, Vercel, Resend)

### Backend - Provider Connectors
- [ ] Base provider connector interface/abstract class
- [ ] Supabase billing integration (organization usage API)
- [ ] Vercel usage API integration
- [ ] Resend usage API integration

### Backend - Data Collection
- [ ] Background job scheduler (APScheduler or Celery)
- [ ] Cost sync job per provider
- [ ] Job status tracking and error handling
- [ ] Manual sync trigger endpoint (POST /api/v1/providers/{id}/sync)

### Frontend
- [ ] Supabase provider setup form + guide
- [ ] Vercel provider setup form + guide
- [ ] Resend provider setup form + guide
- [ ] Sync status and last synced timestamp
- [ ] Manual sync button

---

## Phase 3: Dashboard & Visualization

### Backend
- [ ] Aggregated costs endpoint (GET /api/v1/costs/summary)
- [ ] Costs by provider endpoint (GET /api/v1/costs/by-provider)
- [ ] Costs by service endpoint (GET /api/v1/costs/by-service)
- [ ] Costs over time endpoint (GET /api/v1/costs/timeline)
- [ ] Cost trends/comparison endpoint (current vs previous period)

### Frontend
- [ ] Dashboard layout with widgets
- [ ] Total spend card (current month, previous month, % change)
- [ ] Spend by provider chart (pie/donut)
- [ ] Spend by service chart (bar chart)
- [ ] Spend over time chart (line chart)
- [ ] Date range picker for filtering
- [ ] Provider filter dropdown

---

## Phase 4: Second Provider Integrations (Stripe, OpenAI, Anthropic)

### Backend - Provider Connectors
- [ ] Stripe billing integration
- [ ] OpenAI usage API integration
- [ ] Anthropic usage API integration

### Frontend
- [ ] Stripe provider setup form + guide
- [ ] OpenAI provider setup form + guide
- [ ] Anthropic provider setup form + guide

---

## Phase 5: Alerts & Notifications

### Backend
- [ ] Alert model (id, user_id, provider_id, threshold, currency, notification_type, enabled)
- [ ] Alert CRUD endpoints
- [ ] Alert evaluation job (runs after cost sync)
- [ ] Email notification via Resend
- [ ] Webhook notification support

### Frontend
- [ ] Alerts management page
- [ ] Create/edit alert form (threshold, provider, notification method)
- [ ] Alert history/triggered alerts list

---

## Phase 6: Reports & Export

### Backend
- [ ] Monthly report generation
- [ ] CSV export endpoint (GET /api/v1/costs/export)
- [ ] PDF report generation (optional)

### Frontend
- [ ] Reports page
- [ ] Export button with format selection
- [ ] Scheduled reports configuration (optional)

---

## Phase 7: Polish & Production Ready

### Backend
- [ ] Rate limiting
- [ ] Request logging and monitoring
- [ ] API documentation (OpenAPI/Swagger already included)
- [ ] Error tracking (Sentry integration)
- [ ] Health check endpoint improvements (DB, providers status)

### Frontend
- [ ] Loading states and skeletons
- [ ] Error boundaries and error pages
- [ ] Empty states for no data
- [ ] Mobile responsive design
- [ ] Dark mode (optional)

### DevOps
- [ ] Docker configuration (Dockerfile for backend and frontend)
- [ ] Docker Compose for local development
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Production deployment guide

---

## Future Ideas (Backlog)

### More Provider Integrations
- [ ] AWS Cost Explorer
- [ ] Google Cloud Billing
- [ ] Azure Cost Management
- [ ] DigitalOcean billing
- [ ] Cloudflare billing
- [ ] PlanetScale billing
- [ ] Railway billing
- [ ] Render billing

### Features
- [ ] Team/organization support (multi-user)
- [ ] Budget planning and forecasting
- [ ] Cost anomaly detection
- [ ] Slack integration for alerts
- [ ] Browser extension for quick cost check
- [ ] Mobile app (React Native)
- [ ] API for external integrations
- [ ] Cost optimization recommendations
