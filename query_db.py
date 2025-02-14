import sqlite3

conn = sqlite3.connect('C:/Users/PHILHEALTH/Desktop/Try/OJT System/instance/users.db')  
cursor = conn.cursor()

cursor.execute("SELECT * FROM excel_file")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()

