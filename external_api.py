import random
from datetime import datetime, timedelta
from fastapi import APIRouter

router = APIRouter(prefix="/external", tags=["External Mock API"])

CUSTOMER_NAMES = [
    "Acme Corp", "TechStart Inc", "Global Solutions", "InnovateTech", 
    "DataFlow Systems", "CloudNine Ltd", "ByteWise Solutions", "NextGen Dynamics",
    "Alpha Industries", "Quantum Labs", "Cyber Solutions", "Digital Frontier",
    "Smart Systems", "Future Tech", "Pioneer Enterprises", "Velocity Corp"
]

PRODUCT_NAMES = [
    "Enterprise License", "Pro Subscription", "Basic Plan", "Premium Support",
    "API Access", "Data Analytics", "Cloud Storage", "Security Suite",
    "Team Collaboration", "Integration Package", "Custom Development", "Consulting Hours"
]

EVENT_TYPES = [
    "user.created", "user.updated", "order.placed", "order.completed",
    "payment.received", "subscription.renewed", "account.upgraded", "support.ticket.opened"
]

def generate_mock_customers(count: int = 20):
    customers = []
    for i in range(count):
        customers.append({
            "id": f"cust_{1000 + i}",
            "name": random.choice(CUSTOMER_NAMES) + f" #{i+1}",
            "email": f"contact{i+1}@company{i+1}.com",
            "company": random.choice(CUSTOMER_NAMES),
            "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 365))).isoformat()
        })
    return customers

def generate_mock_orders(count: int = 50):
    orders = []
    statuses = ["pending", "completed", "processing", "cancelled"]
    weights = [0.15, 0.60, 0.15, 0.10]
    
    for i in range(count):
        orders.append({
            "id": f"ord_{10000 + i}",
            "customer_name": random.choice(CUSTOMER_NAMES),
            "product": random.choice(PRODUCT_NAMES),
            "status": random.choices(statuses, weights=weights)[0],
            "amount": round(random.uniform(99.99, 9999.99), 2),
            "created_at": (datetime.utcnow() - timedelta(days=random.randint(0, 90))).isoformat()
        })
    return orders

def generate_mock_events(count: int = 30):
    events = []
    for i in range(count):
        event_type = random.choice(EVENT_TYPES)
        events.append({
            "id": f"evt_{20000 + i}",
            "type": event_type,
            "description": f"Event {event_type} triggered by system",
            "created_at": (datetime.utcnow() - timedelta(hours=random.randint(0, 168))).isoformat()
        })
    return events

@router.get("/customers")
def get_external_customers():
    return {"data": generate_mock_customers(), "source": "mock_saas_api", "timestamp": datetime.utcnow().isoformat()}

@router.get("/orders")
def get_external_orders():
    return {"data": generate_mock_orders(), "source": "mock_saas_api", "timestamp": datetime.utcnow().isoformat()}

@router.get("/events")
def get_external_events():
    return {"data": generate_mock_events(), "source": "mock_saas_api", "timestamp": datetime.utcnow().isoformat()}
