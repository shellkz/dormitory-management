# Requirements

| Python | Version |
|--------|---------|
| Minimum | 3.10+ |
| Tested | 3.14 |

# Run
1. Windows
```bash
git clone https://github.com/shellkz/dormitory-management.git
cd dormitory-management
python -m venv venv
venv\Scripts\activate        
pip install -r requirements.txt
python main.py
```

2. Linux and Mac
```bash
git clone https://github.com/shellkz/dormitory-management.git
cd dormitory-management
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

# Default users for test
1. admin
- username: `admin`
- password: `admin`

2. resident
- username: `resident`
- password: `resident`



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


