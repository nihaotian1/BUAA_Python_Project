import tkinter as tk
from tkcalendar import Calendar
#from datetime import datetime
#from ctrl.handler import handle
#from base.request import Command, Request
#from base.mission import Mission
#from database.db_handler import connect_db, close_db, init_db


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
        self.content_area = tk.Frame(main_frame)
        sidebar.grid(row=0, column=0, sticky="ns")
        self.content_area.grid(row=0, column=1, sticky="nsew")

        # 初始化categories_frame，确保它可以在整个类中被引用
        self.categories_frame = tk.Frame(sidebar)

        # 创建下边栏
        bottom_bar = tk.Frame(main_frame)
        bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        # 调整列权重，使得主界面内容区域比侧边栏宽
        main_frame.columnconfigure(1, weight=4)  # 主界面内容区域占80%
        main_frame.columnconfigure(0, weight=1)  # 侧边栏占20%
        main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        # 在侧边栏添加一些内容
        self.create_sidebar(sidebar)

        # 在下边栏添加一些内容
        tk.Label(bottom_bar, text="下边栏").pack(fill='x')

        # 在主界面内容区域添加一些内容
        tk.Label(self.content_area, text="主界面").pack(expand=True, fill='both')

    def display_task_list(self, tasks):
        """在主界面显示任务列表"""
        # 清除之前的内容
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # 创建一个用于显示任务列表的Listbox
        listbox = tk.Listbox(self.content_area, bg="white")
        listbox.grid(row=0, column=1, sticky="nsew")

        for task in tasks:
            listbox.insert(tk.END, task)
        listbox.pack(side="top", fill='both')


    def show_calendar(self):
        def select_date():
            # 当用户选择日期时，这个函数会被调用
            selected_date = cal.get_date()
            date_label.config(text=f"Selected Date: {selected_date}")

        for widget in self.content_area.winfo_children():
            widget.destroy()

        cal = Calendar(self.content_area, selectmode='day', year=2024, month=7, day=16)
        cal.pack(side="top", fill="both", pady=20)

        # 添加一个按钮用于获取选中的日期
        select_button = tk.Button(self.content_area, text="Select Date", command=select_date)
        select_button.pack()

        date_label = tk.Label(self.content_area, text="")
        date_label.pack()

        tasks = ["任务甲", "任务乙", "任务丙"]
        # 创建一个用于显示任务列表的Listbox
        listbox = tk.Listbox(self.content_area, bg="white")
        # listbox.grid(row=0, column=1, sticky="nsew")

        for task in tasks:
            listbox.insert(tk.END, task)
        listbox.pack()

    def recently_to_be_done_list(self):
        task = ["庚"]
        self.display_task_list(task)

    def todo_box(self):
        task = ["辛"]
        self.display_task_list(task)

    def create_sidebar(self, sidebar):
        def uncategorized_list():
            task = ["甲", "乙", "丙", "丁", "戊", "己"]
            self.display_task_list(task)

        def work_list():
            task = ["甲"]
            self.display_task_list(task)

        def study_list():
            task = ["乙"]
            self.display_task_list(task)

        def life_list():
            task = ["丙"]
            self.display_task_list(task)

        def contest_list():
            task = ["丁"]
            self.display_task_list(task)

        def long_term_planning_list():
            task = ["戊"]
            self.display_task_list(task)

        def intemperance_list():
            task = ["己"]
            self.display_task_list(task)

        def toggle_categories():
            if self.categories_frame.winfo_ismapped():  # 使用self.categories_frame
                self.categories_frame.pack_forget()
            else:
                self.categories_frame.pack(side="top", fill="x")

        # 创建一个frame来容纳所有的类别按钮
        # 注意这里不需要重新定义categories_frame，而是使用在__init__中定义的那个
        uncategorized_button = tk.Button(self.categories_frame, text="未分类", command=uncategorized_list)
        uncategorized_button.pack(side="top", fill="x")

        work_button = tk.Button(self.categories_frame, text="工作", command=work_list)
        work_button.pack(side="top", fill="x")

        study_button = tk.Button(self.categories_frame, text="学习", command=study_list)
        study_button.pack(side="top", fill="x")

        contest_button = tk.Button(self.categories_frame, text="竞赛", command=contest_list)
        contest_button.pack(side="top", fill="x")

        life_button = tk.Button(self.categories_frame, text="生活", command=life_list)
        life_button.pack(side="top", fill="x")

        long_term_planning_button = tk.Button(self.categories_frame, text="长期规划", command=long_term_planning_list)
        long_term_planning_button.pack(side="top", fill="x")

        intemperance_button = tk.Button(self.categories_frame, text="放纵", command=intemperance_list)
        intemperance_button.pack(side="top", fill="x")

        # 最初隐藏类别按钮
        self.categories_frame.pack_forget()

        # 其他按钮保持不变
        day_todo_button = tk.Button(sidebar, text="Day Todo", command=self.show_calendar)
        day_todo_button.pack(side="top", fill="x")

        recent_tasks_button = tk.Button(sidebar, text="最近待办", command=self.recently_to_be_done_list)
        recent_tasks_button.pack(side="top", fill="x")

        todo_box_button = tk.Button(sidebar, text="待办箱", command=self.todo_box)
        todo_box_button.pack(side="top", fill="x")

        # 添加一些垂直间距
        spacer = tk.Label(sidebar, text="", pady=10)
        spacer.pack(side="top", fill="x")

        # 创建“分类清单”按钮，点击时切换显示/隐藏类别按钮
        # 将其置于“待办箱”按钮下方，并与之保持一定距离
        categories_button = tk.Button(sidebar, text="分类清单", command=toggle_categories)
        categories_button.pack(side="top", fill="x")


def open_main_window():
    root = tk.Tk()
    app = TaskDisplayApp(root)
    root.mainloop()


open_main_window()


