1. Discover schema from requirement
- ER model (done)
- Relational model (done)
- Create table instruction (PK/FK/Other constraints）(done)

2. Reflect schema with menus(done)
   For each menu, find out:
   	1. What table should be shown and operated
   	2. Component structure 
   	3. Menu transition

3. Implment required business logic(done)
4. Bind business logic to menu(done)
5. Test(done)
	3, 4, 5 should be conducted in functionality group manner





---

## 必做缺漏
### Navigation
1. APP is composed of SideNavigation(old main_frame) and RightContentPanel(other frames) [done]

### A. SQL VIEW（Database Design 25分）[done]
要求 at least one `CREATE VIEW` used in the app，目前完全沒有。
- 建議：`RoomStatusView`（JOIN Room + Stay 推導 occupied/available）
- 或把 `get_maintenance_requests` 的 JOIN 改成 VIEW
1. Room search filter(all/occupied/available)


### B. LIKE 搜尋（Application Features 25分）[done]
要求 at least one search using `LIKE` or comparison operators，目前全部是 `= ?` 完全匹配。
- 建議：maintenance viewer 的 username 搜尋改成 `LIKE ?`（加 % 模糊搜）

### C. Many-to-many junction table（Database Design 25分） [done]
要求 at least one many-to-many via junction table。
- `Stay` 連接 User ↔ Room，屬於 associative entity，應可算數，但要在 write-up 中說明清楚。

---

## 選做改善
1. 統一用表單提交觸發DB操作(雖然是退後 但統一)
2. 統一排版，由上到下分別是
```
TabContainer
	TabForSomeAction
		InputField
		Button
	TabForOtherActions
		...
	List
		Item
		Item
		...
```
3. ListView預製Item分頁提供內容(很慢)

## 墳場
1. Logout 

## 非程式項目

| 項目 | 說明 | 分數 | 完成 |
|------|------|------|------|
| ER Diagram | 手繪，PK 底線，標示 cardinality，需清晰可讀 | 10 | O |
| Write-up | 3–4 頁 PDF，含 schema 設計說明 + AI 使用聲明 | 10 |  |
| Demo Video | 3 分鐘內，展示 admin/resident 兩種角色操作 | 10 |  |
| README | 說明如何執行程式 | — |  |
