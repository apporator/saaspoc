import os
from datetime import datetime
from fastapi import FastAPI, Request, Depends, HTTPException, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import engine, get_db, Base
from models import Order, Customer, Event, StripePayment, GitHubIssue, WeatherData, SyncLog, AuditLog
from auth import create_access_token, authenticate_user, get_current_user, get_admin_user, require_role
from external_api import router as external_router, generate_mock_orders
from integrations import fetch_stripe_payments, fetch_github_issues, fetch_weather_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Integration POC Demo", version="1.0.0")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(external_router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return RedirectResponse(url="/login")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    token = create_access_token({"sub": user["username"], "role": user["role"], "name": user["name"]})
    
    audit = AuditLog(user=username, action="login", resource="auth", details="User logged in")
    db.add(audit)
    db.commit()
    
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=3600)
    return response

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("access_token")
    return response

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request)
    except HTTPException:
        return RedirectResponse(url="/login")
    
    orders_count = db.query(func.count(Order.id)).scalar() or 0
    orders_pending = db.query(func.count(Order.id)).filter(Order.status == "pending").scalar() or 0
    orders_completed = db.query(func.count(Order.id)).filter(Order.status == "completed").scalar() or 0
    total_revenue = db.query(func.sum(Order.amount)).filter(Order.status == "completed").scalar() or 0
    
    stripe_count = db.query(func.count(StripePayment.id)).scalar() or 0
    github_count = db.query(func.count(GitHubIssue.id)).scalar() or 0
    weather_count = db.query(func.count(WeatherData.id)).scalar() or 0
    
    last_sync = db.query(SyncLog).order_by(SyncLog.synced_at.desc()).first()
    last_sync_time = last_sync.synced_at.strftime("%Y-%m-%d %H:%M:%S") if last_sync else "Never"
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "user": user,
        "orders_count": orders_count,
        "orders_pending": orders_pending,
        "orders_completed": orders_completed,
        "total_revenue": round(total_revenue, 2),
        "stripe_count": stripe_count,
        "github_count": github_count,
        "weather_count": weather_count,
        "last_sync_time": last_sync_time
    })

@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request, status: str = Query(None), page: int = Query(1), db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request)
    except HTTPException:
        return RedirectResponse(url="/login")
    
    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    
    per_page = 20
    total = query.count()
    orders = query.order_by(Order.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()
    total_pages = (total + per_page - 1) // per_page
    
    return templates.TemplateResponse("orders.html", {
        "request": request,
        "user": user,
        "orders": orders,
        "current_status": status,
        "page": page,
        "total_pages": total_pages,
        "total": total
    })

@app.get("/stripe", response_class=HTMLResponse)
async def stripe_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request)
    except HTTPException:
        return RedirectResponse(url="/login")
    
    payments = db.query(StripePayment).order_by(StripePayment.created_at.desc()).limit(50).all()
    total_amount = db.query(func.sum(StripePayment.amount)).filter(StripePayment.status == "succeeded").scalar() or 0
    succeeded_count = db.query(func.count(StripePayment.id)).filter(StripePayment.status == "succeeded").scalar() or 0
    pending_count = db.query(func.count(StripePayment.id)).filter(StripePayment.status == "pending").scalar() or 0
    
    return templates.TemplateResponse("stripe.html", {
        "request": request,
        "user": user,
        "payments": payments,
        "total_amount": round(total_amount, 2),
        "succeeded_count": succeeded_count,
        "pending_count": pending_count
    })

@app.get("/github", response_class=HTMLResponse)
async def github_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request)
    except HTTPException:
        return RedirectResponse(url="/login")
    
    issues = db.query(GitHubIssue).order_by(GitHubIssue.created_at.desc()).limit(50).all()
    open_count = db.query(func.count(GitHubIssue.id)).filter(GitHubIssue.state == "open").scalar() or 0
    closed_count = db.query(func.count(GitHubIssue.id)).filter(GitHubIssue.state == "closed").scalar() or 0
    
    return templates.TemplateResponse("github.html", {
        "request": request,
        "user": user,
        "issues": issues,
        "open_count": open_count,
        "closed_count": closed_count
    })

@app.get("/weather", response_class=HTMLResponse)
async def weather_page(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request)
    except HTTPException:
        return RedirectResponse(url="/login")
    
    weather = db.query(WeatherData).order_by(WeatherData.recorded_at.desc()).all()
    cities_count = db.query(func.count(func.distinct(WeatherData.city))).scalar() or 0
    avg_temp = db.query(func.avg(WeatherData.temperature)).scalar() or 0
    
    return templates.TemplateResponse("weather.html", {
        "request": request,
        "user": user,
        "weather": weather,
        "cities_count": cities_count,
        "avg_temp": round(avg_temp, 1)
    })

@app.post("/api/sync/orders")
async def sync_orders(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_admin_user(request)
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    
    mock_orders = generate_mock_orders()
    
    synced = 0
    for order_data in mock_orders:
        existing = db.query(Order).filter(Order.external_id == order_data["id"]).first()
        if not existing:
            order = Order(
                external_id=order_data["id"],
                customer_name=order_data["customer_name"],
                status=order_data["status"],
                amount=order_data["amount"],
                source="mock_saas"
            )
            db.add(order)
            synced += 1
    
    sync_log = SyncLog(source="mock_saas", records_synced=synced, status="success")
    db.add(sync_log)
    
    audit = AuditLog(user=user.get("sub"), action="sync", resource="orders", details=f"Synced {synced} orders")
    db.add(audit)
    db.commit()
    
    return {"success": True, "synced": synced, "source": "mock_saas"}

@app.post("/api/sync/stripe")
async def sync_stripe(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_admin_user(request)
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    
    result = fetch_stripe_payments()
    synced = 0
    
    for payment_data in result.get("data", []):
        existing = db.query(StripePayment).filter(StripePayment.payment_id == payment_data["payment_id"]).first()
        if not existing:
            payment = StripePayment(
                payment_id=payment_data["payment_id"],
                amount=payment_data["amount"],
                currency=payment_data["currency"],
                status=payment_data["status"],
                customer_email=payment_data["customer_email"],
                description=payment_data["description"]
            )
            db.add(payment)
            synced += 1
    
    sync_log = SyncLog(source="stripe", records_synced=synced, status="success")
    db.add(sync_log)
    db.commit()
    
    return {"success": True, "synced": synced, "source": result.get("source")}

@app.post("/api/sync/github")
async def sync_github(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_admin_user(request)
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    
    result = fetch_github_issues()
    synced = 0
    
    for issue_data in result.get("data", []):
        existing = db.query(GitHubIssue).filter(GitHubIssue.issue_id == issue_data["issue_id"]).first()
        if not existing:
            issue = GitHubIssue(
                issue_id=issue_data["issue_id"],
                title=issue_data["title"],
                state=issue_data["state"],
                author=issue_data["author"],
                repository=issue_data["repository"],
                labels=issue_data["labels"]
            )
            db.add(issue)
            synced += 1
    
    sync_log = SyncLog(source="github", records_synced=synced, status="success")
    db.add(sync_log)
    db.commit()
    
    return {"success": True, "synced": synced, "source": result.get("source")}

@app.post("/api/sync/weather")
async def sync_weather(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_admin_user(request)
    except HTTPException as e:
        return JSONResponse({"error": e.detail}, status_code=e.status_code)
    
    result = fetch_weather_data()
    synced = 0
    
    for weather_data in result.get("data", []):
        weather = WeatherData(
            city=weather_data["city"],
            temperature=weather_data["temperature"],
            feels_like=weather_data["feels_like"],
            humidity=weather_data["humidity"],
            description=weather_data["description"],
            wind_speed=weather_data["wind_speed"]
        )
        db.add(weather)
        synced += 1
    
    sync_log = SyncLog(source="openweather", records_synced=synced, status="success")
    db.add(sync_log)
    db.commit()
    
    return {"success": True, "synced": synced, "source": result.get("source")}

@app.get("/api/metrics")
async def get_metrics(request: Request, db: Session = Depends(get_db)):
    try:
        user = await get_current_user(request)
    except HTTPException:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    return {
        "orders": {
            "total": db.query(func.count(Order.id)).scalar() or 0,
            "pending": db.query(func.count(Order.id)).filter(Order.status == "pending").scalar() or 0,
            "completed": db.query(func.count(Order.id)).filter(Order.status == "completed").scalar() or 0,
            "revenue": round(db.query(func.sum(Order.amount)).filter(Order.status == "completed").scalar() or 0, 2)
        },
        "stripe": {
            "total": db.query(func.count(StripePayment.id)).scalar() or 0,
            "volume": round(db.query(func.sum(StripePayment.amount)).filter(StripePayment.status == "succeeded").scalar() or 0, 2)
        },
        "github": {
            "total": db.query(func.count(GitHubIssue.id)).scalar() or 0,
            "open": db.query(func.count(GitHubIssue.id)).filter(GitHubIssue.state == "open").scalar() or 0
        },
        "weather": {
            "cities": db.query(func.count(func.distinct(WeatherData.city))).scalar() or 0,
            "readings": db.query(func.count(WeatherData.id)).scalar() or 0
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
