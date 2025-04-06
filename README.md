# Find Food to Eat - ร้านอาหารใกล้คุณ

เว็บแอปพลิเคชันสำหรับค้นหาร้านอาหารใกล้เคียง โดยใช้ตำแหน่งปัจจุบันของผู้ใช้

## คุณสมบัติ

- ค้นหาร้านอาหารใกล้เคียงโดยอัตโนมัติ
- แสดงข้อมูลร้านอาหาร เช่น ชื่อ, คะแนน, ที่อยู่
- แสดงรูปภาพร้านอาหาร
- นำทางไปยังร้านอาหารผ่าน Google Maps
- ระบบติดตามผู้ใช้งาน (Admin Panel)
- แสดงชื่อเครื่องของผู้ใช้งาน

## เทคโนโลยีที่ใช้

- Python Flask
- SQLite Database
- Google Places API
- Google Maps API
- HTML/CSS/JavaScript
- Font Awesome Icons
- Google Fonts (Kanit)

## การติดตั้ง

1. Clone repository:
```bash
git clone https://github.com/yourusername/find-food-to-eat.git
cd find-food-to-eat
```

2. สร้าง virtual environment และติดตั้ง dependencies:
```bash
python -m venv venv
source venv/bin/activate  # สำหรับ Linux/Mac
venv\Scripts\activate     # สำหรับ Windows
pip install -r requirements.txt
```

3. สร้างไฟล์ .env และกำหนดค่า API key:
```
GOOGLE_API_KEY=your_google_api_key_here
```

4. รันแอปพลิเคชัน:
```bash
python app.py
```

## การ Deploy

### Render

1. สร้างบัญชี Render (https://render.com)
2. สร้าง Web Service ใหม่
3. เชื่อมต่อกับ GitHub repository
4. กำหนดค่าดังนี้:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. เพิ่ม Environment Variables:
   - GOOGLE_API_KEY
6. Deploy

## โครงสร้างโปรเจค

```
find-food-to-eat/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── .env               # Environment variables
├── README.md          # Project documentation
├── templates/         # HTML templates
│   ├── index.html     # Main page
│   └── admin.html     # Admin dashboard
└── user_log/          # User data logs
    └── user_data.db   # SQLite database
```

## การใช้งาน

1. เข้าถึงเว็บไซต์ผ่าน URL ที่กำหนด
2. อนุญาตการเข้าถึงตำแหน่งเมื่อเบราว์เซอร์ขอ
3. ระบบจะแสดงรายการร้านอาหารใกล้เคียงโดยอัตโนมัติ
4. คลิกปุ่ม "นำทาง" เพื่อดูเส้นทางไปยังร้านอาหาร

## Admin Panel

เข้าถึงหน้า Admin ได้ที่ `/admin` เพื่อดูข้อมูลผู้ใช้งาน:
- จำนวนการเข้าชมทั้งหมด
- จำนวนเบราว์เซอร์ที่แตกต่างกัน
- การเข้าชมล่าสุด
- รายละเอียดผู้ใช้งานแต่ละราย

## License

MIT License 