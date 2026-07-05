import asyncio
import random
import os
from datetime import datetime
from database import SessionLocal
from models import AuditLog

# Daftar simulasi ancaman
THREAT_TYPES = ["SQLi_ATTEMPT", "BRUTE_FORCE", "XSS_INJECTION", "MALWARE_SCAN"]
IP_POOL = ["192.168.1.105", "45.76.12.3", "103.24.1.99", "185.12.33.4"]

async def run_scanner():
    """
    Modul Scanner: Deteksi ancaman dan logging otomatis ke database.
    Berjalan di background sebagai asyncio task.
    """
    print("[SYSTEM] Scanner online. Memulai pemindaian jaringan...")
    
    while True:
        # Probabilitas deteksi ancaman (30% setiap 10 detik)
        if random.random() > 0.7:
            db = SessionLocal()
            try:
                new_threat = AuditLog(
                    timestamp=datetime.now().strftime("%H:%M:%S"),
                    ip_source=random.choice(IP_POOL),
                    threat_level=random.choice(THREAT_TYPES)
                )
                db.add(new_threat)
                db.commit()
                print(f"[ALERT] Ancaman terdeteksi: {new_threat.threat_level} dari {new_threat.ip_source}")
            except Exception as e:
                print(f"[ERROR] Gagal mencatat ancaman: {e}")
            finally:
                db.close()
        
        # Jeda scan agar tidak membebani CPU (10 detik)
        await asyncio.sleep(10)
