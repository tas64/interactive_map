def convert_movable(object):
    id, name, movable_type_id, points_counter = object
    return {'id' : id, 'name' : name, 'movable_type_id' : movable_type_id, 'points_counter' : points_counter}

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
    if hour < 10:
        hour = "0" + str(hour)
    minute = time.minute
    if minute < 10:
        minute = "0" + str(minute)
    s, ms = time.second, time.microsecond
    if s < 10 and ms == 0:
        s = "0" + str(s)
    second = str(s)
    if ms > 0:
        second +=".%s" % str(ms)[:2]
    return {'id' : id, 'movable_id' : movable_id, 'hour' : hour, 'minute' : minute, 'second' : second, 'latitude' : latitude, 'longitude' : longitude}
