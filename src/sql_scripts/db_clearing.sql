--coords validator1
DROP TRIGGER IF EXISTS coords_validator1 ON imap_immobileobject;
DROP FUNCTION IF EXISTS func_validator1() CASCADE;

--coords validator2
DROP TRIGGER IF EXISTS coords_validator2 ON imap_locationpoint;
DROP FUNCTION IF EXISTS func_validator2() CASCADE;

--points counter
DROP TRIGGER IF EXISTS movableobject_points_counter ON imap_locationpoint;
DROP FUNCTION IF EXISTS func_counter() CASCADE;

--cascade deleter
DROP TRIGGER IF EXISTS movableobject_deleter ON imap_movabletype;
DROP FUNCTION IF EXISTS func_deleter() CASCADE;

DROP TABLE IF EXISTS imap_immobileobject;
DROP TABLE IF EXISTS imap_locationpoint;
DROP TABLE IF EXISTS imap_movableobject;
DROP TABLE IF EXISTS imap_movabletype;

