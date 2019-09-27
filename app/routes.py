from app import app
from flask import jsonify, abort, request
from app import db
from app.models import Task


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/tasks', methods=['GET'])
def get_tasks():
    all_tasks = Task.query.all()
    resp = list(map(lambda task: task.serialize(), all_tasks))
    return jsonify({'tasks': resp})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404)
    return jsonify(task.serialize())


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)

    task = Task(title=request.json['title'],
                description=request.json.get('description', ""),
                done=request.json.get('done', False))

    db.session.add(task)
    db.session.commit()
    return jsonify(task.serialize()), 201


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404)

    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task.title = request.json.get('title', task.title)
    task.description = request.json.get('description', task.description)
    task.done = request.json.get('done', task.done)
    db.session.commit()
    return jsonify(task.serialize())


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        abort(404)
    db.session.delete(task)
    return jsonify({'result': True})