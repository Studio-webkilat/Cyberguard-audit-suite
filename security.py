import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError # Menggunakan library jose yang tepat

# Konfigurasi Enkripsi
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Menggunakan Environment Variable untuk keamanan (PENTING untuk Railway)
SECRET_KEY = os.getenv("SECRET_KEY", "SCOC_SECRET_KEY_V2_CHANGE_ME_IN_PRODUCTION")
ALGORITHM = "HS256"

# 1. Fungsi Hash Password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# 2. Fungsi Verifikasi Password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# 3. Tokenizer untuk Sesi Admin (Zero Trust Access)
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 4. Validasi Scanner API Key
def validate_scanner_key(api_key: str) -> bool:
    # Dalam produksi, pindahkan ke database atau env variable
    VALID_KEYS = [os.getenv("SCANNER_API_KEY",)]
    return api_key in VALID_KEYS

# 5. Tambahan: Fungsi Decode Token (Untuk proteksi rute)
def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
