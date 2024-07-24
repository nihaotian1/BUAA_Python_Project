import database.db_handler as db


def register(user_name, user_password):
    # at least 8 char for password
    # > 0 char ==> usr_name
    if len(user_name) == 0 or len(user_password) < 8:
        return "Invalid username or password"

    work = db.register_user(user_name, user_password)
    if work:
        return "Successfully registered"
    else:
        return "Unknown Error inside database"


def login(user_name, user_password):
    res = db.get_user_info(user_name)

    if res is None:
        return "User not found"
    if res[2] != user_password:
        return "Wrong password"
    else:
        return res[0]


def udpate_user(uid, user_name, user_password):
    if len(user_password) < 8:
        return "Invalid password"

    work = db.update_user(uid, user_name, user_password)

    if work:
        return "Successfully updated"
    else:
        return "Unknown Error inside database"
