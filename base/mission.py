class Mission:
    def __init__(self, uid, name, due, mid=-1, duration=1, type='default', weight=1.0, is_daily=False, complete=False):
        # 用户ID
        self.uid = uid
        # 任务ID
        self.mid = mid
        # 任务名称
        self.name = name
        # 任务日期设定，if 当前日期 > due ==> 过期
        self.due = due
        # 任务类型
        self.type = type
        # 任务持续时间 (为了方便进行调度，提前留好接口)
        self.duration = duration
        # 权重
        self.weight = weight
        # 是否为日常任务
        self.isdaily = is_daily
        # 是否已完成
        self.complete = complete

# class Event:
#     def __init__(self, title, description,start_day, start_time, end_time, end_day, isDayly, weight , completed=False):
#         self.title = title
#         self.description = description
#         self.start_day = start_day
#         self.start_time = start_time
#         self.end_day = end_day
#         self.end_time = end_time
#         self.completed = completed
#         self.isDayly = isDayly
#         self.weight = weight
#
#
#     def __str__(self):
#         status = "已完成" if self.completed else "未完成"
#         return f"{self.title}: {self.start_time} - {self.end_time}, 状态: {status}"
