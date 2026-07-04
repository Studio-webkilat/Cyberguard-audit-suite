from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class AdminUser(Base):
    __tablename__ = "admin_users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True) # Tambahan untuk administrasi
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow) # Sinkron dengan timestamp sistem

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String) # Sesuai dengan format WebSocket kita
    ip_source = Column(String)
    threat_level = Column(String)
