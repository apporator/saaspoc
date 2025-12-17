# Integration POC Demo

## Overview

This is an end-to-end integration POC demonstrating how external SaaS data can be ingested, processed, and exposed to users. It showcases the core competency of Solutions Engineering: connecting disparate systems and delivering business value through unified dashboards.

## Project Architecture

```
/
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration and session management
├── models.py            # SQLAlchemy data models
├── auth.py              # JWT authentication and RBAC
├── external_api.py      # Mock SaaS API endpoints
├── integrations.py      # External API integrations (Stripe, GitHub, OpenWeather)
├── templates/           # Jinja2 HTML templates
│   ├── base.html        # Base template with navigation
│   ├── login.html       # Login page
│   ├── dashboard.html   # Main dashboard with KPIs
│   ├── orders.html      # Orders data table
│   ├── stripe.html      # Stripe payments dashboard
│   ├── github.html      # GitHub issues dashboard
│   └── weather.html     # Weather telemetry dashboard
├── static/              # Static assets
├── README.md            # Project documentation
└── SECURITY.md          # Security documentation
```

## Key Components

### Data Sources
1. **Mock SaaS API** - Internal simulated API for orders/customers/events
2. **Stripe** - Payment transaction data (uses test/mock data if no API key)
3. **GitHub** - Repository issues tracking (uses mock data if no token)
4. **OpenWeather** - Weather telemetry data (uses mock data if no API key)

### Authentication
- JWT-based with 60-minute expiration
- Two roles: `admin` (full access) and `viewer` (read-only)
- Demo credentials: admin/admin123, viewer/viewer123

### Database
- PostgreSQL with SQLAlchemy ORM
- Tables: orders, customers, events, stripe_payments, github_issues, weather_data, sync_logs, audit_logs

## Running the Application

```bash
python main.py
```

Server runs on port 5000.

## User Preferences

- Clean, professional UI using Tailwind CSS
- Server-rendered HTML with minimal JavaScript
- Sync buttons on each data source card
- Filter and pagination for data tables

## Recent Changes

- Initial project setup with FastAPI backend
- Created 4 data source integrations
- Implemented JWT authentication with RBAC
- Built responsive dashboard and data table UIs
