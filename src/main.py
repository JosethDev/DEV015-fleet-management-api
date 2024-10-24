from flask import Flask, request, jsonify
from models import db, Taxi, Trajectory
import datetime
from sqlalchemy import func


app = Flask(__name__)
port = 5001
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://default:PCsm1f5kRbWz@ep-weathered-boat-a4axny3b-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require'

# Inicializa la base de datos
db.init_app(app)

@app.route('/')
def hello_world():
    return 'Hello world DB!'

@app.route('/taxis', methods=['GET'])
def get_taxis():
    try:
        # Obtener los parámetros de la consulta
        plate = request.args.get('plate', default=None, type=str) 
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
            taxis_data.append(taxi_data)

        return taxis_data
    
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/trajectories', methods=['GET'])
def get_trajectories_by_taxi_id():
    
    try:
         # Obtener los parámetros de la URL
        date = request.args.get('date')
        taxi_id = request.args.get('taxiId')
        
        # Verificar si 'date' o 'taxiId' no están presentes
        if not date or not taxi_id:
            return jsonify({'message': 'Sin parametro encontrada'}), 400 

        # Convertir el parámetro 'date' a formato de fecha (si es necesario)
        try:
           date = datetime.datetime.strptime(date, '%d-%m-%Y')
        except ValueError:
           return jsonify({'message': 'Formato de fecha no válido. Use DD-MM-YYYY'}), 400

        # Consultar todas las trayectorias que tienen el mismo taxi_id y coinciden con la fecha
        trajectories = Trajectory.query.filter_by(taxi_id=taxi_id).filter(db.func.date(Trajectory.date) == date.date()).all()

        if not trajectories:
            return jsonify({'message': 'No se encontraron trayectorias para este taxiId en la fecha especificada'}), 404

        # Crear una lista para almacenar las trayectorias
        trajectories_data = []
        
        # Recorrer las trayectorias del taxi
        for trajectory in trajectories:
            trajectory_data = {
                'id': trajectory.id,
                'taxiId': trajectory.taxi_id,
                'latitude': trajectory.latitude,
                'longitude': trajectory.longitude,
                'date': trajectory.date
            }
            trajectories_data.append(trajectory_data)
        
        # Devolver las trayectorias en formato JSON
        return jsonify(trajectories_data)
    
    except Exception as error:
        print('Error:', error)
        return jsonify({'message': 'Internal server error'}), 500
    

@app.route('/trajectories/latest', methods=['GET'])
def get_latest_location_of_all_taxis():
    try:
        # Subconsulta para obtener la última fecha reportada por cada taxi
        subquery = db.session.query(
            Trajectory.taxi_id,
            func.max(Trajectory.date).label('last_reported_date')
        ).group_by(Trajectory.taxi_id).subquery()

        # Consulta principal para obtener la última ubicación y datos del taxi
        last_locations = db.session.query(
            Trajectory.taxi_id,
            Trajectory.latitude,
            Trajectory.longitude,
            Taxi.plate,
            Trajectory.date.label('last_reported_date')  # Fecha reportada
        ).join(
            Taxi,  # Unir con la tabla Taxis
            Trajectory.taxi_id == Taxi.id
        ).join(
            subquery,
            (Trajectory.taxi_id == subquery.c.taxi_id) &
            (Trajectory.date == subquery.c.last_reported_date)  # Filtrar por la última fecha
        ).all()  # Obtener todos los resultados

        # 1. Si no hay ubicaciones, devolver un mensaje
        if not last_locations:
            return jsonify({'message': 'No se encontraron trayectorias'}), 404

        # 2. Lista para guardar las últimas ubicaciones y datos de los taxis
        last_locations_data = []

        # 3. Recorrer los resultados y agregar a la lista de ubicaciones
        for loc in last_locations:
            last_locations_data.append({
                'taxiId': loc.taxi_id,
                'latitude': loc.latitude,
                'longitude': loc.longitude,
                'plate': loc.plate,
                'timestamp': loc.last_reported_date.strftime('%Y-%m-%d %H:%M:%S')  # Formato de fecha requerido
            })    

        # 4. Devolver las ubicaciones y datos de los taxis en formato JSON
        return jsonify(last_locations_data)

    except Exception as error:
        print('Error:', error)  # Imprimir el error en la consola
        return jsonify({'message': 'Internal server error'}), 500  # Mensaje de error


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port = port)