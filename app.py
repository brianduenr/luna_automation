import os
import csv
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask_socketio import SocketIO
from celery.result import AsyncResult
from tasks import run_automation_task

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret!')
socketio = SocketIO(app)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
OUTPUT_CSV = os.path.join('data', 'result.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_test():
    if 'csv_file' not in request.files:
        return 'No file part'
    file = request.files['csv_file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        chatbot_url = request.form['chatbot_url']
        wake_word = request.form['wake_word']

        task = run_automation_task.delay(filepath, OUTPUT_CSV, chatbot_url, wake_word)

        return render_template('running.html', task_id=task.id)

@app.route('/results')
def show_results():
    if not os.path.exists(OUTPUT_CSV):
        return "No results found. Please run a test first."

    with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)
        results = list(reader)

    return render_template('results.html', headers=headers, results=results)

@socketio.on('get_logs')
def handle_get_logs(data):
    task_id = data['task_id']
    task = AsyncResult(task_id)
    if task.state == 'PROGRESS':
        socketio.emit('log_message', {'message': task.info.get('log')})
    elif task.state == 'SUCCESS':
        socketio.emit('task_complete', {'message': 'Task complete!'})
    elif task.state == 'FAILURE':
        socketio.emit('task_failed', {'message': 'Task failed!'})

@socketio.on('connect')
def handle_connect():
    print('Client connected')
