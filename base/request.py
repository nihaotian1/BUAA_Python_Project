from enum import Enum


class Command(Enum):
    CREATE = 1,      # 任务创建
    MODIFY = 2,      # 任务修改
    DELETE = 3,      # 任务删除
    GET_ALL = 4,     # 获取所有任务
    GET_EXPIRED = 5, # 获取所有过期任务
    ADD_CATEGORY = 6,         # 增加一个新的mission类型
    DELETE_CATEGORY = 7,      # 删除一个mission类型
    REGISTER_USER = 8,        # 注册一个新用户
    LOG_IN = 9,               # 用户登录
    UDPATE_USER_INFO = 10,    # 更新用户信息
    GET_TODAY_MISSION = 11    # 获取今日任务清单
    GET_CATEGORY_MISSION = 12 # 获取某一类任务
    GET_CATEGORY_COLOR = 13,
    SCHEDULE = 14


class Request:
    def __init__(self, req_type : Command, uid=-1, mission=None,
                 user_name=None, user_password=None, category=None, color=None, date=None):
        self.uid = uid             # 发出当前请求的用户
        self.req_type = req_type   # 请求类型: eg. Command.CREATE, Command.MODIFY ...
        self.mission = mission     # 请求对应的任务，可以为None，定义见mission.py
        self.user_name = user_name         # 用户名
        self.user_password = user_password # 密码
        self.category = category   # 调用获取某类任务时候的类别
        self.color = color         # 当创建一个新类型时，这个类型对应的字体颜色
        self.date = date
