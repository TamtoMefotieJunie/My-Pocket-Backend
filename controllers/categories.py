
from models.exceptions import ModelNotFoundError
from models.categories import Category

#function to get all categories
def get_all_categories():
    categories = Category.read()
    return [ category.toJSON() for category in categories ]

#function to get category with id
def get_category_with_id(id,return_object=True):
    category = Category.read(id)
    # Check if the category is not found
    if category is None:
        # Optionally, return None to indicate that the category doesn't exist
        return None
    # Return the category object or its JSON representation based on the return_object parameter
    return category.toJSON() if not return_object else category

#save category into db
def save_category(name, id=None):
    # If an ID is provided, attempt to update the existing category
    if id is not None:
        existing_category = get_category_with_id(id, return_object=True)
        # If an existing category is found, update the details
        if existing_category is not None:
            existing_category.name = name
            existing_category.save()
            return f"category with ID {id} updated successfully"
        else:
            # If no existing category is found, return an error message
            raise ModelNotFoundError (f"No category found with ID {id}.")
    # If no ID is provided, create a new category
    else:
        new_category = Category(name=name)
        new_category.save()
        return new_category if isinstance(new_category, dict) else new_category.toJSON()
#delete category
def delete_category(id):
    category = get_category_with_id(id)
    # Check if category exists before attempting to delete
    if category is not None:
        # Call delete() method on the Category model instance
        Category.delete(id)
        return f"category wit ID {id} deleted successfully"
    else:
        # Handle case where category does not exist
        raise ModelNotFoundError(f"Category with ID {id} not found")