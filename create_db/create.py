from create_db.add_data import adddata
from create_db.create_database import create_db
from create_db.display_data import displaydata
from create_db.create_database import clear_db


def create():
    create_db()
    clear_db()
    adddata()
    displaydata()


create()
