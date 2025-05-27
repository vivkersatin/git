from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# 設置 SQLite 資料庫
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///announcements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定義公告模型
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

# 創建資料庫
with app.app_context():
    db.create_all()

@app.route('/announcements', methods=['GET'])
def get_announcements():
    announcements = Announcement.query.all()
    return jsonify([{'id': a.id, 'text': a.text} for a in announcements])

@app.route('/announcements', methods=['POST'])
def create_announcement():
    new_announcement = request.json
    announcement = Announcement(text=new_announcement['text'])
    db.session.add(announcement)
    db.session.commit()
    return jsonify({'id': announcement.id, 'text': announcement.text}), 201

@app.route('/announcements/<int:announcement_id>', methods=['PUT'])
def update_announcement(announcement_id):
    updated_announcement = request.json
    announcement = Announcement.query.get(announcement_id)
    if announcement:
        announcement.text = updated_announcement['text']
        db.session.commit()
        return jsonify({'id': announcement.id, 'text': announcement.text}), 200
    return jsonify({"error": "Announcement not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)