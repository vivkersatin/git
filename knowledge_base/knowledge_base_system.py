# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from werkzeug.utils import secure_filename
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from werkzeug.utils import secure_filename
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # 產生一個隨機的 secret key
# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from werkzeug.utils import secure_filename
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
# -*- coding: utf-8 -*-
import json
import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from werkzeug.utils import secure_filename
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

app = Flask(__name__, static_folder='static')
app.secret_key = os.urandom(24)  # 產生一個隨機的 secret key

# 資料庫檔案路徑
DATABASE_FILE = 'knowledge_base.json'

# 載入停用詞
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

# 建立預設的 JSON 資料庫檔案 (如果不存在)
if not os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'knowledge_entries': [], 'users': []}, f, indent=4, ensure_ascii=False)

def load_database():
    """載入 JSON 資料庫"""
    try:
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'knowledge_entries': [], 'users': []}
    except json.JSONDecodeError:
        return {'knowledge_entries': [], 'users': []}

def save_database(data):
    """儲存 JSON 資料庫"""
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def preprocess_text(text):
    """文字前處理：分詞、移除停用詞、詞形還原"""
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalnum() and w not in stop_words]
    words = [lemmatizer.lemmatize(w) for w in words]
    return words

# -------------------- 帳戶管理 --------------------
def authenticate_user(username, password):
    """驗證使用者"""
    data = load_database()
    for user in data['users']:
        if user['username'] == username and user['password'] == password:
            return user
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    """登入頁面"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user.get('is_admin', False)  # 檢查是否為管理員
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """註冊頁面"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        data = load_database()
        # 檢查使用者名稱是否已存在
        if any(user['username'] == username for user in data['users']):
            return render_template('register.html', error='Username already exists')
        # 建立新的使用者
        new_user = {
            'id': len(data['users']) + 1,
            'username': username,
            'password': password,
            'is_admin': username == 'admin'  # 如果使用者名稱是 'admin'，則設定為管理員
        }
        data['users'].append(new_user)
        save_database(data)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    """登出"""
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    return redirect(url_for('login'))

# -------------------- 知識庫管理 --------------------
def is_admin():
    """檢查使用者是否為管理員"""
    return session.get('is_admin', False)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    """新增知識庫條目"""
    if not is_admin():
        return redirect(url_for('index'))
    if request.method == 'POST':
        category = request.form['category']
        keywords = request.form['keywords']
        solution = request.form['solution']
        image_file = request.files['image_url']
        image_url = ''
        if image_file:
            # 儲存圖片到伺服器
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join('static/images', image_filename)
            image_file.save(image_path)
            image_url = url_for('static', filename=f'images/{image_filename}')
        data = load_database()
        new_entry = {
            'id': len(data['knowledge_entries']) + 1,
            'category': category,
            'keywords': keywords.split(','),
            'solution': solution,
            'image_url': image_url
        }
        data['knowledge_entries'].append(new_entry)
        save_database(data)
        return redirect(url_for('index'))
    return render_template('add_entry.html')

@app.route('/edit_entry/<int:entry_id>', methods=['GET', 'POST'])
def edit_entry(entry_id):
    """編輯知識庫條目"""
    if not is_admin():
        return redirect(url_for('index'))
    data = load_database()
    entry = next((e for e in data['knowledge_entries'] if e['id'] == entry_id), None)
    if not entry:
        return redirect(url_for('index'))
    if request.method == 'POST':
        entry['category'] = request.form['category']
        entry['keywords'] = request.form['keywords'].split(',')
        entry['solution'] = request.form['solution']
        entry['image_url'] = request.form['image_url']
        save_database(data)
        return redirect(url_for('index'))
    return render_template('edit_entry.html', entry=entry)

@app.route('/delete_entry/<int:entry_id>')
def delete_entry(entry_id):
    """刪除知識庫條目"""
    if not is_admin():
        return redirect(url_for('index'))
    data = load_database()
    data['knowledge_entries'] = [e for e in data['knowledge_entries'] if e['id'] != entry_id]
    save_database(data)
    return redirect(url_for('index'))

# -------------------- 查詢功能 --------------------
def search_knowledge_base(query):
    """查詢知識庫"""
    processed_query = preprocess_text(query)
    data = load_database()
    results = []
    for entry in data['knowledge_entries']:
        entry_keywords = [keyword.lower() for keyword in entry['keywords']]
        # 檢查查詢字詞是否與關鍵字匹配
        if any(word in entry_keywords for word in processed_query):
            results.append(entry)
    return results

# -------------------- 路由 --------------------
@app.route('/', methods=['GET', 'POST'])
def index():
    """首頁"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        query = request.form['query']
        results = search_knowledge_base(query)
        all_entries = load_database()['knowledge_entries']
        return render_template('index.html', results=results, is_admin=is_admin(), all_entries=all_entries)
    all_entries = load_database()['knowledge_entries']
    return render_template('index.html', results=[], is_admin=is_admin(), all_entries=all_entries)

# -------------------- 啟動伺服器 --------------------
if __name__ == '__main__':
    app.run(debug=True)
