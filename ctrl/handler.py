from base.request import Request, Command
import mission_utils


'''
    这个函数是 (前端唯一需要调用的函数) !!!
    请阅读base.request, base.mission 中关于 Request, Command, Mission的类定义
    req: Request类型
    ret: 类型根据实际函数的不同会有区别
'''
def handle(req : Request):
    if 1 <= req.req_type <= 5: # Mission Related
        if req.req_type == Command.CREATE:
            return mission_utils.create_mission(req.mission) # 0
        elif req.req_type == Command.MODIFY:
            return mission_utils.modify_mission(req.mission) # 0
        elif req.req_type == Command.DELETE:
            return mission_utils.delete_mission(req.mission) # 0
        elif req.req_type == Command.GET_EXPIRED:
            return mission_utils.get_expired_mission() # [missions]
        elif req.req_type == Command.GET_ALL:
            return mission_utils.get_all_mission()     # [missions]

    raise Exception('Unknown request type')
