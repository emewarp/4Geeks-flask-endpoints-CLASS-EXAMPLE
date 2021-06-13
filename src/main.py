"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Alarm

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# NO INFO FROM MODEL
@app.route('/demo', methods=['GET'])
def get_alarm():
    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/demo', methods=['POST'])
def create_demo():
    
    alarm = {
        "type": "demo"
    }

    return jsonify(alarm), 200

# INFO FROM MODEL
@app.route('/alarms', methods=['GET'])
def get_alarms():
    alarms = Alarm.get_alarms()
    serialized_alarms = []
    for alarm in alarms :
        serialized_alarms.append(alarm.serialize())
    return jsonify(serialized_alarms), 200

@app.route('/alarms/<int:id>', methods=['GET'])
def get_alarm_by_id(id):
    alarm = Alarm.get_alarm_by_id(id)
    return jsonify(alarm.serialize())


@app.route('/alarms', methods=['POST'])
def create_alarm():
    id = request.json.get('id')
    type = request.json.get('type')
    priority = request.json.get('priority')
    ack = request.json.get('ack')

    alarm = Alarm(
        id = id,
        type = type,
        priority = priority,
        ack = ack
    )
    alarm.create()
    return jsonify(alarm.serialize())

@app.route('/alarms/<int:id>', methods=['DELETE'])
def delete_alarm(id):
    Alarm.delete_alarm(id)
    response_body = {
        "msg": "alarm deleted"
    }

    return jsonify(response_body), 200
    

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
