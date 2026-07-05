from fastapi import FastAPI, WebSocket, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import asyncio
import os

from database import SessionLocal, engine, Base
from models import AuditLog
from scanner import run_scanner # Import modul scanner kita

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Mengaktifkan Scanner di Background saat App Startup
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_scanner())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(10).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs})

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        while True:
            # Mengambil data terbaru dari DB untuk dikirim ke UI
            latest_logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(5).all()
            data = [{"time": log.timestamp, "ip": log.ip_source, "threat": log.threat_level} for log in latest_logs]
            
            await websocket.send_json(data)
            await asyncio.sleep(5)
    except Exception as e:
        print(f"WS Error: {e}")
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
