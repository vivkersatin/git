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

def main():
    # 初始化員工管理和考勤管理
    employee_manager = EmployeeManager()
    attendance_manager = AttendanceManager()

    while True:
        print("1. 新增員工")
        print("2. 查詢員工")
        print("3. 刪除員工")
        print("4. 退出")
        choice = input("請選擇操作: ")

        if choice == '1':
            add_employee(employee_manager)
        elif choice == '2':
            view_employees(employee_manager)
        elif choice == '3':
            remove_employee(employee_manager)
        elif choice == '4':
            break
        else:
            print("無效的選擇，請再試一次。")

if __name__ == "__main__":
    main()