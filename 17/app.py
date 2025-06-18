import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g

app = Flask(__name__)
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # This allows us to access columns by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def index():
    db = get_db()
    cursor = db.execute('SELECT id, title FROM posts ORDER BY id DESC')
    posts = cursor.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/post/<int:post_id>')
def post(post_id):
    db = get_db()
    cursor = db.execute('SELECT id, title, content FROM posts WHERE id = ?', (post_id,))
    post = cursor.fetchone()
    if post is None:
        return "貼文不存在", 404
    return render_template('post.html', post=post)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        db = get_db()
        db.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        db.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    db = get_db()
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db() # 初始化資料庫
    app.run(debug=True, port=8000)