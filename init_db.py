# initialize_db.py
import sqlite3

conn = sqlite3.connect('app.db')
c = conn.cursor()

# Create User table
c.execute('''
CREATE TABLE IF NOT EXISTS Users (
  id_user INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('user', 'admin', 'super-admin'))
);
''')

# Create Blocked IP table
c.execute('''
CREATE TABLE IF NOT EXISTS BlockedIPs (
  id_ip INTEGER PRIMARY KEY AUTOINCREMENT,
  ip_address TEXT UNIQUE NOT NULL,
  timestamp DATETIME NOT NULL       
);
''')

conn.commit()
conn.close()