import sqlite3
from datetime import datetime

def check_user_logs():
    try:
        # Connect to the database
        conn = sqlite3.connect('user_log/user_data.db')
        cursor = conn.cursor()
        
        # Get all records
        cursor.execute('SELECT * FROM user_logs ORDER BY timestamp DESC')
        records = cursor.fetchall()
        
        print("\n=== รายงานข้อมูลผู้ใช้ ===\n")
        print(f"จำนวนการเข้าชมทั้งหมด: {len(records)} ครั้ง\n")
        
        # Print each record with Thai formatting
        for record in records:
            print(f"ลำดับที่: {record[0]}")
            print(f"เวลา: {record[1]}")
            print(f"เบราว์เซอร์: {record[2]}")
            print(f"ละติจูด: {record[3]}")
            print(f"ลองจิจูด: {record[4]}")
            print(f"ที่อยู่: {record[5]}")
            print("-" * 50)
        
        # Get statistics
        cursor.execute('SELECT COUNT(DISTINCT user_agent) FROM user_logs')
        unique_browsers = cursor.fetchone()[0]
        
        print(f"\nสถิติการใช้งาน:")
        print(f"- จำนวนเบราว์เซอร์ที่แตกต่างกัน: {unique_browsers}")
        print(f"- จำนวนการเข้าชมทั้งหมด: {len(records)}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"เกิดข้อผิดพลาดในการเชื่อมต่อฐานข้อมูล: {e}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    check_user_logs() 