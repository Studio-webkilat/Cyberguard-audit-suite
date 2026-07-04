from database import SessionLocal, engine, Base
from models import AdminUser, AuditLog  # Sinkronisasi dengan model baru
from security import get_password_hash
from datetime import datetime

# Inisialisasi struktur database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

try:
    # 1. Inisialisasi Akun Admin
    if not db.query(AdminUser).filter(AdminUser.username == "komandan").first():
        admin = AdminUser(
            username="komandan", 
            hashed_password=get_password_hash("GantiPasswordKuat123!")
        )
        db.add(admin)
        print("[SYSTEM] Admin 'komandan' berhasil diinisialisasi.")

    # 2. Inisialisasi Log Awal (Modul Baru: Audit Seed)
    # Memastikan dashboard tidak kosong saat pertama kali akses
    if not db.query(AuditLog).first():
        init_log = AuditLog(
            timestamp=datetime.now().strftime("%H:%M:%S"),
            ip_source="SYSTEM_INITIALIZED",
            threat_level="INFO"
        )
        db.add(init_log)
        print("[SYSTEM] Audit log baseline berhasil dibuat.")

    db.commit()

except Exception as e:
    print(f"[ERROR] Inisialisasi gagal: {e}")
    db.rollback()
finally:
    db.close()
