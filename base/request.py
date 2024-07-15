from enum import Enum

class Command(Enum):
    CREATE = 1,      # 任务创建
    MODIFY = 2,      # 任务修改
    DELETE = 3,      # 任务删除
    GET_ALL = 4,     # 获取所有任务
    GET_EXPIRED = 5, # 获取所有过期任务
    ADD_CATEGORY = 6,     # 增加一个新的mission类型
    DELETE_CATEGORY = 7,  # 删除一个mission类型


class Request:
    def __init__(self, req_type : Command, uid=-1, mission=None):
        self.uid = uid             # 发出当前请求的用户
        self.req_type = req_type   # 请求类型: eg. Command.CREATE, Command.MODIFY ...
        self.mission = mission     # 请求对应的任务，可以为None，定义见mission.py
