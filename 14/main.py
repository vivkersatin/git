from datetime import datetime, timedelta

# main.py
# 這是HR系統的主程式檔案

from employee import EmployeeManager
from attendance import AttendanceManager

def add_employee(employee_manager):
    name = input("請輸入員工姓名: ")
    employee_manager.add_employee(name)  # 只傳遞姓名
    print(f"員工 {name} 已成功新增！")

def remove_employee(employee_manager):
    id = int(input("請輸入要刪除的員工ID: "))
    employee_manager.remove_employee(id)
    print(f"員工ID {id} 已成功刪除！")

def view_employees(employee_manager):
    employees = employee_manager.get_employees()
    if not employees:
        print("目前沒有任何員工資料。")
    else:
        print("已新增的員工:")
        for emp in employees:
            print(f"姓名: {emp.name}, ID: {emp.id}")

def record_attendance(attendance_manager):
    employee_id = int(input("請輸入員工ID: "))
    
    # 提供日期選擇
    print("請選擇考勤日期:")
    today = datetime.now()
    date_options = [today + timedelta(days=i) for i in range(7)]  # 接下來7天的日期
    for i, date in enumerate(date_options):
        print(f"{i + 1}. {date.strftime('%Y-%m-%d')}")
    
    date_choice = int(input("請選擇日期 (1-7): ")) - 1
    date = date_options[date_choice].strftime('%Y-%m-%d')
    
    # 提供狀態選擇
    print("請選擇考勤狀態:")
    print("1. 出勤")
    print("2. 缺勤")
    status_choice = int(input("請選擇狀態 (1-2): "))
    status = "出勤" if status_choice == 1 else "缺勤"
    
    attendance_manager.record_attendance(employee_id, date, status)
    print(f"員工ID {employee_id} 的考勤已成功記錄！")

def view_attendance(attendance_manager):
    records = attendance_manager.get_attendance_records()
    if not records:
        print("目前沒有任何考勤資料。")
    else:
        print("考勤記錄:")
        for record in records:
            print(f"員工ID: {record.employee_id}, 日期: {record.date}, 狀態: {record.status}")

def main():
    # 初始化員工管理和考勤管理
    employee_manager = EmployeeManager()
    attendance_manager = AttendanceManager()

    while True:
        print("1. 新增員工")
        print("2. 查詢員工")
        print("3. 刪除員工")
        print("4. 記錄考勤")
        print("5. 查詢考勤")
        print("6. 退出")
        choice = input("請選擇操作: ")

        if choice == '1':
            add_employee(employee_manager)
        elif choice == '2':
            view_employees(employee_manager)
        elif choice == '3':
            remove_employee(employee_manager)
        elif choice == '4':
            record_attendance(attendance_manager)
        elif choice == '5':
            view_attendance(attendance_manager)
        elif choice == '6':
            break
        else:
            print("無效的選擇，請再試一次。")

if __name__ == "__main__":
    main()