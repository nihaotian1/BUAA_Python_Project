import tkinter as tk
from tkinter import Listbox, END, ttk, StringVar, Entry, Button, Label, Frame
from datetime import datetime
from ctrl.handler import handle
from base.request import Command,Request
from base.mission import Mission

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("任务顺序图")
        self.root.geometry("1200x800")  # 扩大视图界面

        self.tasks = []  # 存储任务信息的列表

        # 创建UI框架
        self.setup_ui()

    def setup_ui(self):
        # 顶部标签和输入框框架
        top_frame = Frame(self.root)
        top_frame.pack(pady=20)

        Label(top_frame, text="任务名称:").grid(row=0, column=0, padx=10, pady=5)
        self.task_name_entry = Entry(top_frame, width=40)
        self.task_name_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(top_frame, text="截止日期 (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        self.deadline_entry = Entry(top_frame, width=20)
        self.deadline_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(top_frame, text="任务类型 (1-5):").grid(row=2, column=0, padx=10, pady=5)
        self.type_entry = Entry(top_frame, width=5)
        self.type_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(top_frame, text="任务持续时间 (小时):").grid(row=3, column=0, padx=10, pady=5)
        self.duration_entry = Entry(top_frame, width=10)
        self.duration_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(top_frame, text="任务权重:").grid(row=4, column=0, padx=10, pady=5)
        self.weight_entry = Entry(top_frame, width=10)
        self.weight_entry.grid(row=4, column=1, padx=10, pady=5)

        Label(top_frame, text="是否是日常任务 (1是/0否):").grid(row=5, column=0, padx=10, pady=5)
        self.daily_entry = Entry(top_frame, width=5)
        self.daily_entry.grid(row=5, column=1, padx=10, pady=5)

        # 按钮
        button_frame = Frame(self.root)
        button_frame.pack(pady=20)

        self.add_button = Button(button_frame, text="添加任务", command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.remove_button = Button(button_frame, text="删除任务", command=self.remove_task)
        self.remove_button.pack(side=tk.RIGHT, padx=10, pady=5)

        # 任务列表
        self.task_listbox = Listbox(self.root, width=100, height=30, font=("Arial", 14))
        self.task_listbox.pack(pady=20)

        # 初始化任务列表
        self.update_task_list()

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

                # 假设默认状态为“未开始”
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

        # 清空输入框
        self.task_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)

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
        self.task_listbox.delete(0, END)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()