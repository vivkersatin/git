from flask import Flask, render_template, request, redirect, url_for
from employee import EmployeeManager
from attendance import AttendanceManager

app = Flask(__name__)
employee_manager = EmployeeManager()
attendance_manager = AttendanceManager()

@app.route('/')
def index():
    employees = employee_manager.get_employees()
    attendance_records = attendance_manager.get_attendance_records()  # 獲取考勤記錄
    return render_template('index.html', employees=employees, attendance_records=attendance_records)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    employee_manager.add_employee(name)
    return redirect(url_for('index'))

@app.route('/remove_employee/<int:id>')
def remove_employee(id):
    employee_manager.remove_employee(id)
    return redirect(url_for('index'))

@app.route('/record_attendance', methods=['POST'])
def record_attendance():
    employee_id = request.form['employee_id']
    date = request.form['date']
    status = request.form['status']
    attendance_manager.record_attendance(employee_id, date, status)
    return redirect(url_for('index'))

@app.route('/attendance/<date>')
def attendance(date):
    records = attendance_manager.get_attendance_records()
    attendance_details = [record for record in records if record.date == date]
    return render_template('attendance.html', date=date, attendance_details=attendance_details)

if __name__ == '__main__':
    app.run(debug=True)