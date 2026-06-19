# Term Project Specification — Database Management Systems

**National United University · Dept. of CSIE**
Instructor: Yu-Wei Wen · Semester: 114-2 · Total: 100 pts
Individual project · Choose one scenario · See requirements and scoring below

---

## ⚠️ 學術誠信聲明 — 生成式 AI 使用規範

本課程**允許**使用生成式 AI 工具（如 ChatGPT、Claude、GitHub Copilot 等），但須於期末報告中附上完整的 **AI 使用聲明**，並明確說明下列事項：

- 所使用之 AI 工具名稱（請逐一列出）
- 每項工具的*具體用途*（例如：「使用 Claude 產生初版 ER 圖，並自行修改後定稿」）
- 說明哪些部分由學生本人獨立理解與實作完成

**若繳交之作品明顯由 AI 全程生成，且缺乏個人理解與實作之跡象，該作業將以零分計算。** 如於展示過程中無法自行解釋程式碼或資料庫設計決策，無論是否已提交聲明，均視同違反學術誠信。

未聲明擅自使用 AI 工具，屬違反本校學術誠信規範之行為，情節嚴重者將依校規處理。

---

## Step 1 — Choose Your Scenario

### 💰 Personal Finance Tracker
A system for managing personal income, expenses, and budgets across multiple categories and accounts.

**Required Basic Functions**
- Register / login with role (admin / member)
- Add, edit, delete income & expense records
- Manage and assign spending categories
- Set and track monthly budgets per category
- View account balance summary report
- Search transactions by date range or keyword

**Suggested Tables:** `users` `accounts` `transactions` `categories` `budgets`

---

### 📦 Inventory Management
A small-shop system tracking products, suppliers, stock levels, and purchase/sale transactions.

**Required Basic Functions**
- Register / login with role (manager / staff)
- Add, edit, delete products and categories
- Record stock-in and stock-out transactions
- Link products to one or more suppliers
- View low-stock alert report
- Search products by name or category

**Suggested Tables:** `users` `products` `suppliers` `orders` `product_supplier`

---

### 🏠 Dormitory Room Allocation
A system for managing dorm rooms, resident check-ins/check-outs, and maintenance requests.

**Required Basic Functions**
- Register / login with role (admin / resident)
- Add and manage room records and types
- Assign rooms and record check-in / check-out
- Submit and track maintenance requests
- View current occupancy report
- Search rooms by status, type, or floor

**Suggested Tables:** `users` `rooms` `residents` `allocations` `maintenance`

---

## Step 2 — Requirements

### 🗄️ Database Design
- Must have **at least 3 related tables** connected with proper foreign keys
- Must include **at least one many-to-many relationship** implemented via a junction/bridge table
- Must use `NOT NULL` or `UNIQUE` constraints where logically appropriate (e.g., usernames, emails)
- Must create **at least one SQL VIEW** (virtual table) used for data retrieval in the application
- Must draw an ER diagram **by hand** showing all entities, attributes, and relationships with correct notation. *Students are solely responsible for the image quality and readability — illegible diagrams will not be graded.*

### 🖥️ Application Features
- Must implement a **working UI** — text-based (console menu), GUI (e.g., Tkinter), or web UI
- Must implement a **login function** that authenticates users before granting access
- Must implement **role-based access control** with at least 2 distinct roles (e.g., admin vs. regular user) with different menu options and permissions
- Must implement **at least one search or filter feature** using `LIKE` or comparison operators (`<`, `>`, `BETWEEN`, etc.)
- Must implement **at least one report view** that retrieves data using a `JOIN` across 2 or more tables
- Must **gracefully handle invalid input** — the program must not crash on bad data; show a clear error message instead

### 🔐 Security
- Passwords must be **hashed** before storage — never stored as plain text (e.g., use `hashlib` or `bcrypt`)
- Must use **parameterized queries** (with `?` placeholders) for all user-supplied input — no f-string or string concatenation for SQL with user data

---

## Step 3 — Scoring (100 Points)

| Category | Graded Items | Points |
|----------|-------------|--------|
| 🗄️ Database Design | 3+ tables with correct foreign keys; at least one many-to-many (junction table); appropriate `NOT NULL` / `UNIQUE` constraints; at least one `CREATE VIEW` used in the app | 25 |
| 🖥️ Application & Features | Working UI; login flow; role-based menus (2+ roles); search/filter with `LIKE` or operators; JOIN-based report; input error handling without crashes | 25 |
| 🔐 Security | Hashed passwords (no plain text); all user input goes through parameterized queries; role permissions enforced at runtime | 20 |
| 📐 ER Diagram | Hand-drawn; correct entities, attributes, and relationships; proper notation (PK underlined, cardinality marked); matches actual schema; image must be clear and legible | 10 |
| 📄 Write-up | 3–4 pages; explains schema design decisions and trade-offs; includes AI 使用聲明 with specific tool names and usage descriptions | 10 |
| 🎬 Demo Video | Under 3 minutes; shows login for each role; demonstrates core features (search, report, CRUD); narration or on-screen text explains what is happening | 10 |
| **Total** | | **100** |

---

## Step 4 — Submission Checklist

**1. Source Code**
All `.py` files and the `.db` file. Include a `README.md` or `README.txt` with instructions on how to run the program.

**2. ER Diagram**
A photo or scan of your **hand-drawn** ER diagram. You are responsible for image clarity — blurry or illegible submissions will not be graded. Submit as `.jpg` or `.pdf`.

**3. Write-up**
3–4 pages as `.pdf`. Must include schema design rationale **and** an AI 使用聲明 section.

**4. Demo Video**
Under 3 minutes. Upload to YouTube (unlisted) or submit as `.mp4`. Must show both roles in action.

---

*Database Management Systems · Semester 114-2 · National United University · Dept. of CSIE · Instructor: Yu-Wei Wen*
