from flask import Flask, url_for, request, jsonify
from worker import celery
import celery.states as states
from flask_cors import CORS

app = Flask(__name__)
CORS(app, expose_headers='Authorization')

RESPONSE = "<a href='{url}'>check status of {tid} </a>"

@app.route('/')
def home():
    return 'deff updating'

@app.route('/bbb/:param')
def bbb(p):
    return 'bbb '+p

@app.route('/airbnb')
def predict():
    username = request.args.get('username')
    apikey = request.args.get('api_key')
    input_table = request.args.get('input_table')
    output_table  = request.args.get('output_table')

    print('------------------------')
    print('username ', username )
    print('apikey ',apikey )
    print('input table ', input_table)
    print('output table ', output_table)
    print('------------------------')

    task = celery.send_task('tasks.predict', args=[username,apikey, input_table,output_table], kwargs={})
    response = RESPONSE.format(
            tid=task.id,
            url=url_for('check_task', task_id=task.id, external=True)
        )
    return response

@app.route('/check/<string:task_id>')
def check_task(task_id):
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return jsonify({'state': res.state})
    else:
        return jsonify({'state': res.state, 'table_name': res.result})
