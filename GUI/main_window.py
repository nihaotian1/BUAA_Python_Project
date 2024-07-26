import tkinter as tk
from tkcalendar import Calendar


# from datetime import datetime
# from ctrl.handler import handle
# from base.request import Command, Request
# from base.mission import Mission
# from database.db_handler import connect_db, close_db, init_db


class TaskDisplayApp:
    def __init__(self, app=None):
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
        self.root.title("任务日历系统")
        self.root.geometry("1200x720+150+0")  # 扩大视图界面

        # 修改按钮颜色  注意不能修改指令，否则会导致循环依赖import，导致死锁！！！！！！！！！！！！
        self.start_button["bg"] = "white"
        self.overview_button["bg"] = "DarkGray"
        self.edit_button["bg"] = "white"

        # 恢复框架结构 ，只摧毁了content_area
        self.content_area = tk.Frame(self.main_frame)
        self.content_area.grid(row=0, ipadx=1, ipady=1, sticky="nsew")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        self.main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        self.create_addition()

    def create_addition(self):
        def select_date():
            # 当用户选择日期时，这个函数会被调用
            selected_date = self.cal.get_date()
            self.date_label.config(text=f"Selected Date: {selected_date}")

        sidebar = tk.Frame(self.content_area)
        # sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.place(x=100, y=10, width=100, height=500)

        self.content_right_area = tk.Frame(self.content_area)
        # self.content_right_area.grid(row=0, column=3, sticky="nsew")
        self.content_right_area.place(x=200, y=10, width=1000, height=500)

        # 初始化categories_frame，确保它可以在整个类中被引用
        self.categories_frame = tk.Frame(sidebar)

        # 创建日历组件和相关控件
        self.calendar_frame = tk.Frame(self.content_right_area, padx=120, pady=45)
        self.calendar_frame.pack(side="top", fill="both", expand=True)

        self.cal = Calendar(self.calendar_frame, selectmode='day', year=2024, month=7, day=16)
        self.cal.pack(side="top", fill="both", pady=(0, 10))

        self.select_button = tk.Button(self.calendar_frame, text="Select Date", command=select_date)
        self.select_button.pack(side="top")
        self.date_label = tk.Label(self.calendar_frame, text="未选择")
        self.date_label.pack(side="top")

        # 创建一个用于显示任务列表的 Listbox
        self.listbox = tk.Listbox(self.calendar_frame, bg="white")
        self.listbox.pack(side="bottom", fill="both", expand=True)

        # 在主界面内容区域添加一些内容
        tk.Label(self.content_right_area, text="欢迎使用！请点击侧边栏按钮查看任务日历系统", font=('华文行楷', 15)).pack(
            expand=True, fill='both')

        # 在侧边栏添加一些内容
        self.create_sidebar(sidebar)

    # def __init__(self, root):
        # def select_date():
            #当用户选择日期时，这个函数会被调用
        #   selected_date = self.cal.get_date()
        #   self.date_label.config(text=f"Selected Date: {selected_date}")

        # 创建主窗口
        # self.buttons = []
        # self.root = root
        # self.root.title("主界面")

        # 设置窗口大小
        # self.root.winfo_screenwidth()
        # self.root.winfo_screenheight()
        # self.root.geometry("1200x720")

        # 创建一个主框架，用于放置其他组件
        # main_frame = tk.Frame(root)
        # main_frame.pack(fill=tk.BOTH, expand=True)

        # 创建侧边栏和主界面内容区域

        # self.content_area = tk.Frame(main_frame)
        # sidebar.grid(row=0, column=0, sticky="ns")
        # self.content_area.grid(row=0, column=1, sticky="nsew")

        # 初始化categories_frame，确保它可以在整个类中被引用
        # self.categories_frame = tk.Frame(sidebar)

        # 创建下边栏
        # bottom_bar = tk.Frame(main_frame)
        # bottom_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

        # 调整列权重，使得主界面内容区域比侧边栏宽
        # main_frame.columnconfigure(1, weight=2)  # 主界面内容区域占80%
        # main_frame.columnconfigure(0, weight=1)  # 侧边栏占20%
        # main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        # main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        # 在侧边栏添加一些内容
        # self.create_sidebar(sidebar)

        # 在下边栏添加一些内容
        # tk.Label(bottom_bar, text="").pack(fill='x')

        # 创建日历组件和相关控件
        # self.calendar_frame = tk.Frame(self.content_right_area, padx=120, pady=45)
        # self.calendar_frame.pack(side="top", fill="both", expand=True)

        # self.cal = Calendar(self.calendar_frame, selectmode='day', year=2024, month=7, day=16)
        # self.cal.pack(side="top", fill="both", pady=(0, 10))

        # self.select_button = tk.Button(self.calendar_frame, text="Select Date", command=select_date)
        # self.select_button.pack(side="top")
        # self.date_label = tk.Label(self.calendar_frame, text="")
        # self.date_label.pack(side="top")

        # 创建一个用于显示任务列表的 Listbox
        # self.listbox = tk.Listbox(self.calendar_frame, bg="white")
        # self.listbox.pack(side="bottom", fill="both", expand=True)

        # 在主界面内容区域添加一些内容
        # tk.Label(self.content_right_area, text="欢迎使用！请点击侧边栏按钮查看任务日历系统", font=('华文行楷', 15)).pack(
        #   expand=True, fill='both')

    def create_sidebar(self, sidebar):
        def add_type(type, row_index):
            tasks_uncategorized = []
            button = tk.Button(self.categories_frame, text=str(type), font=('华文行楷', 15),
                                             command=lambda: show_calendar(tasks_uncategorized, button),
                                             bg="white")
            self.buttons.append(button)
            button.grid(row=row_index, column=0, sticky="ew")

        def change_color_for_button(button):
            for item in self.buttons:
                if item == button:
                    item["bg"] = "DarkGray"
                else:
                    item["bg"] = "white"

        def show_calendar(tasks, button):
            # self.debug(button)
            change_color_for_button(button)
            # 清除任务列表
            self.listbox.delete(0, tk.END)

            # 更新任务列表
            for task in tasks:
                self.listbox.insert(tk.END, task)

            # 更改listbox中的字体
            self.listbox.config(font=("华文宋体", 15))  # 这里使用了华文宋体和字号12作为示例

        def toggle_categories():
            if self.categories_frame.winfo_ismapped():  # 使用self.categories_frame
                self.categories_frame.grid_forget()
            else:
                self.categories_frame.grid(row=7, column=0, sticky="nsew")

        self.buttons = []

        row_index = 7

        # 创建一个frame来容纳所有的类别按钮
        # 注意这里不需要重新定义categories_frame，而是使用在__init__中定义的那个

        add_type("未分类", row_index)
        row_index += 1

        # add_type("工作", row_index)
        # row_index += 1

        # add_type("学习", row_index)
        # row_index += 1

        # add_type("竞赛", row_index)
        # row_index += 1

        # add_type("生活", row_index)
        # row_index += 1

        # add_type("长期规划", row_index)
        # row_index += 1

        # add_type("放纵", row_index)
        # row_index += 1

        # 最初隐藏类别按钮
        self.categories_frame.pack_forget()

        # 添加一些垂直间距
        spacer_top = tk.Label(sidebar, text="", pady=10)
        spacer_top.grid(row=0, column=0)

        # 其他按钮保持不变
        tasks_day_todo = ["任务乙", "任务丙", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        day_todo_button = tk.Button(sidebar, text="Day Todo", font=('华文行楷', 15),
                                    command=lambda: show_calendar(tasks_day_todo, day_todo_button), bg="white")
        day_todo_button.grid(row=1, column=0, sticky="ew")
        self.buttons.append(day_todo_button)

        recent_tasks = ["任务甲", "任务乙", "任务丙"]
        recent_tasks_button = tk.Button(sidebar, text="最近待办", font=('华文行楷', 15),
                                        command=lambda: show_calendar(recent_tasks, recent_tasks_button), bg="white")
        recent_tasks_button.grid(row=2, column=0, sticky="ew")
        self.buttons.append(recent_tasks_button)

        tasks_todo_box = ["任务甲", "任务乙", "任务丙"]
        todo_box_button = tk.Button(sidebar, text="待办箱", font=('华文行楷', 15),
                                    command=lambda: show_calendar(tasks_todo_box, todo_box_button), bg="white")
        todo_box_button.grid(row=4, column=0, sticky="ew")
        self.buttons.append(todo_box_button)

        # 添加一些垂直间距
        spacer = tk.Label(sidebar, text="", pady=10)
        spacer.grid(row=5, column=0)

        # 创建“分类清单”按钮，点击时切换显示/隐藏类别按钮
        # 将其置于“待办箱”按钮下方，并与之保持一定距离
        categories_button = tk.Button(sidebar, text="分类清单", font=('华文行楷', 15), command=toggle_categories, bg="white")
        categories_button.grid(row=6, column=0, sticky="ew")


def createMainWindowAndReturn(app=None):
    # root = tk.Tk()
    newApp = TaskDisplayApp(app)
    return newApp.content_area

# open_main_window()
