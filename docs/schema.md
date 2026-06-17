# Dormitory Room Allocation

# Requirement
## Description
A system for managing dorm rooms, resident check-ins/check-outs, and maintenance requests.

## Required Basic Functions:
1. Register / login with role (admin / resident)	
1. Add and manage room records and types
1. Assign rooms and record check-in / check-out
1. Submit and track maintenance requests
1. View current occupancy report
1. Search rooms by status, type, or floor

## Suggested Tables:
1. users
1. rooms
1. residents
1. allocations
1. maintenance


# Schema
```
User
    id          PK
    username    NOT NULL, UNIQUE
    password    NOT NULL
    role        NOT NULL  (admin/resident)
```
```
Room
    id          PK
    type        NOT NULL  (small/medium/large)
    floor       NOT NULL
```
```
Stay
    id          PK
    resident_id FK → User.id, NOT NULL
    room_id     FK → Room.id, NOT NULL
    check_in_at NOT NULL
    check_out_at  (nullable = 還在住)
```
```
RequestMaintenance
    id            PK
    created_by    FK → User.id, NOT NULL
    room_id       FK → Room.id, NOT NULL
    status        NOT NULL  (submitted/processing/completed)
    description   NOT NULL
    created_at    NOT NULL
    processing_at (nullable)
    completed_at  (nullable)
```
# Desision Making
## User

1. 加入 username（UNIQUE）和 password 欄位以支援登入功能
2. role 欄位區分 admin/resident，role-based permission 在應用層而非 DB 層 enforce

## Room

1. 移除原本的 resident_id，因為「目前誰住這間」可從 Stay 推導，存在 Room 會造成資料冗餘與不一致風險
1. 移除 status 欄位，available/occupied/maintaining 皆為 derived state，改用動態 query 根據搜尋條件即時計算

## Stay

1. 作為 User 和 Room 的 M:N junction table，同時記錄 check-in/out 歷史
2. check_out_at nullable，NULL 代表目前仍在住
使用 surrogate PK（id），因為同一 user 可多次入住同一房間，(resident_id, room_id) 無法作為 PK

## RequestMaintenance

1. created_by 而非 resident_id，因為 admin 也能建單
2. room_id NOT NULL，系統不處理公共區域報修
時間戳拆成 created_at / processing_at / completed_at 三個欄位，分別對應狀態轉換時間點，而非單一 updated_at
3. 使用 surrogate PK，同一 user 可對同一房間提多張單


