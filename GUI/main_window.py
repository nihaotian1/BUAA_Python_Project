import tkinter as tk
from datetime import datetime
from ctrl.handler import handle
from base.request import Command, Request
from base.mission import Mission
from database.db_handler import connect_db, close_db, init_db


def create_sidebar(sidebar, content_area):
    def toggle_categories():
        if categories_frame.winfo_ismapped():  # 如果类别已经显示，则隐藏
            categories_frame.pack_forget()
        else:  # 如果类别隐藏，则显示
            categories_frame.pack(side="top", fill="x")

    # 创建一个frame来容纳所有的类别按钮
    categories_frame = tk.Frame(sidebar)

    # 创建所有类别的按钮并放入categories_frame中
    categories = ["未分类", "工作", "学习", "竞赛", "生活", "长期规划", "放纵"]
    for category in categories:
        button = tk.Button(categories_frame, text=category, command=lambda cat=category: print(cat))
        button.pack(side="top", fill="x")

    # 最初隐藏类别按钮
    categories_frame.pack_forget()

    # 其他按钮保持不变
    day_todo_button = tk.Button(sidebar, text="Day Todo", command=lambda: print("Day Todo"))
    day_todo_button.pack(side="top", fill="x")

    recent_tasks_button = tk.Button(sidebar, text="最近待办", command=lambda: print("最近待办"))
    recent_tasks_button.pack(side="top", fill="x")

    todo_box_button = tk.Button(sidebar, text="待办箱", command=lambda: print("待办箱"))
    todo_box_button.pack(side="top", fill="x")

    # 添加一些垂直间距
    spacer = tk.Label(sidebar, text="", pady=10)  # pady设置间距大小
    spacer.pack(side="top", fill="x")

    # 创建“分类清单”按钮，点击时切换显示/隐藏类别按钮
    # 将其置于“待办箱”按钮下方，并与之保持一定距离
    categories_button = tk.Button(sidebar, text="分类清单", command=toggle_categories)
    categories_button.pack(side="top", fill="x")


class TaskDisplayApp:

    def __init__(self, root):
        # 创建主窗口
        self.root = root
        self.root.title("主界面")

        # 设置窗口大小
        self.root.winfo_screenwidth()
        self.root.winfo_screenheight()
        self.root.geometry("1200x800")

        # 创建一个主框架，用于放置其他组件
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建侧边栏和主界面内容区域
        sidebar = tk.Frame(main_frame)
        content_area = tk.Frame(main_frame)
        sidebar.grid(row=0, column=0, sticky="ns")
        content_area.grid(row=0, column=1, sticky="nsew")

        # 创建下边栏
        bottom_bar = tk.Frame(main_frame)
        bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        # 创建一个用于绘制分隔线的Canvas
        canvas = tk.Canvas(main_frame, bg="white")
        canvas.grid(row=0, column=1, sticky="nsew")

        # 调整列权重，使得主界面内容区域比侧边栏宽
        main_frame.columnconfigure(1, weight=4)  # 主界面内容区域占80%
        main_frame.columnconfigure(0, weight=1)  # 侧边栏占20%
        main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        # 在侧边栏添加一些内容
        create_sidebar(sidebar, content_area)

        # 在下边栏添加一些内容
        tk.Label(bottom_bar, text="下边栏").pack(fill='x')

        # 在主界面内容区域添加一些内容
        tk.Label(content_area, text="主界面").pack(expand=True, fill='both')


def open_main_window():
    root = tk.Tk()
    app = TaskDisplayApp(root)
    root.mainloop()


open_main_window()



