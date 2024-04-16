import os
from models.exceptions import ModelNotFoundError
from models.users import User

#function to get all users
def get_all_users():
    users = User.read()
    return [ user.toJSON() for user in users ]

#function to get user with id
def get_user_with_id(id,return_object=True):
    user = User.read(id)
    # Check if the user is not found
    if user is None:
        # Optionally, return None to indicate that the user doesn't exist
        return None
    # Return the user object or its JSON representation based on the return_object parameter
    return user.toJSON() if not return_object else user

#save user into db
def save_user(name, email, password, id=None):
    # If an ID is provided, attempt to update the existing user
    if id is not None:
        existing_user = get_user_with_id(id, return_object=True)
        # If an existing user is found, update the details
        if existing_user is not None:
            existing_user.name = name
            existing_user.email = email
            existing_user.password = password
            existing_user.save()
            return f"user with ID {id} updated successfully"
        else:
            # If no existing user is found, return an error message
            raise ModelNotFoundError (f"No user found with ID {id}.")
    # If no ID is provided, create a new user
    else:
        new_user = User(name=name, email=email, password=password)
        new_user.save()
        return new_user if isinstance(new_user, dict) else new_user.toJSON()



#delete user
def delete_user(id):
    user = get_user_with_id(id)
    # Check if user exists before attempting to delete
    if user is not None:
        # Call delete() method on the User model instance
        User.delete(id)
        return f"user wit ID {id} deleted successfully"
    else:
        # Handle case where user does not exist
        raise ModelNotFoundError(f"User with ID {id} not found.")