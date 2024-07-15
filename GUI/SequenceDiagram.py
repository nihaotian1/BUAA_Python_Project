import tkinter as tk
from tkinter import Listbox, END, ttk, StringVar, Entry, Button, Label, Frame
from datetime import datetime
from ctrl.handler import handle
from base.request import Command,Request
from base.mission import Mission
from database.db_handler import connect_db, close_db, init_db


class TaskManagerApp(Frame):
    def __init__(self, root):
        self.root = root
        self.root.title("任务顺序图")
        self.root.geometry("1200x720+150+0")  # 扩大视图界面

        self.tasks = []  # 存储任务信息的列表

        # 创建UI框架
        self.setup_ui()

    def getAllTasks(self,uid):
        req = Request(Command.GET_ALL,uid)
        tasks = handle(req)
        print(tasks)

    def setup_ui(self):
        # 顶部标签和输入框框架
        self.AddFrame = Frame(self.root,width=500,height=500,bg="black")
        self.AddFrame.place(relx = 0,rely = 0)

        Label(self.AddFrame, text="任务名称:").grid(row=0, column=0, padx=10, pady=5)
        self.task_name_entry = Entry(self.AddFrame, width=40)
        self.task_name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="截止日期 (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        self.deadline_entry = Entry(self.AddFrame, width=20)
        self.deadline_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="任务类型 (1-5):").grid(row=2, column=0, padx=10, pady=5)
        self.type_entry = Entry(self.AddFrame, width=5)
        self.type_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="任务持续时间 (小时):").grid(row=3, column=0, padx=10, pady=5)
        self.duration_entry = Entry(self.AddFrame, width=10)
        self.duration_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="任务权重:").grid(row=4, column=0, padx=10, pady=5)
        self.weight_entry = Entry(self.AddFrame, width=10)
        self.weight_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="是否是日常任务 (1是/0否):").grid(row=5, column=0, padx=10, pady=5)
        self.daily_entry = Entry(self.AddFrame, width=5)
        self.daily_entry.grid(row=5, column=1, padx=10, pady=5)

        self.add_button = Button(self.AddFrame, text="添加任务", command=self.add_task,bg="yellow")
        self.add_button.grid(row=6, column=1, padx=10, pady=5)

        self.AddFrame.place_forget()

        # 任务列表
        self.task_listbox = Listbox(self.root, width=100, height=30, font=("Arial", 14))
        self.task_listbox.pack(pady=20)

        # add按钮,remove按钮
        topF = Frame(self.root,width=30,height=20,bg="yellow",bd="2")
        topF.place(relx = 0.9,rely = 0.8)
        self.button_add = Button(topF,text = "ADD",command=self.openADDFrame,bg="yellow")
        self.remove_button = Button(topF, text="删除", command=self.remove_task,bg = "red")
        self.remove_button.pack()
        self.button_add.pack()

        # 初始化任务列表
        self.update_task_list()

    def openADDFrame(self):
        self.task_listbox.pack_forget()
        # self.AddFrame.place(relx=0.3, rely=0.3, )
        self.AddFrame.pack(pady=20)
        self.task_listbox.pack(pady=20)

    def closeADDFrame(self):
        self.AddFrame.pack_forget()
        self.task_listbox.pack(pady=20)

    def add_task(self):
        task_name = self.task_name_entry.get().strip()
        if not task_name:
            return

        deadline_str = self.deadline_entry.get().strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d") # "%Y-%m-%d %H:%M:%S.%f"
            except ValueError:
                print("截止日期格式错误，应为 YYYY-MM-DD")
                return
        else:
            deadline = datetime.now()
        task_conTime = self.duration_entry.get().strip()
        task_type = self.type_entry.get().strip()
        oneMission = Mission(1,task_name,task_conTime,type=task_type)
        req = Request(req_type=Command.CREATE,uid=-1,mission=oneMission)
        handle((req))

        task_status = '未开始'
        if(datetime.now().date() > deadline.date()):
            task_status = '已过期'
        if(datetime.now().date() == deadline.date()):
            task_status = '正在进行'
        self.tasks.append({'name': task_name, 'status': task_status, 'deadline': deadline})
        self.update_task_list()
        self.closeADDFrame()

    def update_task_status(self):
        # 这里为了简化，我们仅允许通过控制台更新状态（实际中可能需要更复杂的界面）
        print("更新任务状态功能暂未实现完整GUI界面，请通过控制台操作。")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            del self.tasks[index]
            self.update_task_list()

    def update_task_list(self):
        # self.task_listbox.delete(0, END)
        self.getAllTasks(1)
        for index, task in enumerate(self.tasks):
            status_color = {
                '未开始': 'lightgrey',
                '正在进行': 'yellow',
                '已完成': 'green',
                '已过期': 'red'
            }[task['status']]

            deadline_str = task['deadline'].strftime("%Y-%m-%d") if task['deadline'] else '无'
            task_str = f"{task['name']} - {task['status']} (截止: {deadline_str})"
            self.task_listbox.insert(END, task_str)
            self.task_listbox.itemconfig(index, bg=status_color)

def openSequenceDiagram():
    root = tk.Tk()
    init_db()
    app = TaskManagerApp(root)
    root.mainloop()

openSequenceDiagram()