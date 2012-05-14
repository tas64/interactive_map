def convert_movable(object):
    id, name, type = object
    return {'id' : id, 'name' : name, 'type' : type}

def convert_immobile(object):
    id, name, phone, latitude, longitude = object
    return {'id' : id, 'name' : name, 'phone' : phone, 'latitude' : latitude, 'longitude' : longitude}

def convert_point(object):
    id, movable_id, hour, minute, second, latitude, longitude = object
    return {'id' : id, 'movable_id' : movable_id, 'hour' : hour, 'minute' : minute, 'second' : second,
                   'latitude' : latitude, 'longitude' : longitude}
