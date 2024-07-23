import tkinter as tk
from tkinter import messagebox
from GUI.WelcomeWindow import openWelcomeWindow
from ctrl.handler import handle
from base.request import Command,Request
from database.db_handler import init_db


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f'{width}x{height}+{x}+{y}')


class RegistrationWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('注册')
        self.master.geometry('400x300')  # 设定窗口大小
        center_window(self.master, 605, 400)  # 居中显示
        self.frame = tk.Frame(self.master)
        self.username_label = tk.Label(self.frame, text="用户名:")
        self.username_label.pack()
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.frame, text="密码:")
        self.password_label.pack()
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        self.register_button = tk.Button(self.frame, text="注册", command=self.register)
        self.register_button.pack()

        self.frame.pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        request = Request(req_type=Command.REGISTER_USER, user_name=username, user_password=password)
        ret = handle(request)
        if ret == "Successfully registered":
            messagebox.showinfo("成功", "注册成功！")
            self.master.destroy()  # 关闭注册窗口
        elif ret == "Invalid username or password":
            messagebox.showerror("错误", "密码至少八位")
        else:
            messagebox.showerror("错误", "未知错误。")


class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title('登录')
        self.master.geometry('400x250')  # 设定窗口大小
        center_window(self.master, 605, 400)  # 居中显示
        self.frame = tk.Frame(self.master)
        self.username_label = tk.Label(self.frame, text="用户名:", font=('华文行楷', 15))
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack()

        self.password_label = tk.Label(self.frame, text="密码:", font=('华文行楷', 15))
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self.frame, text="***** 登录 *****", command=self.login, font=('华文行楷', 20))
        self.login_button.pack(pady = 5)

        self.frame.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        request = Request(req_type=Command.LOG_IN, user_name=username, user_password=password)
        ret= handle(request)
        if ret == "User not found":
            messagebox.showerror("错误", "无效的用户名")
        elif ret == "Wrong password":
            messagebox.showerror("错误", "密码错误")
        else:
            messagebox.showinfo("成功", "登录成功！")
            self.master.destroy()  # 关闭登录窗口
            openWelcomeWindow(uid=ret,nickname=username)


def login_page():
    root = tk.Tk()
    root.title('任务管理器 - 登录/注册')

    # welcome_image
    canvas = tk.Canvas(root, height=157, width=605)
    image_file = tk.PhotoImage(file='登录页面欢迎图片.png')
    image = canvas.create_image(0, 0, anchor='nw', image=image_file)
    canvas.pack(side='top')

    # 创建并显示登录窗口
    login_window = LoginWindow(root)

    # 可选地，你可以创建一个菜单或按钮切换登录和注册
    # 为了简单起见，我们仅在需要时创建单独的注册窗口
    def open_registration_window():
        registration_window = tk.Toplevel(root)
        registration_window.title('任务管理器 - 注册')
        RegistrationWindow(registration_window)

    # 添加一个按钮从登录窗口打开注册窗口
    register_button = tk.Button(root, text="***** 注册 *****", command=open_registration_window, font=('华文行楷', 20))
    register_button.pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    init_db()
    login_page()

