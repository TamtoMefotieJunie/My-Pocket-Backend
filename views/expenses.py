from flask import Blueprint, request, Response,jsonify

from controllers.expenses import *
from models.exceptions import ModelNotFoundError

expenses_view = Blueprint('expenses', __name__, url_prefix='/expenses')

@expenses_view.route('/', methods=['GET', 'POST'])
def list_or_create():
    if request.method == 'GET':
        return get_all_expenses()
    elif request.method == 'POST':
        # Parse the JSON data from the request body
        data = request.get_json()

        # Check if 'data' is a list of dictionaries
        if isinstance(data, dict) and all(key in data for key in ['name', 'amount', 'description', 'user_id', 'cat_id']):
            try:
                # Hypothetical function to save a category
                expense_response = save_expense(data['name'],data['amount'],data['description'],data['user_id'],data['cat_id'])
                return jsonify(expense_response), 201
            except Exception as e:
                return jsonify({'error': str(e)}), 400
        else:
            return jsonify({'error': 'Invalid request data'}), 400
    else:
        return Response({'error': 'Method not allowed'}, status=405)
    
@expenses_view.route('/<id>', methods=['GET', 'PATCH','DELETE'])
def get_or_update_instance(id):
    if request.method == 'GET':
        try:
            return get_expense_with_id(id,False)
        except ModelNotFoundError:
            return Response(f'expense not found',status=404)  # expense not found
    elif request.method == 'PATCH':
        data = request.get_json()
        return Response(save_expense(name=data['name'],amount=data['amount'],description=data['description'],
                                     user_id=data['user_id'],cat_id=data['cat_id'],id=id),status=201)
    elif request.method == 'DELETE':
        return Response(delete_expense(id),status=201)
    else:
        return None


