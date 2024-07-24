import tkinter as tk
from tkinter import Listbox, END, ttk, StringVar, Entry, Button, Label, Frame
from datetime import datetime
from ctrl.handler import handle
from base.request import Command,Request
from base.mission import Mission
from database.db_handler import connect_db, close_db, init_db
from GUI.SequenceDiagram import createEditWindowAndReturn




class RootWindow(tk.Frame): # 开始界面
    def __init__(self, root=None,app=None,uid= None,nickname=None):
        if app is None: # 第一次打开界面，需要初始化
            self.uid = uid
            self.nickname = nickname
            if(self.uid == -1):
                self.sign_in()
            self.root = root
            self.root.title("Welcome to Mission Planner" + str(self.nickname))
            self.root.geometry("1200x720+150+0")  # 扩大视图界面
            top_menu = tk.Menu(self.root,bg="gray")
            top_menu.add_command(label="登出并退出", command=self.sign_out)
            self.root.config(menu=top_menu)
            top_menu.add_command(label="帮助", command=self.help_for_user)



            # 创建UI框架
            self.setup_side_buttom()
            self.setup_content_area()


        else: # 已经打开过界面，不需要初始化
            # 继承上一级数据
            self.uid = app.uid
            self.nickname = app.nickname
            self.root = app.root
            self.main_frame = app.main_frame
            self.content_area = app.content_area
            self.start_button = app.start_button
            self.overview_button = app.overview_button
            self.edit_button = app.edit_button

            # 修改上一级数据
            self.content_area.destroy()  # 销毁原来的内容区域，注意所有不能留给下一界面的组件都需要放在这里，因为只摧毁它
            self.root.title("Welcome to Mission Planner" + str(self.nickname))
            self.root.geometry("1200x720+150+0")  # 扩大视图界面

            # 修改按钮颜色  注意指令始终不变，否则会导致import循环依赖，造成死锁
            self.start_button["bg"] = "DarkGray"
            self.overview_button["bg"] = "white"
            self.edit_button["bg"] = "white"

            # 恢复框架结构 ，只摧毁了content_area
            self.content_area = tk.Frame(self.main_frame)
            self.content_area.grid(row=0, ipadx=1, ipady=1, sticky="nsew")

            self.main_frame.columnconfigure(0, weight=1)
            self.main_frame.columnconfigure(1, weight=0)
            self.main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
            self.main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

            # 编辑主界面

            self.setup_content_area()




    def setup_side_buttom(self):
        # 设置窗口大小
        self.root.winfo_screenwidth()
        self.root.winfo_screenheight()

        # 创建一个主框架，用于放置其他组件
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建下边栏
        self.content_area = tk.Frame(self.main_frame)
        self.content_area.grid(row=0,ipadx=1, ipady=1, sticky="nsew")
        bottom_bar = tk.Frame(self.main_frame, bg="lightgray")
        bottom_bar.grid(row=1, sticky="ew")

        # 调整列权重，使得主界面内容区域比侧边栏宽
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        self.main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        # 在下边栏添加一些内容
        # 创建一个文本标签（如果需要的话）
        status_label = tk.Label(bottom_bar, text="视图切换：")
        status_label.pack(side=tk.LEFT, fill=tk.X, pady=5)

        # 在bottom_bar中创建按钮
        self.start_button = tk.Button(bottom_bar, text="开始",command = self.bit_to_start,bg= "DarkGray")
        self.start_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.overview_button = tk.Button(bottom_bar, text="总览",command=self.bit_to_main)
        self.overview_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.edit_button = tk.Button(bottom_bar, text="编辑",command=self.bit_to_edit)
        self.edit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)



    def setup_content_area(self):
        # 在主界面内容区域添加一些内容

        text_frame = tk.Frame(self.content_area)
        text_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(text_frame, text="你好，" + str(self.nickname)+ "!\n"+"欢迎使用任务管理系统", font=("华文行楷", 20)).pack()
        tk.Label(text_frame, text="点击编辑调整你的任务，点击总览查看具体信息").pack()

        today_text_frame = tk.Frame(self.content_area)
        today_text_frame.pack(fill=tk.BOTH, expand=True)

        self.task_list_frame = Frame(self.content_area, width=100, height=500, bg="white")
        self.task_list_frame.pack(pady=20)
        self.task_list = Listbox(self.task_list_frame, width=50, height=20, font=("微软雅黑", 14))
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.update_today_task()

        if self.num_yellow == 0 and self.num_green == 0:
            tk.Label(today_text_frame, text="你今天没有任务哦：\n快去点击下方的编辑按钮添加任务吧！", font=("微软雅黑", 14)).pack()
        elif self.num_yellow == 0:
            tk.Label(today_text_frame, text="你今天的任务全部完成了哦：\n真棒！", font=("微软雅黑", 14)).pack()
        elif self.num_green == 0:
            tk.Label(today_text_frame, text="今日任还没有完成任务哦：\n加油！", font=("微软雅黑", 14)).pack()
        else:
            tk.Label(today_text_frame, text="今日你已经完成"+ str(self.num_green)+"个任务\n还有"\
                                            +str(self.num_yellow)+"个任务未完成：\n加油!", font=("微软雅黑", 14)).pack()


    def update_today_task(self):
        self.task_list.delete(0, END)

        req = Request(Command.GET_ALL, self.uid)
        tasks = handle(req)

        self.num_yellow = 0
        self.num_green = 0
        for mission in tasks:
            try:
             due = datetime.strptime(mission.due, "%Y-%m-%d")  # 返回datetime对象
             due = due.date()  # 取出datetime里的date部分
            except:
                continue
            if due > datetime.now().date():
                continue
            elif due < datetime.now().date():
                break
            elif mission.complete:
                status_color = 'green'
                staus_str = '已完成'
                self.num_green += 1
            else:
                status_color = 'yellow'
                staus_str = '正在进行'
                self.num_yellow += 1

            deadline_str = mission.due
            if staus_str == '已完成':
                task_str = f"{mission.name} - {staus_str}"
            else:
                task_str = f"{mission.name} - {staus_str} (截止: {deadline_str})"
            self.task_list.insert(END, task_str)
            self.task_list.itemconfig(END, bg=status_color)



    def bit_to_edit(self):
        print("want from start to edit")
        createEditWindowAndReturn(self)
        print("sussess to edit")

    def bit_to_start(self):
        openWelcomeWindow(self)


    def bit_to_main(self):
        print("want from start to main")
        # self.close_app()
        # main_window.open_main_window()

    def sign_in(self): # 登录界面
        self.uid = -1
        self.nickname = "游客朋友"
        pass


    def sign_up(self): # 注册界面
        pass

    def sign_out(self): # 登出界面
        top = tk.Toplevel(self.root)
        top.geometry("300x150+600+300")
        top.title("确认退出")
        tk.Label(top, text="确认退出登录？\n这会关闭APP\n你需要重新点击APP登录", font=("微软雅黑", 14)).pack()
        button_frame = tk.Frame(top)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="确认",bg="red", command=self.root.destroy).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(button_frame, text="取消", command=top.destroy).grid(row=0, column=1, padx=10, pady=10)

    def close_app(self):
        self.content_area.destroy()

    def help_for_user(self):
        pass


def openWelcomeWindow(app=None,uid = None, nickname = None):
    init_db()  # 初始化数据库
    if app:
        newAPP = RootWindow(root=app.root,app=app)
        app.root.mainloop()
    else: # 第一次打开界面
        root = tk.Tk()
        newAPP = RootWindow(root=root,uid=uid,nickname=nickname)
        root.mainloop()


if __name__ == '__main__':
    openWelcomeWindow(uid=-1,nickname="游客朋友")