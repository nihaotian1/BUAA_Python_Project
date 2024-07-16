import tkinter as tk
from tkinter import Listbox, END, ttk, StringVar, Entry, Button, Label, Frame
from datetime import datetime
from ctrl.handler import handle
from base.request import Command,Request
from base.mission import Mission
from database.db_handler import connect_db, close_db, init_db
from GUI.SequenceDiagram import createEditWindowAndReturn



class RootWindow(tk.Frame): # 开始界面
    def __init__(self, root,app=None):
        if app is None: # 第一次打开界面，需要初始化
            self.uid = -1
            if(self.uid == -1):
                self.sign_in()
            self.root = root
            self.root.title("Welcome to Mission Planner" + self.nickname)
            self.root.geometry("1200x720+150+0")  # 扩大视图界面

            # 创建UI框架
            self.setup_side_buttom()
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
            self.root.title("Welcome to Mission Planner" + self.nickname)
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



        # 在主界面内容区域添加一些内容
        tk.Label(self.content_area, text="主界面").pack(expand=True, fill='both')

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
        self.nickname = " "
        pass

    def sign_up(self): # 注册界面
        pass

    def sign_out(self): # 登出界面
        pass

    def close_app(self):
        self.content_area.destroy()


def openWelcomeWindow(app=None):
    init_db()  # 初始化数据库
    if app:
        newAPP = RootWindow(app.root,app)
        app.root.mainloop()
    else: # 第一次打开界面
        root = tk.Tk()
        newAPP = RootWindow(root)
        root.mainloop()


if __name__ == '__main__':
    openWelcomeWindow()