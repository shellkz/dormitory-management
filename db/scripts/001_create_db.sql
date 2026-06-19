CREATE TABLE User (
    id              INTEGER     PRIMARY KEY     AUTOINCREMENT,
    username        TEXT        NOT NULL        UNIQUE,
    password        TEXT        NOT NULL,
    role            TEXT        NOT NULL
    

);

CREATE TABLE Room (
    id              INTEGER     PRIMARY KEY     AUTOINCREMENT,
    type            TEXT        NOT NULL,
    floor           INTEGER     NOT NULL

);

CREATE TABLE Stay (
    id              INTEGER     PRIMARY KEY     AUTOINCREMENT,
    resident_id     INTEGER     NOT NULL,
    room_id         INTEGER     NOT NULL,
    check_in_at     TEXT        NOT NULL,
    check_out_at    TEXT,
    
    FOREIGN KEY (resident_id)   REFERENCES User(id),
    FOREIGN KEY (room_id)       REFERENCES Room(id)  ON DELETE CASCADE
);

CREATE TABLE RequestMaintenance (
    id              INTEGER     PRIMARY KEY     AUTOINCREMENT,
    created_by      INTEGER     NOT NULL,
    room_id         INTEGER     NOT NULL,
    status          TEXT        NOT NULL,
    description     TEXT        NOT NULL,
    created_at      TEXT        NOT NULL,
    processing_at   TEXT,
    completed_at    TEXT,

    FOREIGN KEY (created_by)    REFERENCES User(id),
    FOREIGN KEY (room_id)       REFERENCES Room(id)  ON DELETE CASCADE
);

CREATE VIEW RoomDetailed AS
SELECT      Room.id     AS  id, 
            Room.type   AS  type,
            Room.floor  AS  floor,
            CASE
                WHEN Stay.id IS NULL 
                THEN 'available' 
                
                WHEN Stay.check_out_at  IS NULL 
                THEN 'occupied'
                ELSE 'available'
            END         AS  status
FROM        Room
LEFT JOIN   Stay    ON  Stay.room_id = Room.id
                    AND Stay.id = (
                        SELECT      id 
                        FROM        Stay s 
                        WHERE       s.room_id = Room.id
                        ORDER BY    s.id DESC
                        LIMIT       1
                    );
              