import database.db_handler as db

def global_init():
    # start db
    db.connect_db()
    print("Config: Connected to database")


def global_close():
    # close db
    db.close_db(db.connect_db())
    print("Config: Closed database")

version = 2.0