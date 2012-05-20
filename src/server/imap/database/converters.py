def convert_movable(object):
    id, name, movable_type_id = object
    return {'id' : id, 'name' : name, 'movable_type_id' : movable_type_id}

def convert_movable_with_type(object):
    id, name, movable_type_id, type_name = object
    return {'id' : id, 'name' : name, 'movable_type_id' : movable_type_id, 'type_name' : type_name}

def convert_movable_type(object):
    id, name = object
    return {'id' : id, 'name' : name}

def convert_immobile(object):
    id, name, phone, latitude, longitude = object
    return {'id' : id, 'name' : name, 'phone' : phone, 'latitude' : latitude, 'longitude' : longitude}

def convert_point(object):
    id, movable_id, time, latitude, longitude = object
    hour = time.hour
    minute = time.minute
    second = float("%d.%d" % (time.second, time.microsecond) )
    return {'id' : id, 'movable_id' : movable_id, 'hour' : hour, 'minute' : minute, 'second' : second, 'latitude' : latitude, 'longitude' : longitude}
