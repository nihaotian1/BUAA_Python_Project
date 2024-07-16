import tkinter as tk
from tkinter import Listbox, END, ttk, StringVar, Entry, Button, Label, Frame
from datetime import datetime
from ctrl.handler import handle
from base.request import Command,Request
from base.mission import Mission
from database.db_handler import connect_db, close_db, init_db

class TaskManagerApp(Frame): # 顺序图界面 也是编辑界面
    def __init__(self,app = None):

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
        self.content_area.destroy() # 销毁原来的内容区域，注意所有不能留给下一界面的组件都需要放在这里，因为只摧毁它
        self.root.title("任务顺序图")
        self.root.geometry("1200x720+150+0")  # 扩大视图界面

        # 修改按钮颜色  注意不能修改指令，否则会导致循环依赖import，导致死锁！！！！！！！！！！！！
        self.start_button["bg"] = "white"
        self.overview_button["bg"] = "white"
        self.edit_button["bg"] = "DarkGray"

        # 恢复框架结构 ，只摧毁了content_area
        self.content_area = tk.Frame(self.main_frame)
        self.content_area.grid(row=0, ipadx=1, ipady=1, sticky="nsew")

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=0)
        self.main_frame.rowconfigure(0, weight=1)  # 主界面和侧边栏的高度可变
        self.main_frame.rowconfigure(1, minsize=50)  # 下边栏有最小高度100像素

        # 创建UI框架
        self.setup_ui()


    def setup_ui(self):
        # 添加任务输入框框架

        self.AddFrame = Frame(self.content_area,width=100,height=500,bg="LightSteelBlue")
        self.AddFrame.place(relx = 0,rely = 0)

        Label(self.AddFrame, text="添加新的任务:", font=("Arial", 14)).grid(row=0, column=0, padx=0, pady=5)
        Label(self.AddFrame, text="(带*号选填)", font=("Arial", 14)).grid(row=0, column=1, padx=0, pady=5)

        Label(self.AddFrame, text="任务名称:").grid(row=1, column=0, padx=10, pady=5)
        self.task_name_entry = Entry(self.AddFrame, width=40)
        self.task_name_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="截止日期 (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        self.deadline_entry = Entry(self.AddFrame, width=20)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="任务类型:").grid(row=3, column=0, padx=10, pady=5)
        self.type_entry = Entry(self.AddFrame, width=5)
        self.type_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="*任务持续时间 (小时):").grid(row=4, column=0, padx=10, pady=5)
        self.duration_entry = Entry(self.AddFrame, width=10)
        self.duration_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="*任务权重:").grid(row=5, column=0, padx=10, pady=5)
        self.weight_entry = Entry(self.AddFrame, width=10)
        self.weight_entry.grid(row=5, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="*是否是日常任务:").grid(row=6, column=0, padx=10, pady=5)
        self.daily_entry = Entry(self.AddFrame, width=5)
        self.daily_entry.grid(row=6, column=1, padx=10, pady=5)

        self.cancel_button = Button(self.AddFrame, text="取消", command=self.closeADDFrame,bg="red")
        self.cancel_button.grid(row=7, column=0, padx=10, pady=5)
        self.add_button = Button(self.AddFrame, text="确认", command=self.add_task,bg="yellow")
        self.add_button.grid(row=7, column=1, padx=10, pady=5)

        self.AddFrame.place_forget() # 隐藏输入框直到用户点击ADD按钮

        # 任务列表区域
        self.task_list_frame = Frame(self.content_area,width=100,height=500,bg="Cyan")
        self.task_list_frame.pack(pady=20)
        button_frame = Frame(self.task_list_frame,width=100,height=50,bg="Cyan")
        button_frame.grid(row =0, column =0, padx=0, pady=5)
        self.task_listbox = Listbox(self.task_list_frame, width=100, height=30, font=("Arial", 14), bg="Cyan")
        self.task_listbox.grid(row=1, column=0, padx=0, pady=5)
        self.remove_button = Button(button_frame, text="删除所选任务", command=self.remove_task,bg = "red")
        self.complete_button = Button(button_frame, text="完成所选任务", command=self.complete_task,bg = "green")
        self.remove_button.grid(row =0, column =0, padx=0, pady=5)
        self.complete_button.grid(row =0, column =1, padx=1, pady=5)


        # add按钮,remove按钮
        topF = Frame(self.content_area,width=30,height=20,bg="Cyan")
        topF.place(relx = 0.9,rely = 0.8)
        self.button_add = Button(topF,text = "+",command=self.openADDFrame,bg="yellow")
        self.button_add.pack()


        # 初始化任务列表
        self.update_task_list()

    def openADDFrame(self):  # 打开添加任务界面（点击ADD）
        self.task_list_frame.pack_forget()  # 先把列表区域隐藏
        self.AddFrame.pack(pady=20)  # 再显示输入框
        self.task_list_frame.pack(pady=20)  # 再显示列表

    def closeADDFrame(self): # 关闭添加任务界面
        self.AddFrame.pack_forget()
        self.task_list_frame.pack(pady=20)

    def add_task(self):
        # 解析输入名称和日期
        task_name = self.task_name_entry.get().strip()
        if not task_name:
            return
        deadline_str = self.deadline_entry.get().strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d") # "%Y-%m-%d %H:%M:%S.%f"
                deadline = deadline.date()
            except ValueError:
                print("截止日期格式错误，应为 YYYY-MM-DD")
                return
        else:
            deadline = datetime.now().date()
        task_conTime = self.duration_entry.get().strip()
        # 调用后端处理函数
        task_type = self.type_entry.get().strip()
        oneMission = Mission(self.uid,task_name,deadline,duration=task_conTime,type=task_type)
        req = Request(req_type=Command.CREATE,uid=-1,mission=oneMission)
        handle((req))
        # 更新任务列表
        self.update_task_list()
        # 关闭添加任务界面
        self.closeADDFrame()

    def complete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]  # 这个能返回鼠标点击的行号
            mession = self.tasks[index]
            mession.complete = True
            print("向后端发送mission的name:",mession.name)
            req = Request(Command.MODIFY,1,mession)
            # 更新后端数据
            handle(req)
            self.update_task_list()

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]  # 这个能返回鼠标点击的行号
            mession = self.tasks.pop(index)
            req = Request(Command.DELETE,1,mession)
            # 删除后端数据
            handle(req)
            self.update_task_list()

    def update_task_status(self):
        # 这里为了简化，我们仅允许通过控制台更新状态（实际中可能需要更复杂的界面）
        print("更新任务状态功能暂未实现完整GUI界面，请通过控制台操作。")

    def getAllTasks(self): # 更新tasks
        req = Request(Command.GET_ALL,self.uid)
        self.tasks = handle(req)

    def update_task_list(self): # 更新任务列表，调用上面那个函数
        self.getAllTasks()
        self.task_listbox.delete(0, END)
        status_color = 'lightgrey'
        staus_str = '未完成'
        for mission in self.tasks:
            try:
                if(mission.complete == False):
                    due = datetime.strptime(mission.due, "%Y-%m-%d") # 返回datetime对象
                    due = due.date() # 取出datetime里的date部分
            except:
                print("后端返回的日期格式错误")
            try:
                if mission.complete:
                    status_color = 'green'
                    staus_str = '已完成'
                elif due < datetime.now().date():
                    status_color ='red'
                    staus_str = '已过期'
                elif due == datetime.now().date():
                    status_color = 'yellow'
                    staus_str = '进行中'
                else:
                    status_color = 'lightgrey'
            except:
                print("error")

            deadline_str = mission.due
            if deadline_str == '0':
                task_str = f"{mission.name} - {staus_str}"
            else:
                task_str = f"{mission.name} - {staus_str} (截止: {deadline_str})"
            self.task_listbox.insert(END,  task_str)
            self.task_listbox.itemconfig(END, bg=status_color)

    def close_window(self):
        # 关闭窗口，这将间接关闭Frame
        self.root.destroy()

def createEditWindowAndReturn(app=None):  # 需要传入用户id和root窗口
    init_db()  # 初始化数据库
    newApp = TaskManagerApp(app)
    return newApp.content_area



