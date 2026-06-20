# Write Up

- 學號：U1224054
- 姓名：王淯霆
- repo：https://github.com/shellkz/dormitory-management

# Schema Design Rationale
Explains schema design decisions and trade-offs.
## Entity and Relation
```
User stay at Room.
User request maintenance for Room.
```
Since User and Room are the beings take and got taken action. They are entities.
On the other hand, Stay and RequestMaintenance are action themself. They are relations.

## Cardinality
But I still need to figure out. Whether Stay and RequestMaintenance are 1 to 1, 1 to N, or N to M.
Based on requirement, I need to keep up stay and maintenance history.
So the scope extends to history-wide.
Let's go back above schema description.
```
User stay at Room.
User request maintenance for Room.
```
Should become
```
Accross history, User stay at Room.
Accross history, User request maintenance for Room.
```
The desision of cardinality is much clear now. Because：
```
Accross history, User can stay at multiple Room.
Accross history, Room can accommodate multiple User.
```
Stay is surely a N to M relation.
Use the same way let's reexamine RequestMaintenance
```
Accross history, User can request maintenance for multiple Room.
Accross history, Room can receive request maintenance from multiple User.
```
Now we can also safely conclude that:
RequestMaintenance is also a N to M relation.

That why I deicde make both of them junction table which use FK point to User and Room.

At this point, we can see overall Relational Model of schema.

That is:
Table                PK         FK
User                 id 
Room                 id
Stay                 id         resident_id -> User.id    room_id -> Room.id        
RequestMaintenance   id         user_id -> User.id        room_id -> Room.id        


## Participation
We can use extended schema description as hint to figure out participation.
```
Accross history, User can stay at multiple Room.
Accross history, Room can accommodate multiple User.
```

Can User never stayed at any Room?
Yes, maybe they just registered. And there is no any Stay record for them.
So User->Stay->Room should be partial participation.

Can Room never accommodated any User?
Yes, maybe it's a new room. And no User ever stayed at.
So Room->Stay->User should be partial participation.

```
Accross history, User can request maintenance for multiple Room.
Accross history, Room can receive request maintenance from multiple User.
```
Can User never request maintenance for Room?
Yes, maybe User simply doesn't want to report or User never encoutered bad Room.
So User->RequestMaintenance->Room should be partial participation.

Can Room never receive request maintenance from any User?
Yes, maybe Room is built perfectly flawlesss. Or User stayed at Room never had a chance to live out that Room. 
So Room->RequestMaintenance->User should be partial participation.

Now we can conclude both Stay and RequestMaintenance's double direction are partial participation.

This also contribute to Relation Model of schema:
That is we now know Stay and RequestMaintenance's FK to User and ROOM could be NULL. 

## Attributes
1. Why Stay carry check_in_at/check_out_at attributes?

I can use them as indicator to whether Room is available or occupied.

If a Room have no correspondant Stay record, that means no User had ever stayed at Room, which means it's empty it's available.

If a Room have correspondant Stay record, but latest record's check_out_at is NULL, that means there is User staying at Room and he hadn't check out, which means Room is occupied.

If a Room have correspondant Stay record, but latest record's check_out_at is not NULL, that means there were indeed some User stayed at Room, but they had checked out. Currently no User staying at Room, which means Room is available.

Because for some User to stay at Room, he must check in. So Stay.check_int_at is NOT NULLABLE.

During his stay, Stay's check_out_at is NULL. It's not until User check out then Stay's check_out_at finally have value. So Stay.check_out_at is NULLABLE.


2. Why RequestMaintenance carry status attribute?

I need to keep track of maintenance progress in 3 phases(submitted/processing/completed). 

So I add this attribute, and updating maintenance progress simply means updating this column to next phase. And this is enforece by Application layer.



## CASCADE DEELTE
Why CASCADE DEELTE Stay/RequestMaintenance(FK) to Room(id) ?

Room and User are solid entities. Stay and RequestMaintenance are relations depend on entities.

So Stay and RequestMaintenance should be deleted if their dependant Room and User get deleted for data integrity.

Given this view, I should setup `ON DELETE CASCADE` constraint for FK in Stay and RequestMaintenance to PK in User and Room.

But since there is no bussiness need for deleting User. I simply setup `ON DELETE CASCADE` constraint for Room.

## CREATE VIEW
Why setup RoomDetailed VIEW?

I need to filter Room with status which is no a column in Room schema. It's a derived column but need to join Stay table to calculate it. 
The query statement alone to get this extended Room is complex enough. Not to mention I have to combine other WHERE filter. So it makes sense to store extended Room query as VIEW and reference it like table. Which makes extended Room query with complex filter a lot easier and clearer.
```sql
SELECT  * 
FROM    RoomDetailed 
WHERE   status = ? AND 
        floor = ?
;
```

## Conclusion
Room and User are entities, which should be stored as table.
Stay and RequestMaintenance are N-M relation, which should also be stored as junction table that use FK referencing User and Room. 

Both Stay and RequestMaintenance are bidirectional partial participation, which means their FK to User and ROOM could be NULL.

Add CASCADE DELETE contraint to Stay and RequestMaintenance's room_id FK, so that when Room get deleted correspondant Stay and RequestMaintenance also get deleted to keep data integrity.

Adopting junction table to store relations make query more complex because we need to JOIN multiple referenced tables. Thats's why I introduce RoomDetailed VIEW to simplify query.


# AI Disclosure
## 所使用之 AI 工具名稱
- Claude Code
## 具體用途
1. Generete layout from conceptual UI structure description
See: `docs/frames.md`
2. Examine hand written db psuedo code.
3. Examine hand written db actuall code.
4. Detect missing edge error case, but only mention me without syntax, I still patched myself.


## 由學生本人獨立理解與實作完成
1. db/feature/view 3 layered archtechture
- db: Database, provide basic sql operation
- feature: API, compose db operations into business logic,  validate parameters, raise meaningful error.
- view: UI, provide user interface to view and operate db with feature layer.

2. db
- Design db schema
- implement db helper scripts

3. feature
- Catch and handle error
- Compose db operation into business logic



# Check List

## Required Basic Functions
1. Register / login with role (admin / resident)
   - 對應程式碼：`db/db.py` 內 `create_user`、`get_user` / `features/auth.py` 內 `login`、`register`
   - 對應UI：LoginRegister Frame

2. Add and manage room records and types
   - 對應程式碼：`db/db.py` 內 `create_room`、`update_room`、`delete_room` / `features/room.py`
   - 對應UI：Room Management Frame

3. Assign rooms and record check-in / check-out
   - 對應程式碼：`db/db.py` 內 `check_in`、`check_out` / `features/assign.py`
   - 對應UI：Assign Room Frame

4. Submit and track maintenance requests
   - 對應程式碼：`db/db.py` / `features/maintenance.py`
   - 對應UI：Maintenance Frame

5. View current occupancy report
   - 對應程式碼：`db/db.py` / `features/report.py`
   - 對應UI：Report Frame

6. Search rooms by status, type, or floor
   - 對應程式碼：`db/db.py` 內 `get_rooms` / `features/room.py` 內 `get_rooms`
   - 對應UI：Room Management Frame（SearchBar）

## Database Design
1. 3+ tables with correct foreign keys
   - 對應程式碼：`db/scripts/001_create_db.sql`（User / Room / Stay / RequestMaintenance）

2. At least one many-to-many via junction table
   - 對應程式碼：`db/scripts/001_create_db.sql`（Stay 作為 User ↔ Room 的 junction table）

3. NOT NULL / UNIQUE constraints
   - 對應程式碼：`db/scripts/001_create_db.sql`（User.username UNIQUE、check_in_at NOT NULL 等）

4. At least one CREATE VIEW used in the app
   - 對應程式碼：`db/scripts/001_create_db.sql` 內 `RoomDetailed` VIEW / `db/db.py` 內 `get_rooms`
   - 對應UI：Room Management Frame

## Application Features
1. Working UI
   - 對應程式碼：`views/`
   - 對應UI：所有 Frame

2. Login function
   - 對應程式碼：`features/auth.py` 內 `login`
   - 對應UI：LoginRegister Frame

3. Role-based access control (admin / resident)
   - 對應程式碼：`views/room_frame.py`（`is_admin` 切換）
   - 對應UI：Room Management Frame（admin 才顯示 Edit/Remove/Create）

4. Search / filter with LIKE or comparison operators
   - 對應程式碼：`db/db.py` 內 `get_maintenance_requests`（LIKE 模糊搜尋）
   - 對應UI：Maintenance Frame（搜尋欄 username輸入框）

5. JOIN-based report view
   - 對應程式碼：`db/db.py` 內 `get_stays`（Stay JOIN Room JOIN User）
   - 對應UI：Report Frame

6. Invalid input handling
   - 對應程式碼：`features/auth.py`、`features/room.py`、`features/assign.py`（ValueError + messagebox）
   - 對應UI：所有Frame的提交表單

## Security
1. Passwords hashed before storage
   - 對應程式碼：`utils/hash.py` / `features/auth.py` 內 `register`（hash 後才存入 DB）

2. Parameterized queries for all user input
   - 對應程式碼：`db/db.py`（所有 `cursor.execute` 皆使用 `?` placeholder）



