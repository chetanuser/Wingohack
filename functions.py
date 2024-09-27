import os
import json

def isExists(user_id):
    """Check if the user file exists."""
    file_path = os.path.join('Account', f'{user_id}.json')
    return os.path.isfile(file_path)

def insertUser(user_id, data):
    """Insert user data if user file does not exist."""
    if not isExists(user_id):
        if not os.path.exists('Account'):
            os.makedirs('Account')
        file_path = os.path.join('Account', f'{user_id}.json')
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    return False

def getData(user_id):
    """Retrieve all user data in JSON format."""
    if isExists(user_id):
        file_path = os.path.join("Account", f'{user_id}.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        # Return None or an empty dictionary if the user file does not exist
        return None

def addBalance(user_id, amount):
    """Add balance to the user account."""
    if isExists(user_id):
        file_path = os.path.join('Account', f'{user_id}.json')
        with open(file_path, 'r+') as file:
            data = json.load(file)
            data['balance'] = str(float(data['balance']) + amount)
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        return True
    return False

def cutBalance(user_id, amount):
    """Deduct balance from the user account."""
    if isExists(user_id):
        file_path = os.path.join('Account', f'{user_id}.json')
        with open(file_path, 'r+') as file:
            data = json.load(file)
            # Convert both the current balance and the amount to floats for arithmetic operation
            current_balance = float(data['balance'])
            amount = float(amount)  # Ensure amount is a float
            if current_balance >= amount:
                # After the calculation, convert the balance back to a string if necessary
                data['balance'] = str(current_balance - amount)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()
                return True
    return False


def track_exists(user_id):
    """Check if the referral user exists."""
    return isExists(user_id)

def setWelcomeStaus(user_id):
    """Set the referral information for the user."""
    if isExists(user_id):

        file_path = os.path.join("Account", f'{user_id}.json')
        with open(file_path, 'r+') as file:
            data = json.load(file)
            data['welcome_bonus'] = 1
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        return True
    return False

def setReferredStatus(user_id):
    """Set the referral information for the user."""
    if isExists(user_id):

        file_path = os.path.join("Account", f'{user_id}.json')
        with open(file_path, 'r+') as file:
            data = json.load(file)
            data['referred'] = 1
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        return True
    return False


def addRefCount(user_id):
    """Increment the referral count for the user."""
    if isExists(user_id):
        file_path = os.path.join("Account", f'{user_id}.json')
        with open(file_path, 'r+') as file:
            data = json.load(file)
            # Increment the total_refs count
            data['total_refs'] = data.get('total_refs', 0) + 1  # Default to 0 if not found
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()
        return True
    return False
