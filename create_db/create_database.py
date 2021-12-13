import sqlite3


def create_db():
    conn = sqlite3.connect('DV')
    c = conn.cursor()

    c.execute('''
              CREATE TABLE IF NOT EXISTS Driver
              ([id] INTEGER PRIMARY KEY, [first_name] TEXT, [last_name] TEXT, [created_at] TEXT,  [updated_at] TEXT)
              ''')

    c.execute('''
              CREATE TABLE IF NOT EXISTS Vehicle
              ([id] INTEGER PRIMARY KEY, [driver_id] INTEGER, [make] TEXT, [model] TEXT,  [plate_number] TEXT,  [created_at] TEXT, [updated_at] TEXT,
              FOREIGN KEY (driver_id) 
              REFERENCES Driver (id) 
              )
           ''')

    conn.commit()


'''ON UPDATE SET NULL
          ON DELETE SET NULL'''


def create_database():
    return None

def clear_db():
    conn = sqlite3.connect('DV')
    c = conn.cursor()

    c.execute('''
                  DELETE FROM Vehicle;
                  ''')

    c.execute('''
                  DELETE FROM Driver;
                  ''')

    conn.commit()