from fastapi import FastAPI, WebSocket, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import asyncio
import json
from datetime import datetime

# Import dari file lokal kita
from database import SessionLocal, engine, Base
from models import AuditLog

# Inisialisasi database
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_dashboard(request: Request, db: Session = Depends(get_db)):
    # Mengambil log terakhir dari database untuk ditampilkan saat page load
    logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(10).all()
    return templates.TemplateResponse("dashboard.html", {"request": request, "logs": logs})

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # Menggunakan DB session lokal untuk WebSocket
    db = SessionLocal()
    try:
        while True:
            # Simulasi deteksi ancaman (Mock data)
            threat_data = {
                "time": datetime.now().strftime("%H:%M:%S"),
                "ip": "192.168.1.105",
                "lat": -6.2088,
                "lon": 106.8456,
                "threat": "CRITICAL"
            }
            
            # Simpan ke Database secara otomatis
            new_log = AuditLog(
                timestamp=threat_data["time"],
                ip_source=threat_data["ip"],
                threat_level=threat_data["threat"]
            )
            db.add(new_log)
            db.commit()
            
            # Kirim ke Frontend via WebSocket
            await websocket.send_json(threat_data)
            await asyncio.sleep(5)
    except Exception as e:
        print(f"Connection closed: {e}")
    finally:
        db.close()
