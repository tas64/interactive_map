BEGIN;
CREATE TABLE "imap_immobileobject" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" text NOT NULL,
    "phone" text,
    "latitude" double precision NOT NULL,
    "longitude" double precision NOT NULL
)
;
CREATE TABLE "imap_movabletype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" text NOT NULL
)
;
CREATE TABLE "imap_movableobject" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" text NOT NULL,
    "movable_type_id" integer NOT NULL REFERENCES "imap_movabletype" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "imap_locationpoint" (
    "id" serial NOT NULL PRIMARY KEY,
    "movable_object_id" integer NOT NULL REFERENCES "imap_movableobject" ("id") DEFERRABLE INITIALLY DEFERRED,
    "hour" integer NOT NULL,
    "minute" integer NOT NULL,
    "second" double precision NOT NULL,
    "latitude" double precision NOT NULL,
    "longitude" double precision NOT NULL
)
;
CREATE INDEX "imap_movableobject_movable_type_id" ON "imap_movableobject" ("movable_type_id");
CREATE INDEX "imap_locationpoint_movable_object_id" ON "imap_locationpoint" ("movable_object_id");
COMMIT;
