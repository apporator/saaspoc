import os
import requests
from datetime import datetime
from typing import Optional

STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")

def fetch_stripe_payments(limit: int = 25):
    if not STRIPE_API_KEY:
        return generate_mock_stripe_payments(limit)
    
    try:
        response = requests.get(
            "https://api.stripe.com/v1/charges",
            params={"limit": limit},
            auth=(STRIPE_API_KEY, ""),
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            payments = []
            for charge in data.get("data", []):
                payments.append({
                    "payment_id": charge["id"],
                    "amount": charge["amount"] / 100,
                    "currency": charge.get("currency", "usd").upper(),
                    "status": charge.get("status", "unknown"),
                    "customer_email": charge.get("billing_details", {}).get("email", "N/A"),
                    "description": charge.get("description", "No description"),
                    "created_at": datetime.fromtimestamp(charge["created"]).isoformat()
                })
            return {"data": payments, "source": "stripe_live", "success": True}
        else:
            return generate_mock_stripe_payments(limit)
    except Exception as e:
        return generate_mock_stripe_payments(limit)

def generate_mock_stripe_payments(count: int = 25):
    import random
    payments = []
    statuses = ["succeeded", "pending", "failed"]
    weights = [0.8, 0.15, 0.05]
    emails = ["customer@example.com", "buyer@company.com", "user@business.org", "client@startup.io"]
    
    for i in range(count):
        payments.append({
            "payment_id": f"ch_mock_{100000 + i}",
            "amount": round(random.uniform(10, 500), 2),
            "currency": "USD",
            "status": random.choices(statuses, weights=weights)[0],
            "customer_email": random.choice(emails),
            "description": f"Payment for order #{random.randint(1000, 9999)}",
            "created_at": datetime.utcnow().isoformat()
        })
    return {"data": payments, "source": "stripe_mock", "success": True}

def fetch_github_issues(repo: str = "facebook/react", limit: int = 25):
    if not GITHUB_TOKEN:
        return generate_mock_github_issues(limit)
    
    try:
        headers = {"Authorization": f"token {GITHUB_TOKEN}"}
        response = requests.get(
            f"https://api.github.com/repos/{repo}/issues",
            params={"per_page": limit, "state": "all"},
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            issues = []
            for issue in data:
                issues.append({
                    "issue_id": issue["id"],
                    "title": issue["title"][:200],
                    "state": issue["state"],
                    "author": issue["user"]["login"],
                    "repository": repo,
                    "labels": ",".join([l["name"] for l in issue.get("labels", [])]),
                    "created_at": issue["created_at"]
                })
            return {"data": issues, "source": "github_live", "success": True}
        else:
            return generate_mock_github_issues(limit)
    except Exception as e:
        return generate_mock_github_issues(limit)

def generate_mock_github_issues(count: int = 25):
    import random
    issues = []
    titles = [
        "Bug: Component not rendering correctly",
        "Feature request: Add dark mode support",
        "Performance issue with large datasets",
        "Documentation update needed",
        "Refactor: Improve code organization",
        "Fix: Memory leak in event handler",
        "Add unit tests for new module",
        "Update dependencies to latest versions"
    ]
    authors = ["developer1", "contributor42", "maintainer", "user123", "coder99"]
    repos = ["facebook/react", "vercel/next.js", "microsoft/vscode"]
    
    for i in range(count):
        issues.append({
            "issue_id": 50000 + i,
            "title": random.choice(titles) + f" #{i+1}",
            "state": random.choice(["open", "closed"]),
            "author": random.choice(authors),
            "repository": random.choice(repos),
            "labels": random.choice(["bug", "enhancement", "documentation", "help wanted"]),
            "created_at": datetime.utcnow().isoformat()
        })
    return {"data": issues, "source": "github_mock", "success": True}

def fetch_weather_data(cities: list = None):
    if cities is None:
        cities = ["London", "New York", "Tokyo", "Sydney", "Paris"]
    
    if not OPENWEATHER_API_KEY:
        return generate_mock_weather_data(cities)
    
    try:
        weather_data = []
        for city in cities:
            response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                weather_data.append({
                    "city": city,
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "recorded_at": datetime.utcnow().isoformat()
                })
        if weather_data:
            return {"data": weather_data, "source": "openweather_live", "success": True}
        return generate_mock_weather_data(cities)
    except Exception as e:
        return generate_mock_weather_data(cities)

def generate_mock_weather_data(cities: list):
    import random
    weather_data = []
    descriptions = ["clear sky", "few clouds", "scattered clouds", "light rain", "sunny", "overcast"]
    
    for city in cities:
        weather_data.append({
            "city": city,
            "temperature": round(random.uniform(-5, 35), 1),
            "feels_like": round(random.uniform(-8, 38), 1),
            "humidity": random.randint(30, 90),
            "description": random.choice(descriptions),
            "wind_speed": round(random.uniform(0, 20), 1),
            "recorded_at": datetime.utcnow().isoformat()
        })
    return {"data": weather_data, "source": "openweather_mock", "success": True}
