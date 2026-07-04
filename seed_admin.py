from database import SessionLocal, engine, Base
from models import AdminUser
from security import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()
if not db.query(AdminUser).filter(AdminUser.username == "komandan").first():
    db.add(AdminUser(username="komandan", hashed_password=get_password_hash("GantiPasswordKuat123!")))
    db.commit()
    print("Admin 'komandan' berhasil diinisialisasi.")
db.close()
