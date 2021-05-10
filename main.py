# AUTH PROJECT APP
from flask import Flask, request, make_response

from cipher import Authentication
import status_code
import user_database as user_db

# Create Flask app
app = Flask(__name__)

# API endpoint to home.
@app.route('/')
@app.route('/home')
def home():
        return "<h1>WELCOME TO USERS PROJECT<h1>"

# API endpoint to list users.
@app.route('/users/list')
def users():
    # Fetch the users from the Database and send it in response
    user_list = db.list_users()
    return user_list, 200

# API endpoint to create a user record.
@app.route('/users', methods = ['POST'])
def implement_create_users():
    # Check whether given username is already in the DB
    # If exists, send Error as User Exists in DB
    # Else create user and return success.
    username = password = email = telephone = None
    if request.method == 'POST':
        data = request.json
        if len(data.keys()) < status_code.USER_RECORD_LENGTH:
            return "Need all the user record fields to create user", 403

        if data.get("username"):
            username = data['username']

        if data.get("password"):
            password = str(cipher_handle.encrypt(data['password']))

        if data.get("email"):
            email = data['email']

        if data.get('telephone'):
            telephone = data['telephone']

        user_record = (username,
                       password,
                       email,
                       telephone)

    result, msg = db.create_user(user_record)
    if result == status_code.OPERATION_SUCCESS:
        return msg, 200
    else:
        return msg, 422


# API endpoint to modify a user record.
@app.route('/users', methods = ['PUT'])
def implement_modify_users():
    # Check whether user exists in the DB
    # If exists, proceed with Update and send response
    # else send Error as No user with such username
    username = password = email = telephone = None
    if request.method == 'PUT':
        data = request.json
        if not len(data.keys()):
            return "Please provide values to update User Record", 403

        if data.get("username", ""):
            username = data['username']

        if data.get("password", ""):
            password = cipher_handle.encrypt(data['password'])

        if data.get("email", ""):
            email = data['email']

        if data.get('telephone', ""):
            telephone = data['telephone']

        if not len(username):
            return "Username is mandatory to update the User Record", 403

    result, msg= db.modify_user(username, password, email, telephone)
    if result == status_code.OPERATION_SUCCESS:
        return msg, 200
    else:
        return msg, result

# API endpoint to delete a user record.
@app.route('/users', methods = ['DELETE'])
def implement_delete_users():
    # Check whether user exists in DB,
    # If exists, delete and send response
    # else send error as User doesn't exists.
    if request.method == 'DELETE':
        data = request.json
        if not len(data.keys()):
            return "Please provide username to delete user record", 403

        if data.get("username"):
            username = data['username']

        if not username:
            return "Username is mandatory to update the User Record", 403

    result = db.delete_user(username)

    if result == status_code.OPERATION_SUCCESS:
        return "User deleted.", 200
    else:
        return "User delete failed", 422


if __name__ == '__main__':
    # Initialize DB to store user record
    db = user_db.UserDB()
    # Creating Singleton instance for encryption key
    cipher_handle = Authentication.get_instance()

    app.run(host='0.0.0.0')
