# 1. User Identity
**決策**：`username` `role` store at  `class App(ctk.CTk)` as member variable

**原因**：
- 
**定義**：
```python
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.current_user = null

```
**用起來**
```
when login
    app.current_user = user object from query
```

# 2. Data Class 映射查詢結果

**決策**：SQLite 查詢結果統一映射成 `dataclass`，不直接使用 `dict`。

**原因**：
- 屬性存取有 IDE autocomplete，打錯名稱編譯期即可發現
- 型別標註明確，結構一目瞭然

**定義**：
```python
# models/user.py
from dataclasses import dataclass

@dataclass
class User:
    id: int
    username: str
    type: str  # "admin" | "resident"
```

**用起來**：
```python
user = auth.login("admin", "1234")
print(user.type)      # "admin"
print(user.username)  # "admin"
```

---

# 3. Feature 層封裝 Business Logic

**決策**：SQL 操作封裝在 `features/` 各模組，`views/` 不直接寫 SQL。

**原因**：
- 畫面與資料邏輯分離，各自修改互不影響
- SQL 集中管理，查詢邏輯不散落在各個 Frame
- 回傳 dataclass，views 層不需要知道 DB 結構

**結構**：
```
features/
    auth.py         ← login, register
    room.py         ← get_rooms, create_room, update_room, delete_room
    stay.py         ← checkin, checkout, get_active_stay
    maintenance.py  ← submit, update_status, get_all, get_by_resident
    report.py       ← get_occupancy_stats
```

**定義**：
```python
# features/room.py
from db import get_connection
from models.room import Room

def get_rooms(floor=None, type=None) -> list[Room]:
    pass
```

**用起來**：
```python
# views/manage_room_frame.py
from features.room import get_rooms, create_room, delete_room

rooms = get_rooms(floor=3, type="small")  # List[Room]
for room in rooms:
    RoomItem(self, room=room)
```