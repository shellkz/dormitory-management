
1. Create table
2. Add mocking data
3. Define dataclass object
4. Implment features

# 1. Auth
```
canRegister(username, password)
    username 不為空
    password 不為空
    username 不重複 (查 DB)

register(username, password)
    hash password
    insert User  (role 寫死 resident)

canLogin(username, password)
    username 存在
    password 正確

login(username, password)
    → 回傳 User (含 role)
```