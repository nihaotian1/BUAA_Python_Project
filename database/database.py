import sqlite3
from getpass import getpass

# 连接到SQLite数据库
conn = sqlite3.connect('todo.db')
c = conn.cursor()

# 创建用户表
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             username TEXT UNIQUE NOT NULL,
             password TEXT NOT NULL)''')

# 创建任务表
c.execute('''CREATE TABLE IF NOT EXISTS tasks (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             uid INTEGER NOT NULL,
             name TEXT NOT NULL,
             due_date TEXT NOT NULL,
             duration INTEGER DEFAULT 1,
             type TEXT DEFAULT 'default',
             weight REAL DEFAULT 1.0,
             is_daily INTEGER DEFAULT 0,
             complete INTEGER DEFAULT 0,
             FOREIGN KEY(uid) REFERENCES users(id))''')

conn.commit()