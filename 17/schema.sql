DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

INSERT INTO posts (title, content) VALUES ('範例貼文', '這是範例貼文的內容。');