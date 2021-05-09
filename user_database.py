import sqlite3

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
ADMIN_USER_VALUES = ("admin", "password", "admin@auth.project", "0000000000")
UPDATE_QUERY = """UPDATE USERS SET USERNAME=?,PASSWORD=?,EMAIL=?,TELEPHONE=? WHERE USERNAME=?"""

class UserDB():
    def __init__(self):
        # Connects to the Database, User_DB.db
        self.conn = sqlite3.connect("User_DB.db", check_same_thread=False)
        # Creates User Table.
        self.create_table()
        # Creates default user, admin
        self.create_user(ADMIN_USER_VALUES)

    def create_table(self):
        cursor = self.conn.cursor()
        try:
            cursor.execute(CREATE_USER_TABLE)
        except Exception as e:
            print("User table creation failed. %s" % e)
        finally:
            self.conn.commit()

    def create_user(self, user_record):
        status = None
        cursor = self.conn.cursor()
        # Check whether user record already exists
        try:
            users = cursor.execute(QUERY_USER,(user_record[0], )).fetchall()
            if users:
                print("User already exists.")
                return status_code.USER_ALREADY_EXISTS
        except Exception as e:
            print("Unable to check whether user exists or not. %s" % e)
            return status_code.INTERNAL_SERVER_ERROR
        # Add user record to the Database
        USER_RECORD = INSERT_USER_RECORD.format(user_record)
        try:
           cursor.execute(str(USER_RECORD))
           status = status_code.OPERATION_SUCCESS
        except Exception as e:
            print("User creation failed. %s" %e)
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
        status = None
        cursor = self.conn.cursor()
        # Check whether user record already exists
        # Check whether user record already exists
        try:
            users = cursor.execute(QUERY_USER, (username, )).fetchall()
            if not users:
                print("User does not exists.")
                return status_code.USER_DOESNOT_EXISTS
        except Exception as e:
            print("Unable to check whether user exists or not. %s" % e)
            return status_code.INTERNAL_SERVER_ERROR
        try:
            cursor.execute(UPDATE_QUERY,(username, password, email, telephone, username))
            status = status_code.OPERATION_SUCCESS
        except Exception as e:
            print("Exception during user modification. %s" % e)
            status = status_code.INTERNAL_SERVER_ERROR
        finally:
            self.conn.commit()
            #self.conn.close()
            return status


