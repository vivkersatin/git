import json
import os

class Attendance:
    def __init__(self, employee_id, date, status):
        self.employee_id = employee_id
        self.date = date
        self.status = status

class AttendanceManager:
    def __init__(self, filename='attendance.json'):
        self.attendance_records = []
        self.filename = filename
        self.load_attendance()

    def load_attendance(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                attendance_data = json.load(f)
                for record in attendance_data:
                    self.attendance_records.append(Attendance(record['employee_id'], record['date'], record['status']))

    def save_attendance(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([{'employee_id': record.employee_id, 'date': record.date, 'status': record.status} for record in self.attendance_records], f, ensure_ascii=False, indent=4)

    def record_attendance(self, employee_id, date, status):
        # 檢查該員工在該日期的考勤是否已存在
        existing_record = next((record for record in self.attendance_records if record.employee_id == employee_id and record.date == date), None)
        if existing_record:
            print(f"員工ID {employee_id} 在 {date} 的考勤記錄已存在，無法重複記錄。")
            return  # 不執行重複記錄的操作

        new_record = Attendance(employee_id, date, status)
        self.attendance_records.append(new_record)
        self.save_attendance()  # 儲存到檔案

    def get_attendance_records(self):
        return self.attendance_records