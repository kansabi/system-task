# AUTH PROJECT APP
from flask import Flask, request, make_response

import status_code
import user_database as user_db

# Create Flask app
app = Flask(__name__)

# API endpoint to home.
@app.route('/')
@app.route('/home')
def home():
        return "<h1>WELCOME TO AUTH PROJECT<h1>"

# API endpoint to list users.
@app.route('/users/list')
def users():
    # Fetch the users from the Database and send it in response
    user_list = db.list_users()
    #print(user_list)
    return user_list

# API endpoint to create a user record.
@app.route('/users', methods = ['POST'])
def implement_create_users():
    # Check whether given username is already in the DB
    # If exists, send Error as User Exists in DB
    # Else create user and return success.
    if request.method == 'POST':
        data = request.json
        user_record = (data.get('username'),
                      data.get('password'),
                       data.get('email'),
                       data.get('telephone'))
    result = db.create_user(user_record)
    if result == status_code.OPERATION_SUCCESS:
        return "User Created"
    else:
        return "User Creation failed"


# API endpoint to modify a user record.
@app.route('/users', methods = ['PUT'])
def implement_modify_users():
    # Check whether user exists in the DB
    # If exists, proceed with Update and send response
    # else send Error as No user with such username
    if request.method == 'PUT':
        data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    telephone = data.get('telephone')
    result = db.modify_user(username, password, email, telephone)
    if result == status_code.OPERATION_SUCCESS:
        return "User Modified"
    else:
        return "User Modification failed"

# API endpoint to delete a user record.
@app.route('/users', methods = ['DELETE'])
def implement_delete_users():
    # Check whether user exists in DB,
    # If exists, delete and send response
    # else send error as User doesnot exists.
    pass


if __name__ == '__main__':
    #user = User()
    db = user_db.UserDB()
    app.run(debug=True)




#