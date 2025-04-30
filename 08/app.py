import os
from flask import Flask, session, url_for, redirect, request, render_template, jsonify, flash
from authlib.integrations.flask_client import OAuth
from models import db, Personnel  # 導入 models.py 中的 db 和 Personnel
from urllib.parse import urlencode # For logout URL

# --- Flask App Initialization ---
app = Flask(__name__)
# 重要：設定一個安全的 Secret Key 來保護 Session
# 在生產環境中，應該從環境變數讀取
app.config['SECRET_KEY'] = 'your_secret_key'  # 替換為安全的密鑰
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///personnel.db'  # SQLite 資料庫檔案
app.secret_key = os.urandom(24)

# --- Authlib OAuth Configuration ---
oauth = OAuth(app)

# 從環境變數或設定檔讀取 Keycloak 設定，更安全
# 為了範例方便，直接寫在這裡，但強烈建議不要硬編碼
KEYCLOAK_ISSUER = 'http://localhost:8080/auth/realms/my-personnel-realm' # 替換成你的 Realm URL
KEYCLOAK_CLIENT_ID = 'personnel-system-app' # 替換成你的 Client ID
KEYCLOAK_CLIENT_SECRET = 'yNiPHz2k5kapLXnEG30p54Q93Mkt4Z7A' # 替換成你在 Keycloak 拿到的 Client Secret (如果是 confidential client)
# 如果是 public client，不需要 secret

oauth.register(
    name='keycloak',
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret=KEYCLOAK_CLIENT_SECRET, # 如果是 public client，可以省略或設為 None
    server_metadata_url=f'{KEYCLOAK_ISSUER}/.well-known/openid-configuration', # Authlib 會自動從這裡取得端點資訊
    client_kwargs={
        'scope': 'openid email profile', # 請求的權限
        'code_challenge_method': 'S256' # Recommended for public clients and confidential clients for better security (PKCE)
    }
)

# --- 你的其他 Flask 設定和 SQLAlchemy 初始化 ---
# from flask_sqlalchemy import SQLAlchemy
# app.config['SQLALCHEMY_DATABASE_URI'] = '...'
# db = SQLAlchemy(app)
# ...


db.init_app(app)

# 創建資料庫表格
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    personnel_list = Personnel.query.all()
    return render_template('index.html', personnel_list=personnel_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        employee_number = request.form['employee_number']
        department = request.form['department']
        position = request.form['position']
        contact = request.form['contact']
        
        # 檢查員工編號是否唯一
        existing = Personnel.query.filter_by(employee_number=employee_number).first()
        if existing:
            flash('員工編號已存在，請使用其他編號。')
            return redirect(url_for('add'))
        
        new_personnel = Personnel(name=name, employee_number=employee_number, department=department, position=position, contact=contact)
        db.session.add(new_personnel)
        db.session.commit()
        flash('人員新增成功！')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    personnel = Personnel.query.get_or_404(id)
    if request.method == 'POST':
        personnel.name = request.form['name']
        personnel.employee_number = request.form['employee_number']
        personnel.department = request.form['department']
        personnel.position = request.form['position']
        personnel.contact = request.form['contact']
        
        # 檢查員工編號是否唯一（排除自己）
        existing = Personnel.query.filter_by(employee_number=personnel.employee_number).filter(Personnel.id != id).first()
        if existing:
            flash('員工編號已存在，請使用其他編號。')
            return redirect(url_for('edit', id=id))
        
        db.session.commit()
        flash('人員更新成功！')
        return redirect(url_for('index'))
    return render_template('edit.html', personnel=personnel)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    personnel = Personnel.query.get_or_404(id)
    db.session.delete(personnel)
    db.session.commit()
    flash('人員刪除成功！')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
