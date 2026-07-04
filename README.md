# Cyberguard Audit Suite (SCOC V2.0)

Sistem Operasi Pusat Keamanan (SCOC) untuk pemantauan deteksi ancaman *real-time*.

## Fitur Utama
- **Real-time Threat Monitoring:** Deteksi ancaman jaringan dengan WebSocket.
- **Cyberpunk UI:** Antarmuka responsif berbasis *Zero Trust*.
- **Automated Logging:** Pencatatan otomatis ke database melalui modul scanner.
- **Secure Access:** Proteksi admin dengan sistem enkripsi Bcrypt & JWT.

## Setup
1. Clone repositori ini.
2. Buat `.env` berdasarkan `.env.example`.
3. Jalankan `pip install -r requirements.txt`.
4. Jalankan `python seed_admin.py` untuk inisialisasi admin.
5. Jalankan aplikasi dengan `uvicorn main:app --reload`.

## Lisensi
Proyek ini dilindungi oleh lisensi MIT.
# Cyberguard-audit-suite
