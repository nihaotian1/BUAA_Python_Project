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
        self.setup_add_Frame()


        # 任务列表区域
        self.task_list_frame = Frame(self.content_area,width=100,height=500,bg="Cyan")
        self.task_list_frame.pack(pady=20)

        button_frame = Frame(self.task_list_frame,width=100,height=50,bg="Cyan")
        button_frame.grid(row =0, column =0, padx=0, pady=0)
        self.remove_button = Button(button_frame, text="删除所选任务", command=self.remove_task, bg="red")
        self.change_task_button = Button(button_frame, text="修改所选任务", command=self.change_task, bg="orange")
        self.details_button = Button(button_frame, text="所选任务详情", command=self.show_task_details, bg="gray")
        self.complete_button = Button(button_frame, text="完成所选任务", command=self.complete_task, bg="green")
        self.remove_button.grid(row=0, column=0, padx=0, pady=5)
        self.change_task_button.grid(row=0, column=1, padx=1, pady=5)
        self.details_button.grid(row=0, column=2, padx=1, pady=5)
        self.complete_button.grid(row=0, column=3, padx=1, pady=5)

        self.task_listbox = Listbox(self.task_list_frame, width=100, height=30, font=("Arial", 14), bg="Cyan")
        self.task_listbox.grid(row=1, column=0, padx=0, pady=0)


        # add按钮,remove按钮
        topF = Frame(self.content_area,width=30,height=20,bg="Cyan")
        topF.place(relx = 0.9,rely = 0.8)
        self.button_add = Button(topF,text = "+",command=self.openADDFrame,bg="yellow")
        self.button_add.pack()


        # 初始化任务列表
        self.update_task_list()

    def setup_add_Frame(self): # 这是添加任务界面
        self.AddFrame = Frame(self.content_area, width=100, height=500, bg="LightSteelBlue")
        self.AddFrame.place(relx=0, rely=0)

        Label(self.AddFrame, text="请添加新的任务:", font=("宋体", 14)).grid(row=0, column=0, padx=0, pady=5)
        Label(self.AddFrame, text="(带*号选填)", font=("Arial", 14)).grid(row=0, column=1, padx=0, pady=5)

        Label(self.AddFrame, text="任务名称:").grid(row=1, column=0, padx=10, pady=5)
        self.task_name_entry = Entry(self.AddFrame, width=40)
        self.task_name_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="*截至 (YYYY-MM-DD)\n不写默认今天:").grid(row=2, column=0, padx=10, pady=5)
        self.deadline_entry = Entry(self.AddFrame, width=20)
        self.deadline_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="*任务类型（默认无）:").grid(row=3, column=0, padx=10, pady=5)
        self.type_entry = Entry(self.AddFrame, width=5)
        self.type_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.AddFrame, text="*任务描述:").grid(row=4, column=0, padx=10, pady=5)
        self.description_entry = tk.Text(self.AddFrame, width=40, height=5)
        self.description_entry.grid(row=4, column=1, padx=10, pady=5)

        self.duration_value = 0
        self.weight_value = 0
        self.daily_value = 0

        button_add_more = Button(self.AddFrame, text="添加权重等信息", command=self.create_add_more_menu, bg="yellow")
        button_add_more.grid(row=5, column=0, padx=10, pady=5)


        self.cancel_button = Button(self.AddFrame, text="取消", command=self.closeADDFrame, bg="red")
        self.cancel_button.grid(row=6, column=0, padx=10, pady=5)
        self.add_button = Button(self.AddFrame, text="确认", command=self.add_task, bg="yellow")
        self.add_button.grid(row=6, column=1, padx=10, pady=5)

        self.AddFrame.place_forget()  # 隐藏输入框直到用户点击ADD按钮


    def create_add_more_menu(self,change_v1 = None,change_v2 = None,change_v3 = None):
        def change_duration(l1,v1):
            l1["text"] = f"{v1}小时"
            self.duration_value = v1
        def change_weight(l2,v2):
            l2["text"] = "无"
            self.weight_value = v2
            if v2 == 1:
                l2["text"] = "低"
            elif v2 == 2:
                l2["text"] = "中"
            elif v2 == 3:
                l2["text"] = "高"
        def change_daily(l3,v3):
            self.daily_value = v3
            if v3 == 1:
                l3["text"] = "是"
            else:
                l3["text"] = "否"

        top_add_more = tk.Toplevel()
        top_add_more.title("任务详情")
        top_add_more.geometry("300x120+630+300")

        def on_cancel():
            # 弹窗关闭
            top_add_more.destroy()

        add_menu = tk.Menu(top_add_more, tearoff=0)

        time_nume_menu = tk.Menu(add_menu, tearoff=0)
        add_menu.add_cascade(label="持续时间", menu=time_nume_menu)
        weight_menu = tk.Menu(add_menu, tearoff=0)
        add_menu.add_cascade(label="权重", menu=weight_menu)
        daily_menu = tk.Menu(add_menu, tearoff=0)
        add_menu.add_cascade(label="日常", menu=daily_menu)

        label_Frame = Frame(top_add_more, width=100, height=50, bg="LightSteelBlue") # 权重等信息标签框架
        label_Frame.pack(pady=20)
        extend_Frame = Frame(top_add_more, width=100, height=50, bg="LightSteelBlue") # #方便扩展，在添加界面不使用。在修改的时候使用。

        Label(label_Frame, text="点击上方菜单栏修改权重等信息").grid(row=0, column=0,columnspan=4, padx=10, pady=5)


        l1 = Label(label_Frame, text="0小时")
        l1.grid(row=1, column=0, padx=10, pady=5)
        l2 = Label(label_Frame, text="无")
        l2.grid(row=1, column=1, padx=15, pady=5)
        l3 = Label(label_Frame, text="否")
        l3.grid(row=1, column=2, padx=10, pady=5)



        if change_v1 != None and change_v2  != None and change_v3 != None: #如果是修改任务，那么显示原来的权重
            change_duration(l1,change_v1)
            change_weight(l2,change_v2)
            change_daily(l3,change_v3)
        else:
            Button(label_Frame, text="确定", command=lambda: on_cancel(),bg = "yellow").\
                grid(row = 1, column = 3, padx=10, pady=5)

        for i in range(25):
            time_nume_menu.add_command(label=f"{i}小时", command=lambda v=i: change_duration(l1,v))
        weight_menu.add_command(label=f"无", command=lambda v=0: change_weight(l2,v))
        weight_menu.add_command(label=f"低", command=lambda v=1: change_weight(l2,v))
        weight_menu.add_command(label=f"中", command=lambda v=2: change_weight(l2,v))
        weight_menu.add_command(label=f"高", command=lambda v=3: change_weight(l2,v))

        daily_menu.add_command(label="否", command=lambda v=0: change_daily(l3,v))
        daily_menu.add_command(label="是", command=lambda v=1: change_daily(l3,v))

        top_add_more["menu"] = add_menu

        return top_add_more , extend_Frame

    def openADDFrame(self):  # 打开添加任务界面（点击ADD）
        self.duration_value = 0
        self.weight_value = 0
        self.daily_value = 0

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

        task_duration = self.duration_value
        task_weight = self.weight_value
        task_daily = self.daily_value
        task_description = self.description_entry.get("1.0", "end-1c").strip()

        # 调用后端处理函数
        task_type = self.type_entry.get().strip()
        oneMission = Mission(uid=self.uid,name=task_name,duration=task_duration,due=deadline,\
                             weight=task_weight,is_daily=task_daily,description=task_description,type=task_type)
        req = Request(req_type=Command.CREATE,uid=self.uid,mission=oneMission)
        handle(req)
        # 更新任务列表
        self.update_task_list()
        # 关闭添加任务界面
        self.closeADDFrame()

    def find_mission_index(self): #返回列表里鼠标坐在位置的mission
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = selected_index[0]  # 这个能返回鼠标点击的行号
            return self.tasks[index]
        return None

    def complete_task(self):
        top = tk.Toplevel()
        top.title("完成任务确认")

        top.geometry("200x100+680+300")

        # 弹窗中的文本
        label = tk.Label(top, text="真的完成了吗，年轻人？")
        label.pack(pady=20)

        def on_cancel():
            # 弹窗关闭
            top.destroy()

        cancel_button = tk.Button(top, text="啊……这", command=on_cancel,bg = "DarkGray")
        cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

        # 确认按钮
        def on_confirm():
            # 执行指令
            mession = self.find_mission_index()
            if mession:
                mession.complete = True
                req = Request(Command.MODIFY, self.uid, mession)
                # 更新后端数据
                handle(req)
                self.update_task_list()
            # 弹窗关闭
            top.destroy()

        confirm_button = tk.Button(top, text="完成啦！", command=on_confirm,bg = "green")
        confirm_button.pack(side=tk.RIGHT, padx=10, pady=10)



    def show_task_details(self):
        mission = self.find_mission_index()
        top = tk.Toplevel()
        top.title("任务详情")
        top.geometry("300x300+630+300")


        def on_cancel():
            # 弹窗关闭
            top.destroy()

        Label(top,text="任务名称:"+mission.name,font=("宋体", 14)).pack(pady=8)
        Label(top,text="截止日期:"+mission.due,font=("宋体", 14)).pack(pady=8)
        Label(top,text="持续时间:"+str(mission.duration)+"小时",font=("宋体", 14)).pack(pady=8)
        weight_str = "无"
        if mission.weight == 1:
            weight_str = "低"
        elif mission.weight == 2:
            weight_str = "中"
        elif mission.weight == 3:
            weight_str = "高"
        Label(top,text="权重:"+weight_str,font=("宋体", 14)).pack(pady=8)
        isdaily_str = "否"
        if mission.isdaily:
            isdaily_str = "是"
        Label(top,text="日常:"+isdaily_str,font=("宋体", 14)).pack(pady=8)
        Label(top,text="任务描述:",font=("宋体", 14)).pack(pady=8)
        Label(top,text=mission.description,font=("宋体", 14)).pack(pady=8)
        Button(top, text="知道了", command=on_cancel,bg = "yellow").pack(pady=8)



    def change_task(self):
        mission = self.find_mission_index()
        top = None
        extend_frame = None
        if mission:
            # 弹出修改任务界面
            top, extend_frame= self.create_add_more_menu(change_v1=mission.duration,change_v2=mission.weight,change_v3=mission.isdaily)
            top.title("修改任务")
            top.geometry("500x500+530+100")
        else:
            print("未选择任务")

        def on_cancel():
            # 弹窗关闭
            top.destroy()
        extend_frame.pack(pady=10)

        def remove_and_add_task():
            # 先删除原来的任务
            req = Request(Command.DELETE, self.uid, mission)
            # 删除后端数据
            handle(req)
            self.update_task_list()
            # 再添加修改后的任务
            change_task_name = self.change_name_entry.get().strip()
            change_deadline_str = self.change_deadline_entry.get().strip()
            change_deadline = None
            if change_deadline_str:
                try:
                    change_deadline = datetime.strptime(change_deadline_str, "%Y-%m-%d") # "%Y-%m-%d %H:%M:%S.%f"
                    change_deadline = change_deadline.date()
                except ValueError:
                    print("截止日期格式错误，应为 YYYY-MM-DD")
                    return
            else:
                change_deadline = datetime.now().date()
            change_description = self.change_description_entry.get("1.0", "end-1c").strip()
            change_type = self.change_type_entry.get().strip()
            change_mission = Mission(uid=self.uid,name=change_task_name,duration=self.duration_value,due=change_deadline,\
                             weight=self.weight_value,is_daily=self.daily_value,description=change_description,type=change_type)
            req = Request(Command.CREATE, self.uid, change_mission)
            # 添加后端数据
            handle(req)
            self.update_task_list()
            # 弹窗关闭
            top.destroy()

        Label(extend_frame,text="修改前",font=("宋体", 16)).grid(row=0, column=0, padx=10, pady=5)
        Label(extend_frame,text="修改为",font=("宋体", 16)).grid(row=0, column=1, padx=10, pady=5)
        Label(extend_frame,text="任务名称:"+mission.name,font=("宋体", 14)).grid(row=1, column=0, padx=10, pady=5)
        self.change_name_entry = Entry(extend_frame, width=20)
        self.change_name_entry.grid(row=1, column=1, padx=10, pady=5)
        self.change_name_entry.insert(0, mission.name)
        Label(extend_frame,text="截止日期:"+mission.due,font=("宋体", 14)).grid(row=2, column=0, padx=10, pady=5)
        self.change_deadline_entry = Entry(extend_frame, width=20)
        self.change_deadline_entry.grid(row=2, column=1, padx=10, pady=5)
        self.change_deadline_entry.insert(0, mission.due)
        Label(extend_frame,text="任务描述:",font=("宋体", 14)).grid(row=3, column=0, padx=10, pady=5)
        self.change_description_entry = tk.Text(extend_frame, width=20, height=5)
        self.change_description_entry.grid(row=3, column=1, padx=10, pady=5)
        self.change_description_entry.insert(1.0, mission.description)
        Label(extend_frame,text="任务类型:",font=("宋体", 14)).grid(row=4, column=0, padx=10, pady=5)
        self.change_type_entry = Entry(extend_frame, width=20)
        self.change_type_entry.grid(row=4, column=1, padx=10, pady=5)
        self.change_type_entry.insert(0, mission.type)
        Button(extend_frame, text="确定修改", command=remove_and_add_task,bg = "yellow").\
            grid(row = 8, column = 0, padx=10, pady=5)




    def remove_task(self):
        top = tk.Toplevel()
        top.title("删除任务确认")

        top.geometry("200x100+680+300")

        # 弹窗中的文本
        label = tk.Label(top, text="真的要删除任务吗，年轻人？")
        label.pack(pady=20)

        def on_cancel():
            # 弹窗关闭
            top.destroy()

        cancel_button = tk.Button(top, text="再考虑一下", command=on_cancel,bg = "DarkGray")
        cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

        # 确认按钮
        def on_confirm():
            # 执行指令
            mession = self.find_mission_index()
            if mession:
                req = Request(Command.DELETE, self.uid, mession)
                # 删除后端数据
                handle(req)
                self.update_task_list()
            # 弹窗关闭
            top.destroy()

        confirm_button = tk.Button(top, text="就删！", command=on_confirm,bg = "red")
        confirm_button.pack(side=tk.RIGHT, padx=10, pady=10)


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
            if staus_str == '已完成':
                task_str = f"{mission.name} - {staus_str}"
            else:
                task_str = f"{mission.name} - {staus_str} (截止: {deadline_str})"
            self.task_listbox.insert(END,  task_str)
            self.task_listbox.itemconfig(END, bg=status_color)

    def close_window(self):
        # 关闭窗口，这将间接关闭Frame
        self.root.destroy()


def createEditWindowAndReturn(app=None):  # 需要传入用户id和root窗口
    newApp = TaskManagerApp(app)
    return newApp.content_area