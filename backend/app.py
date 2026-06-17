from flask import Flask, jsonify, request
import os

app = Flask(__name__)

todos = [] # will be connected to PostgreSQL later

@app.route('api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('api/todos', methods=['POST'])
def add_todos():
    todo_data = request.json
    current_todo = {"id": len(todos) + 1, "text": todo_data['text']}
    todos.append(current_todo)
    return jsonify(current_todo), 201
    
@app.route('api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t['id'] != todo_id]
    return jsonify({"result": True})

if __name__ == '__main__':
    app.run(host=0.0.0.0, port=5000)

