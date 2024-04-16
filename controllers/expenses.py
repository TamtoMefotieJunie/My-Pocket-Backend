
from models.exceptions import ModelNotFoundError
from models.expenses import Expense




def get_all_expenses():
    expenses = Expense.read()
    return [ expense.toJSON() for expense in expenses ]

#function to get expense with id
def get_expense_with_id(id,return_object=True):
    expense = Expense.read(id)
    # Check if the expense is not found
    if expense is None:
        # Optionally, rExpensene to indicate that the expense doesn't exist
        return None
    # Return the expense object or its JSON representation based on the return_object parameter
    return expense.toJSON() if not return_object else expense

#save expense into db
def save_expense(name,amount,description,user_id,cat_id, id=None):
    # If an ID is provided, attempt to update the existing expense
    if id is not None:
        existing_expense = get_expense_with_id(id, return_object=True)
        # If an existing expense is found, update the details
        if existing_expense is not None:
            existing_expense.name = name
            existing_expense.amount = amount
            existing_expense.description = description
            existing_expense.user = user_id
            existing_expense.cat_id = cat_id
            existing_expense.save()
            return f"expense with ID {id} updated successfully"
        else:
            # If no existing expense is found, return an error message
            raise ModelNotFoundError (f"No expense found with ID {id}.")
    # If no ID is provided, create a new expense
    else:
        new_expense = Expense(name=name)
        new_expense.save()
        return new_expense if isinstance(new_expense, dict) else new_expense.toJSON()
#delete expense
def delete_expense(id):
    expense = get_expense_with_id(id)
    # Check if expense exists before attempting to delete
    if expense is not None:
        # Call delete() method on the Expense model instance
        Expense.delete(id)
        return f"expense wit ID {id} deleted successfully"
    else:
        # Handle case where expense does not exist
        raise ModelNotFoundError(f"expense with ID {id} not found")