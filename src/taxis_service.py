from flask import request, jsonify
from models import Taxi
from db import db

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

