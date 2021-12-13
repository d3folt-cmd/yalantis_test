import sys
from datetime import datetime

from flask import Flask, request, jsonify
import sqlite3
import os


app = Flask(__name__)


def log(s):
    print(s, file=sys.stderr)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This is a prototype API</p>"


def datetime_format():
    return "%d/%m/%Y %H:%M:%S"


def query_date_format():
    return "%d-%m-%Y"


def now():
    return datetime.now().strftime(datetime_format())


def invalid_json_message():
    return "The content isn't of type JSON"


@app.route('/drivers/driver/', methods=['POST'])
def add_driver():
    log("add_driver")
    if not request.is_json:
        return invalid_json_message()

    content = request.get_json()
    first_name = content.get('first_name')
    last_name = content.get('last_name')
    time = now()
    created_at = time
    updated_at = time

    # Save the data in db
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)
    query = f'INSERT INTO Driver (first_name, last_name, created_at, updated_at) \
              VALUES ("{first_name}", "{last_name}", "{created_at}", "{updated_at}");'

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    return jsonify({'id': cur.lastrowid})


@app.route('/drivers/driver/', methods=['GET'])
def drivers():
    log("drivers")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    created_at__gte = request.args.get('created_at__gte')
    created_at__lte = request.args.get('created_at__lte')

    query = 'SELECT * FROM Driver;'
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_drivers = cur.execute(query).fetchall()

    if created_at__gte is not None:
        gte_drivers = []
        dt_gte = datetime.strptime(created_at__gte, query_date_format())
        for dr in all_drivers:
            log(str(dr))
            dt = datetime.strptime(dr.get('created_at'), datetime_format())
            if dt >= dt_gte:
                gte_drivers.append(dr)
        return jsonify(gte_drivers)
    else:
        if created_at__lte is not None:
            lte_drivers = []
            dt_lte = datetime.strptime(created_at__lte, query_date_format())
            for dr in all_drivers:
                dt = datetime.strptime(dr.get('created_at'), datetime_format())
                if dt <= dt_lte:
                    lte_drivers.append(dr)
            return jsonify(lte_drivers)

    return jsonify(all_drivers)


@app.route('/drivers/driver/<driver_id>/', methods=['GET'])
def find_driver(driver_id):
    log("find_driver")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    conn.row_factory = dict_factory
    dr = conn.execute("SELECT * FROM `Driver` WHERE `id` = ? ", driver_id).fetchall()

    return jsonify(dr)


@app.route('/drivers/driver/<driver_id>/', methods=['UPDATE'])
def edit_driver(driver_id):
    log("edit_driver")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    if not request.is_json:
        return invalid_json_message()

    content = request.get_json()
    first_name = content.get('first_name')
    last_name = content.get('last_name')
    updated_at = now()

    conn.row_factory = dict_factory
    cur = conn.cursor()

    query = f'UPDATE `Driver` SET '
    if first_name is not None:
        query = query + f' first_name = "{first_name}", '
    if last_name is not None:
        query = query + f' last_name = "{last_name}", '
    query = query + f' updated_at = "{updated_at}" WHERE "id" = "{driver_id}"'
    cur.execute(query)
    conn.commit()

    return jsonify(request.get_json())


@app.route('/drivers/driver/<driver_id>/', methods=['DELETE'])
def delete_driver(driver_id):
    log("delete_driver")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(f'UPDATE Vehicle SET driver_id = null WHERE "driver_id" = "{driver_id}" ;')
    cur.execute(f'DELETE FROM Driver WHERE "id" = "{driver_id}" ;')

    conn.commit()

    return jsonify(request.get_json())


@app.route('/vehicles/vehicle/', methods=['GET'])
def vehicles():
    log("vehicles")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    with_drivers = request.args.get('with_drivers')
    if with_drivers is None:
        query = 'SELECT * FROM Vehicle;'
    else:
        if with_drivers == "yes":
            query = " SELECT * FROM `Vehicle` WHERE driver_id IS NOT null; "
        else:
            if with_drivers == "no":
                query = " SELECT * FROM `Vehicle` WHERE driver_id IS null; "
            else:
                return "expected with_drivers yes or no"
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_vehicles = cur.execute(query).fetchall()

    return jsonify(all_vehicles)


@app.route('/vehicles/vehicle/', methods=['POST'])
def add_vehicle():
    log("add_vehicle")
    if not request.is_json:
        return invalid_json_message()

    content = request.get_json()
    driver_id = content.get('driver_id')
    make = content.get('make')
    model = content.get('model')
    plate_number = content.get('plate_number')

    time = now()
    created_at = time
    updated_at = time

    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)
    query = f'INSERT INTO Vehicle (make, model, plate_number, created_at, updated_at) \
              VALUES (""{driver_id}", {make}", "{model}", "{plate_number}", "{created_at}", "{updated_at}");'

    cur = conn.cursor()
    cur.execute(query)
    conn.commit()

    return jsonify(request.get_json())


@app.route('/vehicles/vehicle/<vehicle_id>', methods=['GET'])
def find_vehicle(vehicle_id):
    log("find_vehicle")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    conn.row_factory = dict_factory
    veh = conn.execute("SELECT * FROM `Vehicle` WHERE `id` = ? ", vehicle_id).fetchall()

    return jsonify(veh)


@app.route('/vehicles/vehicle/<vehicle_id>/', methods=['UPDATE'])
def edit_vehicle(vehicle_id):
    log("edit_vehicle")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    if not request.is_json:
        return invalid_json_message()

    content = request.get_json()
    driver_id = content.get('driver_id')
    make = content.get('make')
    model = content.get('model')
    plate_number = content.get('plate_number')
    updated_at = now()

    conn.row_factory = dict_factory
    cur = conn.cursor()

    query = f'UPDATE `Vehicle` SET '
    if driver_id is not None:
        query = query + f' driver_id = "{driver_id}", '
    if make is not None:
        query = query + f' make = "{make}", '
    if model is not None:
        query = query + f' model = "{model}", '
    if plate_number is not None:
        query = query + f' plate_number = "{plate_number}", '
    query = query + f' updated_at = "{updated_at}" WHERE "id" = "{vehicle_id}"'
    cur.execute(query)
    conn.commit()

    return jsonify(request.get_json())


@app.route('/vehicles/vehicle/<vehicle_id>/', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    log("delete_vehicle")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(f'DELETE FROM Vehicle WHERE "id" = "{vehicle_id}" ;')

    conn.commit()

    return jsonify(request.get_json())


@app.route('/vehicles/set_driver/<vehicle_id>/', methods=['POST'])
def set_driver(vehicle_id):
    log("set_driver")
    db_path = os.path.join('create_db', 'DV')
    conn = sqlite3.connect(db_path)

    if not request.is_json:
        return invalid_json_message()

    content = request.get_json()
    driver_id = content.get('driver_id')
    updated_at = now()

    conn.row_factory = dict_factory
    cur = conn.cursor()

    if len(conn.execute(f"SELECT * FROM `Driver` WHERE `id` = '{driver_id}' ").fetchall()) == 0:
        return "no such driver"

    query = f'UPDATE `Vehicle` SET '
    if driver_id is not None:
        query = query + f' driver_id = "{driver_id}", '
    else:
        query = query + f' driver_id = NULL,'
    query = query + f' updated_at = "{updated_at}" WHERE "id" = "{vehicle_id}"'
    cur.execute(query)
    conn.commit()

    return jsonify(request.get_json())


if __name__ == "__main__":
    app.run(debug=False, threaded=True, port=5000)
