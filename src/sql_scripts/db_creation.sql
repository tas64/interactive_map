DROP TABLE IF EXISTS imap_immobileobject;
DROP TABLE IF EXISTS imap_locationpoint;
DROP TABLE IF EXISTS imap_movableobject;
DROP TABLE IF EXISTS imap_movabletype;

CREATE TABLE "imap_immobileobject" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" text NOT NULL,
    "phone" text,
    "latitude" double precision NOT NULL,
    "longitude" double precision NOT NULL,
    UNIQUE (name, latitude, longitude)
)
;
CREATE TABLE "imap_movabletype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" text NOT NULL,
    UNIQUE (name)
)
;
CREATE TABLE "imap_movableobject" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" text NOT NULL,
    "movable_type_id" integer NOT NULL REFERENCES "imap_movabletype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "points_counter" integer DEFAULT 0,
    UNIQUE (name, movable_type_id)
)
;
CREATE TABLE "imap_locationpoint" (
    "id" serial NOT NULL PRIMARY KEY,
    "movable_object_id" integer NOT NULL REFERENCES "imap_movableobject" ("id") ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED,
    "time" time NOT NULL,
    "latitude" double precision NOT NULL,
    "longitude" double precision NOT NULL,
    UNIQUE (movable_object_id, time, latitude, longitude)
)
;


CREATE LANGUAGE plpgsql;

--coords validator1
DROP TRIGGER IF EXISTS coords_validator1 ON imap_immobileobject;
DROP FUNCTION IF EXISTS func_validator1() CASCADE;

CREATE FUNCTION func_validator1() RETURNS trigger AS $$
    DECLARE
        _longitude double precision := NEW.longitude;
    BEGIN
        IF (NEW.latitude > 90) THEN
            UPDATE imap_immobileobject
                SET latitude = 90
                WHERE id = NEW.id;

        ELSIF (NEW.latitude < -90) THEN
            UPDATE imap_immobileobject
                SET latitude = -90
                WHERE id = NEW.id;
        END IF;

        IF (_longitude > 180) THEN
            LOOP
                _longitude = _longitude - 360;
                IF _longitude <= 180 THEN
                    EXIT;
                END IF;
            END LOOP;
        ELSIF (_longitude < -180) THEN
            LOOP
                _longitude = _longitude + 360;
                IF _longitude >= -180 THEN
                    EXIT;
                END IF;
            END LOOP;
        ELSE
            RETURN NEW;
        END IF;

        UPDATE imap_immobileobject
            SET longitude = _longitude
            WHERE id = NEW.id;
        RETURN NEW;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER coords_validator1
    AFTER INSERT
    ON imap_immobileobject
    FOR EACH ROW
    EXECUTE PROCEDURE func_validator1();


--coords validator2
DROP TRIGGER IF EXISTS coords_validator2 ON imap_locationpoint;
DROP FUNCTION IF EXISTS func_validator2() CASCADE;

CREATE FUNCTION func_validator2() RETURNS trigger AS $$
    DECLARE
        _longitude double precision := NEW.longitude;
    BEGIN
        IF (NEW.latitude > 90) THEN
            UPDATE imap_immobileobject
                SET latitude = 90
                WHERE id = NEW.id;

        ELSIF (NEW.latitude < -90) THEN
            UPDATE imap_immobileobject
                SET latitude = -90
                WHERE id = NEW.id;
        END IF;

        IF (_longitude > 180) THEN
            LOOP
                _longitude = _longitude - 360;
                IF _longitude <= 180 THEN
                    EXIT;
                END IF;
            END LOOP;
        ELSIF (_longitude < -180) THEN
            LOOP
                _longitude = _longitude + 360;
                IF _longitude >= -180 THEN
                    EXIT;
                END IF;
            END LOOP;
        ELSE
            RETURN NEW;
        END IF;

        UPDATE imap_locationpoint
            SET longitude = _longitude
            WHERE id = NEW.id;
        RETURN NEW;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER coords_validator2
    AFTER INSERT
    ON imap_locationpoint
    FOR EACH ROW
    EXECUTE PROCEDURE func_validator2();


--points counter
DROP TRIGGER IF EXISTS movableobject_points_counter ON imap_locationpoint;
DROP FUNCTION IF EXISTS func_counter() CASCADE;

CREATE FUNCTION func_counter() RETURNS trigger AS $$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            UPDATE imap_movableobject
                SET points_counter = points_counter - 1
                WHERE imap_movableobject.id = OLD.movable_object_id;
            RETURN OLD;

        ELSIF (TG_OP = 'INSERT') THEN
            UPDATE imap_movableobject
                SET points_counter = points_counter + 1
                WHERE imap_movableobject.id = NEW.movable_object_id;
            RETURN NEW;
        END IF;
        RETURN NULL;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER movableobject_points_counter
    AFTER INSERT OR DELETE
    ON imap_locationpoint
    FOR EACH ROW
    EXECUTE PROCEDURE func_counter();


--cascade deleter
DROP TRIGGER IF EXISTS movableobject_deleter ON imap_movabletype;
DROP FUNCTION IF EXISTS func_deleter() CASCADE;

CREATE FUNCTION func_deleter() RETURNS trigger AS $$
    BEGIN
    	DELETE FROM imap_movableobject
	        WHERE imap_movableobject.movable_type_id = OLD.id;            
        RETURN NULL;
    END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER movableobject_deleter
    AFTER DELETE
    ON imap_movabletype
    FOR EACH ROW
    EXECUTE PROCEDURE func_deleter();



CREATE USER test_user WITH password 'test_pass';
GRANT SELECT, INSERT, UPDATE, DELETE 
    ON imap_immobileobject, imap_movabletype, imap_movableobject, imap_locationpoint
    TO test_user;
