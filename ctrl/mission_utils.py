import config.config

import database.db_handler as db
from datetime import datetime


'''
    返回按照due日期排序的所有missions
    并 return 一个 list
'''
def get_all_mission(uid=-1) -> []:
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

    tasks = db.get_all_tasks(uid)

    tasks = sorted(tasks, key=lambda x : x.due, reverse=True)

    return tasks


'''
    返回一个按照due日期排序的过期missions列表
'''
def get_expired_mission(uid=-1) -> []:
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

    tasks = db.get_expired_tasks(uid)

    tasks = sorted(tasks, key=lambda x : x.due, reverse=True)

    return tasks


def create_mission(mission, uid=-1):
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

    db.add_task(uid, mission.name, mission.description, mission.due, mission.duration,mission.type,
                mission.weight, mission.isdaily)

    return 0 # 0 on success


def modify_mission(mission, uid=-1):
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

    db.update_task(mission.mid, mission.name, mission.description, mission.due, mission.duration, mission.type,
                   mission.weight, mission.isdaily, mission.complete)

    return 0 # 0 on success


def delete_mission(mission, uid=-1):
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

    db.delete_task(mission.mid)

    return 0


def get_today_mission(uid=-1):
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

    today = datetime.now().strftime("%Y-%m-%d")
    tasks = db.find_tasks_by_due_date(today, uid)

    tasks = sorted(tasks, key=lambda x : x.weight, reverse=True)

    return tasks


def get_category(category, uid=-1):
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

    tasks = db.find_tasks_by_type(category, uid)
    tasks = sorted(tasks, key=lambda x: x.due, reverse=True)

    return tasks


def add_category(category, uid=-1):
    if uid == -1 and config.config.version != 0.5:
        raise Exception('Unknown UserId!')

