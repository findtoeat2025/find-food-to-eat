import sqlite3
from datetime import datetime

def check_user_data():
    try:
        # Connect to the database
        conn = sqlite3.connect('user_log/user_data.db')
        cursor = conn.cursor()
        
        # Get all records
        cursor.execute('SELECT * FROM user_logs ORDER BY timestamp DESC')
        records = cursor.fetchall()
        
        print("\n=== User Activity Log ===\n")
        print(f"Total records: {len(records)}\n")
        
        # Print each record
        for record in records:
            print(f"ID: {record[0]}")
            print(f"Timestamp: {record[1]}")
            print(f"User Agent: {record[2]}")
            print(f"Latitude: {record[3]}")
            print(f"Longitude: {record[4]}")
            print(f"Address: {record[5]}")
            print("-" * 50)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_user_data() 