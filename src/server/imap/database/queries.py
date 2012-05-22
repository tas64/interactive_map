from imap.database.DBWrapper import DBWrapper
import converters

class Q:
    SELECT_ALL_IMMOBILES = "SELECT * FROM imap_immobileobject ORDER BY id;"
    SELECT_ALL_MOVABLES  = "SELECT * FROM imap_movableobject ORDER BY id;"
    SELECT_ALL_MOVABLES_WITH_TYPES  = "SELECT imap_movableobject.id, imap_movableobject.name, movable_type_id, \
                                       imap_movabletype.name AS type_name \
                                       FROM imap_movableobject INNER JOIN imap_movabletype ON \
                                       movable_type_id = imap_movabletype.id ORDER BY imap_movableobject.id;"
    SELECT_ALL_MOVABLE_TYPES  = "SELECT * FROM imap_movabletype ORDER BY id;"
    SELECT_ALL_LOCATION_POINTS  = "SELECT * FROM imap_locationpoint ORDER BY id;"

    LOCATION_POINTS_FOR  = "SELECT * FROM imap_locationpoint WHERE movable_object_id = %s ORDER BY time;"


    DELETE_LOCATION_POINTS_FOR  = "DELETE FROM imap_locationpoint WHERE movable_object_id = %s;"

    SEARCH_IMMOBILES = "SELECT * FROM imap_immobileobject WHERE LOWER(name) LIKE '%PATTERN%' ORDER BY id;"
    SEARCH_MOVABLES =  "SELECT imap_movableobject.id, imap_movableobject.name, movable_type_id \
                        FROM imap_movableobject INNER JOIN imap_movabletype ON movable_type_id = imap_movabletype.id \
                        WHERE LOWER(imap_movableobject.name) LIKE '%PATTERN%' OR \
                        LOWER(imap_movabletype.name) LIKE '%PATTERN%' ORDER BY imap_movableobject.id;"

    DELETE_IMMOBILE_OBJECT  = "DELETE FROM imap_immobileobject WHERE id = %s;"
    DELETE_MOVABLE_OBJECT = "DELETE FROM imap_movableobject WHERE id = %s;"
    DELETE_MOVABLE_TYPE = "DELETE FROM imap_movabletype WHERE id = %s;"

    ADD_IMMOBILE_OBJECT = "INSERT INTO imap_immobileobject (name, phone, latitude, longitude) VALUES ('%s', '%s', %s, %s);"
    ADD_MOVABLE_OBJECT = "INSERT INTO imap_movableobject (name, movable_type_id) VALUES ('%s', '%s');"
    ADD_MOVABLE_TYPE = "INSERT INTO imap_movabletype (name) VALUES ('%s');"

    ADD_LOCATION_POINT = "INSERT INTO imap_locationpoint (movable_object_id , time, latitude, longitude) \
                          VALUES (%s, '%s:%s:%s','%s','%s');"

    UPDATE_IMMOBILE_OBJECT = "UPDATE imap_immobileobject SET name = '%s', phone = '%s', latitude = '%s', \
                              longitude = '%s' WHERE id = %s;"
    UPDATE_MOVABLE_OBJECT = "UPDATE imap_movableobject SET name = '%s', movable_type_id = '%s' WHERE id = %s;"
    UPDATE_MOVABLE_TYPE = "UPDATE imap_movabletype SET name = '%s' WHERE id = %s;"

    GET_IMMOBILE_OBJECT = "SELECT * from imap_immobileobject WHERE id = %s LIMIT 1;"
    GET_MOVABLE_OBJECT =  "SELECT * from imap_movableobject WHERE id = %s LIMIT 1;"
    GET_MOVABLE_TYPE =  "SELECT * from imap_movabletype WHERE id = %s LIMIT 1;"


def get_all_movables_objects():
    db_wrapper = DBWrapper()
    movables = db_wrapper.fetch_all(Q.SELECT_ALL_MOVABLES)
    db_wrapper.dispose()
    return map(converters.convert_movable, movables)

def get_all_movables_objects_with_types():
    db_wrapper = DBWrapper()
    movables = db_wrapper.fetch_all(Q.SELECT_ALL_MOVABLES_WITH_TYPES)
    db_wrapper.dispose()
    return map(converters.convert_movable_with_type, movables)

def get_all_movable_types():
    db_wrapper = DBWrapper()
    movable_types = db_wrapper.fetch_all(Q.SELECT_ALL_MOVABLE_TYPES)
    db_wrapper.dispose()
    return map(converters.convert_movable_type, movable_types)

def get_all_immobiles_objects():
    db_wrapper = DBWrapper()
    immobiles = db_wrapper.fetch_all(Q.SELECT_ALL_IMMOBILES)
    db_wrapper.dispose()
    return map(converters.convert_immobile, immobiles)

def get_all_location_points():
    db_wrapper = DBWrapper()
    lps = db_wrapper.fetch_all(Q.SELECT_ALL_LOCATION_POINTS)
    db_wrapper.dispose()
    return map(converters.convert_point, lps)


def search_immobiles_objects(pattern):
    db_wrapper = DBWrapper()
    objects = db_wrapper.fetch_all(Q.SEARCH_IMMOBILES.replace('PATTERN', pattern.strip().lower()))
    db_wrapper.dispose()
    return map(converters.convert_immobile, objects)

def search_movables_objects(pattern):
    db_wrapper = DBWrapper()
    objects = db_wrapper.fetch_all(Q.SEARCH_MOVABLES.replace('PATTERN', pattern.strip().lower()))
    db_wrapper.dispose()
    return map(converters.convert_movable, objects)

def get_all_location_points_for(id):
    points = ()
    try:
        db_wrapper = DBWrapper()
        points = db_wrapper.fetch_all(Q.LOCATION_POINTS_FOR % id)
        db_wrapper.dispose()
    except:
        pass
    return map(converters.convert_point, points)

def delete_all_location_points_for(id):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.DELETE_LOCATION_POINTS_FOR % id)
    db_wrapper.dispose()

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

def delete_movable_object(id):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.DELETE_MOVABLE_OBJECT % id)
    db_wrapper.dispose()
    return True

def add_movable_object(movable_type_id, data):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.ADD_MOVABLE_OBJECT % (data['name'], movable_type_id))
    db_wrapper.dispose()
    return True

def get_movable_object(id):
    db_wrapper = DBWrapper()
    result = db_wrapper.fetch_one(Q.GET_MOVABLE_OBJECT % id)
    db_wrapper.dispose()
    return converters.convert_movable(result)

def update_movable_object(id, movable_type_id, data):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.UPDATE_MOVABLE_OBJECT % (data['name'],movable_type_id, id))
    db_wrapper.dispose()
    return True

def delete_movable_type(id):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.DELETE_MOVABLE_TYPE % id)
    db_wrapper.dispose()
    return True

def add_movable_type(data):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.ADD_MOVABLE_TYPE % (data['name']))
    db_wrapper.dispose()
    return True

def get_movable_type(id):
    db_wrapper = DBWrapper()
    result = db_wrapper.fetch_one(Q.GET_MOVABLE_TYPE % id)
    db_wrapper.dispose()
    return converters.convert_movable_type(result)

def update_movable_type(id, data):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.UPDATE_MOVABLE_TYPE % (data['name'], id))
    db_wrapper.dispose()
    return True

def add_location_point(movable_object_id , hour, minute, second, latitude, longitude):
    db_wrapper = DBWrapper()
    db_wrapper.execute(Q.ADD_LOCATION_POINT % (movable_object_id , hour, minute, second, latitude, longitude))
    db_wrapper.dispose()
