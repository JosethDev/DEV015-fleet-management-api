from flask import Flask
from db import db
from taxis_service import get_taxis
from trajectories_service import get_trajectories_by_taxi_id, get_latest_location_of_all_taxis

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://default:PCsm1f5kRbWz@ep-weathered-boat-a4axny3b-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'
port = 5001

# Inicializa la base de datos
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello world DB!'

@app.route('/taxis', methods=['GET'])
def taxis():
    return get_taxis()

@app.route('/trajectories', methods=['GET'])
def trajectories():
    return get_trajectories_by_taxi_id()

@app.route('/trajectories/latest', methods=['GET'])
def latest_locations():
    return get_latest_location_of_all_taxis()
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = port)