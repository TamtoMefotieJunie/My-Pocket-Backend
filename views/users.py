from flask import Blueprint, jsonify, request, Response,json

from controllers.users import *
from models.exceptions import ModelNotFoundError

users_view = Blueprint('users', __name__, url_prefix='/users')

@users_view.route('/', methods=['GET', 'POST'])
def list_or_create():
    if request.method == 'GET':
        return get_all_users()
    elif request.method == 'POST':
        # Parse the JSON data from the request body
        data = request.get_json()

        # Check if 'data' is a list of dictionaries
        if isinstance(data, list) and all(isinstance(item, dict) and 'name' in item and 'email' in item and 'password' in item for item in data):
            # Iterate over each user and save 
            responses = []
            for user_data in data:
                try:
                    # Call save_user function with the user data
                    user_response = save_user(user_data['name'], user_data['email'], user_data['password'])
                    responses.append(user_response)
                except Exception as e:
                    responses.append({'error': str(e)})
            return jsonify(responses),400
        else:
            # Return an error response if 'data' is not as expected
            return jsonify({'error': 'Invalid request data'}), 400
    else:
        # Handle other HTTP methods
        return Response({'error': 'Method not allowed'}, status=405)
    
    
@users_view.route('/<id>', methods=['GET', 'PUT','DELETE'])
def get_or_update_instance(id):
    if request.method == 'GET':
        try:
            return get_user_with_id(id,False)
        except ModelNotFoundError:
            return Response(f'user not found',status=404)  # User not found
    elif request.method == 'PUT':
        data = request.get_json()
        return Response(save_user(name=data['name'],email=data['email'],password=data['password'],id=id))
    elif request.method == 'DELETE':
        return Response(delete_user(id),status=201)
    else:
        return None




