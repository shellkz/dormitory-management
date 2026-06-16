Dormitory Room Allocation

Description:
A system for managing dorm rooms, resident check-ins/check-outs, and maintenance requests.

Required Basic Functions:
Register / login with role (admin / resident)	#
Add and manage room records and types
Assign rooms and record check-in / check-out
Submit and track maintenance requests
View current occupancy report
Search rooms by status, type, or floor


Suggested Tables:
users
rooms
residents
allocations
maintenance


# Old

User
	id
	type(admin/resident)
	username
	password
	
Room
	id
	type(small/medium/large)
	floor

Stay
	id
	resident_id
	room_id
	check_in_at
	check_out_at

RequestMaintenance
	id
	created_by(user_id)
	room_id
	status(summited/processing/completed)
	created_at
	processing_at
	completed_at
	description
	


# Refined

User
    id          PK
    username    NOT NULL, UNIQUE
    password    NOT NULL
    type        NOT NULL  (admin/resident)

Room
    id          PK
    type        NOT NULL  (small/medium/large)
    floor       NOT NULL

Stay
    id          PK
    resident_id FK → User.id, NOT NULL
    room_id     FK → Room.id, NOT NULL
    check_in_at NOT NULL
    check_out_at  (nullable = 還在住)

RequestMaintenance
    id            PK
    created_by    FK → User.id, NOT NULL
    room_id       FK → Room.id, NOT NULL
    status        NOT NULL  (submitted/processing/completed)
    description   NOT NULL
    created_at    NOT NULL
    processing_at (nullable)
    completed_at  (nullable)

# Desision Making
User

加入 username（UNIQUE）和 password 欄位以支援登入功能
type 欄位區分 admin/resident，role-based permission 在應用層而非 DB 層 enforce

Room

移除原本的 resident_id，因為「目前誰住這間」可從 Stay 推導，存在 Room 會造成資料冗餘與不一致風險
移除 status 欄位，available/occupied/maintaining 皆為 derived state，改用動態 query 根據搜尋條件即時計算

Stay

作為 User 和 Room 的 M:N junction table，同時記錄 check-in/out 歷史
check_out_at nullable，NULL 代表目前仍在住
使用 surrogate PK（id），因為同一 user 可多次入住同一房間，(resident_id, room_id) 無法作為 PK

RequestMaintenance

created_by 而非 resident_id，因為 admin 也能建單
room_id NOT NULL，系統不處理公共區域報修
時間戳拆成 created_at / processing_at / completed_at 三個欄位，分別對應狀態轉換時間點，而非單一 updated_at
使用 surrogate PK，同一 user 可對同一房間提多張單

整體

Stay 和 RequestMaintenance 皆為強實體（有自己的 surrogate PK，不依賴 parent 識別）
所有 participation 皆為 partial（user 可以沒有 stay 記錄、room 可以從未報修等）

