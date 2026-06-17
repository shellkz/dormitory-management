
# Requirements
- [x] Register / login with role (admin / resident)	
- [x] Add and manage room records and types          
- [x] Assign rooms and record check-in / check-out
- [x] Submit and track maintenance requests
- [x] View current occupancy report
- [x] Search rooms by status, type, or floor

# What I need to do
For each menu, find out:
1. What table should be shown and operated
2. Component structure 
3. Menu transition

# Frames
## LoginRegister

1. What table should be shown and operated
`user` table
2. Component structure 
```

Vbox
    TabContainer
        LoginTabPanel
            Hbox
                UsernameLabel
                UsernameInput
            Hbox
                PasswordLabel
                PasswordInput
            LoginButton

        RegisterTabPanel
            Hbox
                UsernameLabel
                UsernameInput
            Hbox
                PasswordLabel
                PasswordInput
            Hbox
                ConfirmPasswordLabel
                ConfirmPasswordInput
            RegisterButton

```
3. Menu transition
```
When LoginButton pressed
    if user.canLogin()
        login with username and role
        goto MainFrame
    else
        show error message 

When RegisterButton pressed
    if user.canRegsiter()
        login with username and role
        goto MainFrame
    else
        show error message 
```


## ManageRoom

0. Functionality
- admin: CRUD room
- resident: search room

1. What table should be shown and operated
`room`
2. Component structure 
```

```
```
ManageRoomFrame (CTkFrame)
    SearchBar (CTkFrame)
        Hbox
            StatusOptionMenu    ← available/occupied/maintaining
            TypeOptionMenu      ← small/medium/large
            FloorEntry
            SearchButton
            ResetButton

    CTkScrollableFrame
        RoomItem (CTkFrame) × N

    [admin only]
    CreateRoomForm (CTkFrame)
        Hbox
            TypeOptionMenu
            FloorEntry
            CreateButton
```

```
RoomItem
    Hbox
        IdLabel
        [view 模式]
            TypeLabel
            FloorLabel
            [admin only] EditButton
            [admin only] RemoveButton

        [edit 模式, admin only]
            TypeOptionMenu
            FloorEntry
            ConfirmButton
            CancelButton
```



## AssignRoomFrame
0. Functionality
Let admin check-in/out resident into/from room

1. What table should be shown and operated
`stay`、`room`
2. Component structure 
```
CheckInOutFrame (CTkFrame)
    CTkScrollableFrame
        AssignRoomItem (CTkFrame) × N

AssignRoomItem (CTkFrame)
    Hbox
        IdLabel
        TypeLabel
        FloorLabel

        [空房模式]
        ResidentOptionMenu    ← 列出無 active stay 的 resident
        CheckInButton

        [有人住模式]
        ResidentLabel         ← 目前住客 username
        CheckInAtLabel        ← check_in_at
        CheckOutButton
```





## RequestMaintenanceFrame

0. Functionality
- admin:  submit request/query all request / update request progress
- resident: submit request/query self request

1. What table should be shown and operated
`RequestMaintenance` `Room` 


2. Component structure 
```
MaintenanceFrame (admin)
    CTkScrollableFrame
        AdminMaintenanceItem (CTkFrame) × N

AdminMaintenanceItem (CTkFrame)
    Hbox
        IdLabel
        RoomLabel
        SubmitterLabel
        DescriptionLabel

        [submitted 模式]
        SubmittedAtLabel        ← 提交於 xxx
        ProcessButton           ← 按下 → processing

        [processing 模式]
        SubmittedAtLabel        ← 提交於 xxx
        ProcessingAtLabel       ← 受理於 xxx
        CompleteButton          ← 按下 → completed

        [completed 模式]
        SubmittedAtLabel        ← 提交於 xxx
        ProcessingAtLabel       ← 受理於 xxx
        CompletedAtLabel        ← 完成於 xxx
```

MaintenanceFrame (resident)
    CreateMaintenanceForm (CTkFrame)
        Hbox
            RoomLabel           ← 目前住的房間 id/type/floor
            DescriptionEntry
            SubmitButton

    CTkScrollableFrame
        ResidentMaintenanceItem (CTkFrame) × N

ResidentMaintenanceItem (CTkFrame)
    Hbox
        IdLabel
        RoomLabel
        DescriptionLabel

        [submitted 模式]
        SubmittedAtLabel        ← 提交於 xxx

        [processing 模式]
        SubmittedAtLabel        ← 提交於 xxx
        ProcessingAtLabel       ← 受理於 xxx

        [completed 模式]
        SubmittedAtLabel        ← 提交於 xxx
        ProcessingAtLabel       ← 受理於 xxx
        CompletedAtLabel        ← 完成於 xxx
3. Menu transition




## ReportFrame
0. Function
- admin: View current occupancy report
- resident: cannot access

1. What table should be shown and operated
`stay` `rooms`

2. Component structure
```
ReportFrame (CTkFrame)
    Vbox
        TotalRoomsLabel         ← 總房間數：xx 間
        OccupiedLabel           ← 已入住：xx 間
        AvailableLabel          ← 空房：xx 間
        OccupancyRateBar:CTkProgressBar          ← 入住比例圖
        OccupancyRateLabel      ← xx%


```
