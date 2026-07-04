from fastapi import FastAPI, WebSocket, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import asyncio

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        # Mock data untuk simulasi serangan
        await websocket.send_json({"time": "2026-07-03", "ip": "192.168.1.1", "lat": -6.2, "lon": 106.8})
        await asyncio.sleep(5)
