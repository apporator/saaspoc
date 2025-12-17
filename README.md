# Integration POC Demo

End-to-end integration demo showing how external SaaS data can be ingested, processed, and exposed to users.

## Overview

"I can ingest data from a third-party system, process it securely, and present actionable output to users."

This demo proves the core competency of Solutions Engineering: connecting disparate systems and delivering business value through unified dashboards.

## Architecture

```
[ External API / Data Sources ]
        |
        |  Mock SaaS API     Stripe API      GitHub API      OpenWeather API
        |       |                |               |                |
        +-------+----------------+---------------+----------------+
                                 |
                              (REST)
                                 |
                    +------------------------+
                    |    FastAPI Backend     |
                    |------------------------|
                    | - JWT Authentication   |
                    | - Role-based Access    |
                    | - Data Normalization   |
                    +------------------------+
                                 |
                    +------------------------+
                    |   PostgreSQL Database  |
                    |------------------------|
                    | - Orders               |
                    | - Stripe Payments      |
                    | - GitHub Issues        |
                    | - Weather Data         |
                    | - Audit Logs           |
                    +------------------------+
                                 |
                    +------------------------+
                    |       Web UI           |
                    |------------------------|
                    | - Dashboard            |
                    | - Data Tables          |
                    | - KPI Cards            |
                    +------------------------+
```

## Use Cases

- CRM / Fintech / SaaS integrations
- Customer onboarding POCs
- Pre-sales demonstrations
- Multi-source data aggregation
- Real-time telemetry dashboards

## Demo Flow

1. **Authenticate** - Login as admin or viewer with role-based access
2. **Sync External Data** - Click sync buttons to fetch from external APIs
3. **View Metrics** - Dashboard updates with KPIs and aggregated data
4. **Explore Data** - Browse detailed tables with filtering and pagination

## Data Sources

| Source | Type | Description |
|--------|------|-------------|
| Mock SaaS API | Internal | Simulated customer/order data |
| Stripe | Payments | Transaction and revenue data |
| GitHub | Issues | Repository issue tracking |
| OpenWeather | Telemetry | Weather conditions and metrics |

## Security

- JWT-based authentication
- Role-based access control (admin/viewer)
- Encrypted transport (TLS)
- Audit logging for all actions
- No credentials stored in frontend

## Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Viewer | viewer | viewer123 |

## API Endpoints

### Authentication
- `POST /login` - Authenticate and receive JWT

### Data Sync
- `POST /api/sync/orders` - Sync from Mock SaaS
- `POST /api/sync/stripe` - Sync from Stripe
- `POST /api/sync/github` - Sync from GitHub
- `POST /api/sync/weather` - Sync from OpenWeather

### Query Data
- `GET /orders` - List orders with filtering
- `GET /api/metrics` - Aggregated metrics

### External Mock API
- `GET /external/customers` - Mock customer data
- `GET /external/orders` - Mock order data
- `GET /external/events` - Mock event data

## Technology Stack

- **Backend**: Python 3.11, FastAPI
- **Database**: PostgreSQL
- **Auth**: JWT (PyJWT)
- **ORM**: SQLAlchemy
- **Frontend**: Jinja2 Templates, Tailwind CSS
- **APIs**: Stripe, GitHub, OpenWeather

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| DATABASE_URL | PostgreSQL connection string | Yes |
| SESSION_SECRET | JWT signing secret | Yes |
| STRIPE_API_KEY | Stripe API key | Optional |
| GITHUB_TOKEN | GitHub personal access token | Optional |
| OPENWEATHER_API_KEY | OpenWeather API key | Optional |

## Running Locally

```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Why This Demo Works

- Looks like a real customer POC
- Demonstrates APIs, integrations, security, and UI output
- Easy to explain to technical and non-technical stakeholders
- Easy to extend with additional data sources
