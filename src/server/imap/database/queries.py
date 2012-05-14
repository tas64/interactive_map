from imap.database.DBWrapper import DBWrapper
import converters

class Q:
    SELECT_ALL_IMMOBILES = "SELECT * FROM imap_immobileobject ORDER BY id;"
    SELECT_ALL_MOVABLES  = "SELECT * FROM imap_movableobject ORDER BY id;"
    LOCATION_POINTS_FOR  = "SELECT * FROM imap_locationpoint WHERE movable_object_id = %s ORDER BY id;"

    DELETE_IMMOBILE_OBJECT  = "DELETE FROM imap_immobileobject WHERE id = %s;"
    ADD_IMMOBILE_OBJECT = "INSERT INTO imap_immobileobject (name, phone, latitude, longitude) VALUES ('%s', '%s', %s, %s);"
    UPDATE_IMMOBILE_OBJECT = "UPDATE imap_immobileobject SET name = '%s', phone = '%s', latitude = '%s', longitude = '%s' WHERE id = %s;";
    GET_IMMOBILE_OBJECT = "SELECT * from imap_immobileobject WHERE id = %s;"


def get_all_movables_objects():
    db_wrapper = DBWrapper()
    movables = db_wrapper.fetch_all(Q.SELECT_ALL_MOVABLES)
    db_wrapper.dispose()
    return map(converters.convert_movable, movables)

def get_all_immobiles_objects():
    db_wrapper = DBWrapper()
    immobiles = db_wrapper.fetch_all(Q.SELECT_ALL_IMMOBILES)
    db_wrapper.dispose()
    return map(converters.convert_immobile, immobiles)

def get_all_location_points_for(id):
    points = ()
    try:
        db_wrapper = DBWrapper()
        points = db_wrapper.fetch_all(Q.LOCATION_POINTS_FOR % id)
        db_wrapper.dispose()
    except:
        pass
    return map(converters.convert_point, points)

def delete_immobile_object(id):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.DELETE_IMMOBILE_OBJECT % id)
    db_wrapper.dispose()
    return True

def add_immobile_object(data):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.ADD_IMMOBILE_OBJECT % (data['name'], data.get('phone', ''), data['latitude'], data['longitude']))
    db_wrapper.dispose()
    return True

def update_immobile_object(id, data):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.UPDATE_IMMOBILE_OBJECT % (data['name'], data.get('phone', ''), data['latitude'], data['longitude'], id))
    db_wrapper.dispose()
    return True

def get_immobile_object(id):
    db_wrapper = DBWrapper()
    result = db_wrapper.fetch_one(Q.GET_IMMOBILE_OBJECT % id)
    db_wrapper.dispose()
    return converters.convert_immobile(result)