import sqlite3

import cipher as cipher
import status_code
import status_code as STATUS

# Global variables to store SQL commands
CREATE_USER_TABLE = """CREATE TABLE IF NOT EXISTS USERS (
                            USERNAME TEXT,
                            PASSWORD TEXT,
                            EMAIL TEXT,
                            TELEPHONE TEXT);"""

INSERT_USER_RECORD = """INSERT INTO USERS VALUES {}"""
QUERY_USER = """SELECT * FROM USERS WHERE USERNAME=?"""
QUERY_ALL_USER = """SELECT USERNAME,EMAIL,TELEPHONE FROM USERS"""
ADMIN_USER_VALUES = { "username": "admin",
                      "password": "admin",
                      "email": "admin@auth.project",
                      "telephone": "0000000000" }
UPDATE_QUERY = """UPDATE USERS SET USERNAME=?,PASSWORD=?,EMAIL=?,TELEPHONE=? WHERE USERNAME=?"""
DELETE_QUERY = """DELETE FROM USERS WHERE USERNAME=?"""
AUTH_USER_PASS = """SELECT USERNAME,PASSWORD FROM USERS WHERE USERNAME=?"""


class UserDB():
    def __init__(self):
        # Connects to the Database, User_DB.db
        self.conn = sqlite3.connect("User_DB.db", check_same_thread=False)

        # Initialize cipher for encryption
        self.key = cipher.Authentication()
        self.cipher_handle = self.key.get_instance()
        print(self.cipher_handle)

        # Creates User Table.
        self.create_table()

        # Creates default user, admin
        self.create_admin_user()

    def create_table(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(CREATE_USER_TABLE)
        except Exception as e:
            print("User table creation failed. %s" % e)
        finally:
            self.conn.commit()

    def create_admin_user(self):
        admin_password = self.cipher_handle.encrypt((ADMIN_USER_VALUES.get('password')))
        ADMIN_USER_VALUES['password'] = str(admin_password)
        admin_user_record = (ADMIN_USER_VALUES.get('username'),
                             ADMIN_USER_VALUES.get('password'),
                             ADMIN_USER_VALUES.get('email'),
                             ADMIN_USER_VALUES.get('telephone'))
        self.create_user(admin_user_record)

    def create_user(self, user_record):
        status = None
        cursor = self.conn.cursor()
        # Check whether user record already exists
        if self.check_user_exists(user_record[0]):
            return status_code.USER_ALREADY_EXISTS, "User already exists"

        # Add user record to the Database
        USER_RECORD = INSERT_USER_RECORD.format(user_record)
        try:
           cursor.execute(str(USER_RECORD))
           status = status_code.OPERATION_SUCCESS, "User Created successfully"
        except Exception as e:
            print("User creation failed. %s" %e), "Exceotion during User creation"
            status = status_code.INTERNAL_SERVER_ERROR
        finally:
            self.conn.commit()
            #self.conn.close()
            return status

    def list_users(self):
        status = None
        try:
            cursor = self.conn.cursor()
            result = cursor.execute(QUERY_ALL_USER).fetchall()
            user_list = {}
            for i in range(0,len(result)):
                user_list[i] = result[i]
            return user_list
        except Exception as e:
            print("Error fetching all users. %s" % e)


    def modify_user(self, username, password, email, telephone):
        status = msg = None
        cursor = self.conn.cursor()
        # Check whether user record already exists
        if username == 'admin':
            return status_code.INTERNAL_SERVER_ERROR, "admin user cannot be modified."

        if not self.check_user_exists(username):
            return status_code.USER_DOESNOT_EXISTS, "User doesnot exists."
        try:
            cursor.execute(UPDATE_QUERY,(username, password, email, telephone, username))
            status, msg = status_code.OPERATION_SUCCESS, "User Record Updated successfully."
        except Exception as e:
            print("Exception during user modification. %s" % e)
            status, msg = status_code.INTERNAL_SERVER_ERROR, "Exception during User Update."
        finally:
            self.conn.commit()
            return status, msg


    def delete_user(self, username):
        cursor = self.conn.cursor()
        # Check whether user exists
        if not self.check_user_exists(username):
            return status_code.USER_DOESNOT_EXISTS
        print(type(username))
        try:
            cursor.execute(DELETE_QUERY, (username,))
            user = cursor.execute(QUERY_USER,(username,)).fetchall()
            if user:
                print("User record still exists. %s" % user)
            return status_code.OPERATION_SUCCESS
        except Exception as e:
            print("User delete failed with exception. %s" % e)
            return status_code.INTERNAL_SERVER_ERROR
        finally:
            self.conn.commit()

    def check_user_exists(self, username):
        cursor = self.conn.cursor()
        try:
            user = cursor.execute(QUERY_USER,(username,)).fetchall()

            if user:
                return True
            else:
                return False
        except Exception as e:
            print("Exception during DB query. %s" % e)
            raise Exception


