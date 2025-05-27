# attendance.py
# 考勤系統功能

class Attendance:
    def __init__(self, employee_id, date, status):
        self.employee_id = employee_id
        self.date = date
        self.status = status

class AttendanceManager:
    def __init__(self):
        self.attendance_records = []

    def record_attendance(self, employee_id, date, status):
        new_record = Attendance(employee_id, date, status)
        self.attendance_records.append(new_record)

    def get_attendance_records(self):
        return self.attendance_records