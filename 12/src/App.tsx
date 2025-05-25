import { useState } from 'react';
import './App.css';

function App() {
  const [announcements, setAnnouncements] = useState<string[]>([]);
  const [newAnnouncement, setNewAnnouncement] = useState('');
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editingText, setEditingText] = useState('');

  const addAnnouncement = () => {
    if (newAnnouncement.trim()) {
      setAnnouncements([...announcements, newAnnouncement]);
      setNewAnnouncement('');
    }
  };

  const deleteAnnouncement = (index: number) => {
    setAnnouncements(announcements.filter((_, i) => i !== index));
  };

  const startEditing = (index: number) => {
    setEditingIndex(index);
    setEditingText(announcements[index]);
  };

  const saveEditing = () => {
    if (editingIndex !== null) {
      const updatedAnnouncements = [...announcements];
      updatedAnnouncements[editingIndex] = editingText;
      setAnnouncements(updatedAnnouncements);
      setEditingIndex(null);
      setEditingText('');
    }
  };

  return (
    <div className="App">
      <h1>公告系統</h1>
      <div>
        <input
          type="text"
          value={newAnnouncement}
          onChange={(e) => setNewAnnouncement(e.target.value)}
          placeholder="輸入新公告"
          title="新增公告輸入框"
        />
        <button onClick={addAnnouncement}>新增公告</button>
      </div>
      <ul>
        {announcements.map((announcement, index) => (
          <li key={index}>
            {editingIndex === index ? (
              <div>
                <input
                  type="text"
                  value={editingText}
                  onChange={(e) => setEditingText(e.target.value)}
                  placeholder="編輯公告內容"
                  title="編輯公告輸入框"
                />
                <button onClick={saveEditing}>儲存</button>
              </div>
            ) : (
              <span>{announcement}</span>
            )}
            <button onClick={() => startEditing(index)}>編輯</button>
            <button onClick={() => deleteAnnouncement(index)}>刪除</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
