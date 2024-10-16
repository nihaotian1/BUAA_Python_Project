import database.db_handler as db


def schedule_tasks(uid, date):
    # Arrange from 8:00-22:00 by default (14h)
    missions = db.find_tasks_by_due_date(date, uid)

    # sort by weight
    missions = sorted(missions, key=lambda m: m.weight, reverse=True)

    # time should <= 14
    schedules = []
    cost = 0
    for m in missions:
        if(m.complete):
            continue
        cost += m.duration
        schedules.append(m)
        if cost >= 14:
            break

    times = []
    start = 8
    end = 8
    for m in schedules:
        if m.duration != 0:
            end += m.duration
        else:
            end += 1
        end = min(22, end)
        times.append('建议-从{}点到{}点'.format(start, end))
        start = end
        if start == 22:
            break

    return missions, times