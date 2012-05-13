class Q:
    SELECT_ALL_IMMOBILES = "SELECT * FROM imap_immobileobject;"
    SELECT_ALL_MOVABLES  = "SELECT * FROM imap_movableobject;"
    LOCATION_POINTS_FOR  = "SELECT * FROM imap_locationpoint WHERE movable_object_id = %s;"