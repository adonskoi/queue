import time
import random
import threading
import queue
from flask import Flask, jsonify
from tinydb import TinyDB
import logging


# config
logging.basicConfig(level=logging.DEBUG)
db = TinyDB('db.json')
q = queue.Queue()
app = Flask(__name__)


# create, start, finish, update task
def create_task() -> int:
    create_time = time.time()
    task_id = db.insert({'create_time': create_time, 'status': 'In Queue', 'start_time': '', 'time_to_execute': ''})
    q.put(task_id)
    logging.info(f'job created: {task_id}')
    return task_id


def start_task(task_id: int):
    start_time = time.time()
    db.update({'start_time': start_time, 'status': 'Run'}, doc_ids=[task_id])


def finish_task(task_id: int):
    time_to_execute = time.time()
    db.update({'time_to_execute': time_to_execute, 'status': 'Completed'}, doc_ids=[task_id])
    logging.info(f'job finish: {task_id}')


def get_task(task_id: int) -> dict:
    result = db.get(doc_id=int(task_id))
    return result


# job to execute
def job():
    time.sleep(random.randint(1, 10))


# worker
def worker(worker_id: int):
    while True:
        task_id = q.get()
        start_task(task_id)
        logging.info(f'job start: {task_id}, with worker: {worker_id}')
        job()
        finish_task(task_id)
        q.task_done()


# create workers
threading.Thread(target=worker, args=(1,), daemon=True).start()
threading.Thread(target=worker, args=(2,), daemon=True).start()


# routes
@app.route('/', methods=['POST'])
def job_post():
    task_id = create_task()
    return jsonify({'id': task_id})


@app.route('/<int:task_id>')
def task_post(task_id: int):
    result = get_task(task_id)
    return jsonify(result)


if __name__ == '__main__':
    app.run(port=5000)
