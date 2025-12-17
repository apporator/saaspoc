from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Enum
from database import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PROCESSING = "processing"

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, index=True)
    customer_name = Column(String(255))
    status = Column(String(50), default="pending")
    amount = Column(Float)
    source = Column(String(50), default="mock_saas")
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, index=True)
    name = Column(String(255))
    email = Column(String(255))
    company = Column(String(255))
    source = Column(String(50), default="mock_saas")
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String(100), unique=True, index=True)
    event_type = Column(String(100))
    description = Column(Text)
    source = Column(String(50), default="mock_saas")
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

class StripePayment(Base):
    __tablename__ = "stripe_payments"
    
    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(String(100), unique=True, index=True)
    amount = Column(Float)
    currency = Column(String(10))
    status = Column(String(50))
    customer_email = Column(String(255))
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

class GitHubIssue(Base):
    __tablename__ = "github_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(Integer, unique=True, index=True)
    title = Column(String(500))
    state = Column(String(50))
    author = Column(String(255))
    repository = Column(String(255))
    labels = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), index=True)
    temperature = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    description = Column(String(255))
    wind_speed = Column(Float)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    synced_at = Column(DateTime, default=datetime.utcnow)

class SyncLog(Base):
    __tablename__ = "sync_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50))
    records_synced = Column(Integer)
    status = Column(String(50))
    synced_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user = Column(String(255))
    action = Column(String(100))
    resource = Column(String(100))
    details = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
