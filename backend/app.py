from flask import Flask, jsonify, request
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'todo_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        cursor_factory=RealDictCursor
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            text TEXT NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/api/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM todos ORDER BY id ASC;')
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todos():
    todo_data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO todos (text) VALUES (%s) RETURNING *;', (todo_data['text'],))
    new_todo = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_todo), 201

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM todos WHERE id = %s;', (todo_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"result": True})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)