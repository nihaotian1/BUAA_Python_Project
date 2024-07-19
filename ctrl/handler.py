from base.request import Request, Command
import ctrl.mission_utils as m_utils
import ctrl.user_uitls as u_utils

# class Command(Enum):
#     CREATE = 1,      # 任务创建
#     MODIFY = 2,      # 任务修改
#     DELETE = 3,      # 任务删除
#     GET_ALL = 4,     # 获取所有任务
#     GET_EXPIRED = 5, # 获取所有过期任务
#     ADD_CATEGORY = 6,         # 增加一个新的mission类型
#     DELETE_CATEGORY = 7,      # 删除一个mission类型
#     REGISTER_USER = 8,        # 注册一个新用户
#     LOG_IN = 9,               # 用户登录
#     UDPATE_USER_INFO = 10,    # 更新用户信息
#     GET_TODAY_MISSION = 11    # 获取今日任务清单
#     GET_CATEGORY_MISSION = 12 # 获取某一类任务

'''
    这个函数是 (前端唯一需要调用的函数) !!!
    请阅读base.request, base.mission 中关于 Request, Command, Mission的类定义
    req: Request类型
    ret: 类型根据实际函数的不同会有区别
'''
def handle(req : Request):
    # Mission Related
    if req.req_type == Command.CREATE:
        return m_utils.create_mission(req.mission) # 0
    elif req.req_type == Command.MODIFY:
        return m_utils.modify_mission(req.mission) # 0
    elif req.req_type == Command.DELETE:
        return m_utils.delete_mission(req.mission) # 0
    elif req.req_type == Command.GET_EXPIRED:
        return m_utils.get_expired_mission() # [missions]
    elif req.req_type == Command.GET_ALL:
        return m_utils.get_all_mission()     # [missions]
    elif req.req_type == Command.ADD_CATEGORY:
        return m_utils.add_category(req.category, req.color, req.uid)
    elif req.req_type == Command.DELETE_CATEGORY:
        return m_utils.del_category(req.category, req.uid)
    elif req.req_type == Command.REGISTER_USER:
        return u_utils.register(req.user_name, req.user_password) # str
    elif req.req_type == Command.LOG_IN:
        return u_utils.login(req.user_name, req.user_password)
    elif req.req_type == Command.UDPATE_USER_INFO:
        return u_utils.udpate_user(req.uid, req.user_name, req.user_password)
    elif req.req_type == Command.GET_TODAY_MISSION:
        return m_utils.get_today_mission(req.uid)
    elif req.req_type == Command.GET_CATEGORY_MISSION:
        return m_utils.get_category(req.category, req.uid)
    elif req.req_type == Command.GET_CATEGORY_COLOR:
        return m_utils.get_category_color(req.category, req.uid)
    raise Exception('Unknown request type')