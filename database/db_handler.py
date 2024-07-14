# db_handler.py
import sqlite3
from datetime import datetime

from base.mission import Mission


def init_db():
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

    # 提交事务并关闭连接
    conn.commit()
    conn.close()

def connect_db():
    return sqlite3.connect('todo.db')

def close_db(conn):
    conn.close()

'''
上面两个是关于数据库链接相关的，一个打开一个关闭
分别写在程序开头和结尾
'''

'''
    用于注册用户
    注册示例：
    if register_user("new_user", "password"):
        print("User registered successfully.")
    else:
        print("Username already exists.")
        
    输入：
    username:str
    password:str
    
    return: bool
'''
def register_user(username, password):
    with connect_db() as conn:
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

'''
    用于更新用户数据
    示例：
    update_user(1, username="updated_username", password="new_password")
    
    输入:
    user_id:int
    username:str
    password:str
    
    输出：
    return: void
'''
def update_user(user_id, username=None, password=None):
    with connect_db() as conn:
        c = conn.cursor()
        if username:
            c.execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))
        if password:
            c.execute("UPDATE users SET password = ? WHERE id = ?", (password, user_id))
        conn.commit()


'''
    用于获取用户密码
    示例：
    ef login():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    user_info = get_user_info(username)

    if user_info and user_info[2] == password:
        print("Login successful.")
        return user_info[0]  # 返回用户ID
    else:
        print("Invalid username or password.")
        return None
        
    输入：     
    username:str
    输出：
    password：str
'''
def get_user_info(username):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        return c.fetchone()

'''
    用于添加事件
    示例：
    add_task(1, "New task", "2023-04-15", duration=2, task_type="urgent", weight=2.0, is_daily=True)
    输入：
    所有的输入类型与mission一致
    输出
    void
'''
def add_task(user_id, name, due_date, duration=1, task_type='default', weight=1.0, is_daily=False):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO tasks (uid, name, due_date, duration, type, weight, is_daily) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (user_id, name, due_date, duration, task_type, weight, int(is_daily)))
        conn.commit()


'''
    删除事件
    示例：
    delete_task(1)
    输入：
    id：（mid）int
    输出：
    viod
'''
def delete_task(task_id):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

'''
    更新事件
    示例：
    update_task(2, name="Updated task name", due_date="2023-04-20")
    输入：
    与mission保持一致
    输出：
    void
'''
# 在 db_handler.py 中
def update_task(task_id, name=None, due_date=None, duration=None, task_type=None, weight=None, is_daily=None):
    updates = []
    params = [task_id]

    if name is not None:
        updates.append("name = ?")
        params.insert(0, name)

    if due_date is not None:
        updates.append("due_date = ?")
        params.insert(0, due_date)

    if duration is not None:
        updates.append("duration = ?")
        params.insert(0, duration)

    if task_type is not None:
        updates.append("type = ?")
        params.insert(0, task_type)

    if weight is not None:
        updates.append("weight = ?")
        params.insert(0, weight)

    if is_daily is not None:
        updates.append("is_daily = ?")
        params.insert(0, int(is_daily))

    if updates:
        query = "UPDATE tasks SET {} WHERE id = ?".format(", ".join(updates))

        with connect_db() as conn:
            c = conn.cursor()
            c.execute(query, params)
            conn.commit()

'''
    查询，获取过期事件表
    示例：
    expired_tasks = get_expired_tasks()
    for task in expired_tasks:
        print(task)
        
    输入：用户id uid：int
    输出    mission类型的列表
    
'''
def get_expired_tasks(uid):
    today = datetime.now().strftime("%Y-%m-%d")
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE due_date <= ? AND uid = ?", (today, uid))
        rows = c.fetchall()
        return [mission_from_row(row) for row in rows]


'''
    查询，全部事件表
    示例：
    all_tasks = get_all_tasks(uid)
    for task in all_tasks:
        print(task)

    输入：用户id uid：int
    输出    mission类型的列表

'''
def get_all_tasks(uid):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE uid = ?", (uid,))
        rows = c.fetchall()
        return [mission_from_row(row) for row in rows]

'''
    查询，特定日期前事件表
    
    输入：用户id uid：int 
    due_date : datetime
    输出    mission类型的列表

'''
def find_tasks_by_due_date(due_date, uid):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM tasks WHERE due_date = ? AND uid = ?", (due_date, uid))
        rows = c.fetchall()
        return [mission_from_row(row) for row in rows]

'''
    用于检查是否存在这一id对应的事件
    输入：task_id: int
    输出：bool
'''
def task_exists(task_id):
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM tasks WHERE id = ?", (task_id,))
        result = c.fetchone()[0]
        return result > 0

'''
    内部自用小函数，莫管
    用来转化输出类型
'''
def mission_from_row(row):
    return Mission(
        row[1],  # uid
        row[2],  # name
        row[3],  # due_date
        row[0],  # mid
        row[4],  # duration
        row[5],  # type
        row[6],  # weight
        bool(row[7]),  # is_daily
        bool(row[8])   # complete
    )