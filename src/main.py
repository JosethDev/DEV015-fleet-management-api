from flask import Flask, request, jsonify
from models import db, Taxi, Trajectory

app = Flask(__name__)
port = 5001
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://default:PCsm1f5kRbWz@ep-weathered-boat-a4axny3b-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'

# Inicializa la base de datos
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello world DB!'


from flask import Flask, request, jsonify
from models import db, Taxi, Trajectory

@app.route('/taxis', methods=['GET'])
def get_taxis():
    try:
        # Obtener los parámetros de la consulta
        plate = request.args.get('plate', default=None, type=str)  # plate es opcional
        page = request.args.get('page', default=1, type=int)  # Página por defecto es 1
        limit = request.args.get('limit', default=10, type=int)  # Límite por defecto es 10

        # Filtrar por plate si se proporciona
        query = Taxi.query
        if plate:
            query = query.filter(Taxi.plate.ilike(f'%{plate}%'))

        # Paginación y límite
        taxis = query.paginate(page=page, per_page=limit).items

        taxis_data = []
        for taxi in taxis:
            taxi_data = {
                'id': taxi.id,
                'plate': taxi.plate,
            }
            '''  
            # Trajectorias por taxi
            for trajectory in taxi.trajectories:
                trajectory_data = {
                    'id': trajectory.id,
                    'taxi_id': trajectory.taxi_id,
                    'latitude': trajectory.latitude,
                    'longitude': trajectory.longitude,
                    'date': trajectory.date
                }
                taxi_data['trajectories'].append(trajectory_data)
            '''
            taxis_data.append(taxi_data)

        return taxis_data
    
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = port)