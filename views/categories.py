from flask import Blueprint, jsonify, request, Response,json

from controllers.categories import *
from models.exceptions import ModelNotFoundError

categories_view = Blueprint('categories', __name__, url_prefix='/categories')

@categories_view.route('/', methods=['GET', 'POST'])
def list_or_create():
    if request.method == 'GET':
        return get_all_categories()
    elif request.method == 'POST':
        # Parse the JSON data from the request body
        data = request.get_json()

        # Check if 'data' is a list of dictionaries
        if isinstance(data, dict) and 'name'  in data:
            try:
                # Hypothetical function to save a category
                category_response = save_category(data['name'])
                return jsonify(category_response), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'Invalid request data'}), 400
    else:
        return Response({'error': 'Method not allowed'}, status=405)
    
@categories_view.route('/<id>', methods=['GET', 'PATCH','DELETE'])
def get_or_update_instance(id):
    if request.method == 'GET':
        try:
            return get_category_with_id(id,False)
        except ModelNotFoundError:
            return Response(f'category not found',status=404)  # Category not found
    elif request.method == 'PATCH':
        data = request.get_json()
        return Response(save_category(name=data['name'],id=id),status=201)
    elif request.method == 'DELETE':
        return Response(delete_category(id),status=201)
    else:
        return None


