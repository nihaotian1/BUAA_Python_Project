from base.request import Request, Command
import ctrl.mission_utils as m_utils


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

    raise Exception('Unknown request type')