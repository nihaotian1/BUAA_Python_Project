import tkinter as tk
from tkcalendar import Calendar
# from datetime import datetime
# from ctrl.handler import handle
# from base.request import Command, Request
# from base.mission import Mission
# from database.db_handler import connect_db, close_db, init_db


class TaskDisplayApp:
    def select_date(self):
        # 当用户选择日期时，这个函数会被调用
        selected_date = self.cal.get_date()
        self.date_label.config(text=f"Selected Date: {selected_date}")

    def __init__(self, root):
        # 创建主窗口
        self.root = root
        self.root.title("主界面")

        # 设置窗口大小
        self.root.winfo_screenwidth()
        self.root.winfo_screenheight()
        self.root.geometry("1200x720")

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
        main_frame.columnconfigure(1, weight=2)  # 主界面内容区域占80%
        main_frame.columnconfigure(0, weight=1)  # 侧边栏占20%
        main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        # 在侧边栏添加一些内容
        self.create_sidebar(sidebar)

        # 在下边栏添加一些内容
        tk.Label(bottom_bar, text="").pack(fill='x')

        # 创建日历组件和相关控件
        self.calendar_frame = tk.Frame(self.content_area, padx=120, pady=45)
        self.calendar_frame.pack(side="top", fill="both", expand=True)

        self.cal = Calendar(self.calendar_frame, selectmode='day', year=2024, month=7, day=16)
        self.cal.pack(side="top", fill="both", pady=(0, 10))

        self.select_button = tk.Button(self.calendar_frame, text="Select Date", command=self.select_date)
        self.select_button.pack(side="top")
        self.date_label = tk.Label(self.calendar_frame, text="")
        self.date_label.pack(side="top")

        # 创建一个用于显示任务列表的 Listbox
        self.listbox = tk.Listbox(self.calendar_frame, bg="white")
        self.listbox.pack(side="bottom", fill="both", expand=True)

        # 在主界面内容区域添加一些内容
        tk.Label(self.content_area, text="欢迎使用！请点击侧边栏按钮查看任务日历系统", font=('华文行楷', 15)).pack(
            expand=True, fill='both')

    def __init__1(self, root):
        # 创建主窗口
        self.root = root
        self.root.title("主界面")

        # 设置窗口大小
        self.root.winfo_screenwidth()
        self.root.winfo_screenheight()
        self.root.geometry("1200x720")

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
        main_frame.columnconfigure(1, weight=2)  # 主界面内容区域占80%
        main_frame.columnconfigure(0, weight=1)  # 侧边栏占20%
        main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        # 在侧边栏添加一些内容
        self.create_sidebar(sidebar)

        # 在下边栏添加一些内容
        tk.Label(bottom_bar, text="下边栏").pack(fill='x')

        # 在主界面内容区域添加一些内容
        tk.Label(self.content_area, text="欢迎使用！请点击侧边栏按钮查看任务日历系统", font=('华文行楷', 15)).pack(expand=True, fill='both')

    def show_calendar1(self, tasks):
        self.listbox.delete(0, tk.END)

        for task in tasks:
            self.listbox.insert(tk.END, task)

    def show_calendar(self, tasks):
        # 清除任务列表
        self.listbox.delete(0, tk.END)

        # 更新任务列表
        for task in tasks:
            self.listbox.insert(tk.END, task)

        # 更改listbox中的字体
        self.listbox.config(font=("华文宋体", 12))  # 这里使用了华文宋体和字号12作为示例

    def show_calendar1(self, tasks):
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

        # 创建一个用于显示任务列表的Listbox
        listbox = tk.Listbox(self.content_area, bg="white")
        # listbox.grid(row=0, column=1, sticky="nsew")

        for task in tasks:
            listbox.insert(tk.END, task)
        listbox.pack()

    def create_sidebar(self, sidebar):
        def toggle_categories():
            if self.categories_frame.winfo_ismapped():  # 使用self.categories_frame
                self.categories_frame.grid_forget()
            else:
                self.categories_frame.grid(row=7, column=0, sticky="nsew")

        row_index = 7

        # 创建一个frame来容纳所有的类别按钮
        # 注意这里不需要重新定义categories_frame，而是使用在__init__中定义的那个
        tasks_uncategorized = ["任务甲", "任务乙", "任务丙"]
        uncategorized_button = tk.Button(self.categories_frame, text="未分类", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_uncategorized))
        uncategorized_button.grid(row=row_index, column=0, sticky="ew")
        row_index += 1

        tasks_work = ["任务甲", "任务乙", "任务丙"]
        work_button = tk.Button(self.categories_frame, text="工作", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_work))
        work_button.grid(row=row_index, column=0, sticky="ew")
        row_index += 1

        tasks_study = ["任务甲", "任务乙", "任务丙"]
        study_button = tk.Button(self.categories_frame, text="学习", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_study))
        study_button.grid(row=row_index, column=0, sticky="ew")
        row_index += 1

        tasks_contest = ["任务甲", "任务乙", "任务丙"]
        contest_button = tk.Button(self.categories_frame, text="竞赛", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_contest))
        contest_button.grid(row=row_index, column=0, sticky="ew")
        row_index += 1

        tasks_life = ["任务甲", "任务乙", "任务丙"]
        life_button = tk.Button(self.categories_frame, text="生活", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_life))
        life_button.grid(row=row_index, column=0, sticky="ew")
        row_index += 1

        tasks_long_term_planning = ["任务甲", "任务乙", "任务丙"]
        long_term_planning_button = tk.Button(self.categories_frame, text="长期规划", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_long_term_planning))
        long_term_planning_button.grid(row=row_index, column=0, sticky="ew")
        row_index += 1

        tasks_intemperance = ["任务甲", "任务乙", "任务丙"]
        intemperance_button = tk.Button(self.categories_frame, text="放纵", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_intemperance))
        intemperance_button.grid(row=row_index, column=0, sticky="ew")

        # 最初隐藏类别按钮
        self.categories_frame.pack_forget()

        # 添加一些垂直间距
        spacer_top = tk.Label(sidebar, text="", pady=10)
        spacer_top.grid(row=0, column=0)

        # 其他按钮保持不变
        tasks_day_todo = ["任务甲", "任务乙", "任务丙"]
        day_todo_button = tk.Button(sidebar, text="Day Todo", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_day_todo))
        day_todo_button.grid(row=1, column=0, sticky="ew")

        recent_tasks = ["任务甲", "任务乙", "任务丙"]
        recent_tasks_button = tk.Button(sidebar, text="最近待办", font=('华文行楷', 15), command=lambda: self.show_calendar(recent_tasks))
        recent_tasks_button.grid(row=2, column=0, sticky="ew")

        tasks_todo_box = ["任务甲", "任务乙", "任务丙"]
        todo_box_button = tk.Button(sidebar, text="待办箱", font=('华文行楷', 15), command=lambda: self.show_calendar(tasks_todo_box))
        todo_box_button.grid(row=4, column=0, sticky="ew")

        # 添加一些垂直间距
        spacer = tk.Label(sidebar, text="", pady=10)
        spacer.grid(row=5, column=0)

        # 创建“分类清单”按钮，点击时切换显示/隐藏类别按钮
        # 将其置于“待办箱”按钮下方，并与之保持一定距离
        categories_button = tk.Button(sidebar, text="分类清单", font=('华文行楷', 15), command=toggle_categories)
        categories_button.grid(row=6, column=0, sticky="ew")


def open_main_window():
    root = tk.Tk()
    app = TaskDisplayApp(root)
    root.mainloop()


open_main_window()

