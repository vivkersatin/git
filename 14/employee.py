import json
import os

class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

class EmployeeManager:
    def __init__(self, filename='employees.json'):
        self.employees = []
        self.filename = filename
        self.load_employees()
        self.next_id = len(self.employees) + 1  # 自動生成下一個ID

    def load_employees(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                employee_data = json.load(f)
                for emp in employee_data:
                    self.employees.append(Employee(emp['name'], emp['id']))

    def save_employees(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([{'name': emp.name, 'id': emp.id} for emp in self.employees], f, ensure_ascii=False, indent=4)

    def add_employee(self, name):
        new_employee = Employee(name, self.next_id)  # 使用自動生成的ID
        self.employees.append(new_employee)
        self.save_employees()  # 儲存到檔案
        self.next_id += 1  # 更新下一個ID

    def remove_employee(self, id):
        self.employees = [emp for emp in self.employees if emp.id != id]
        self.save_employees()  # 儲存到檔案

    def get_employees(self):
        return self.employees