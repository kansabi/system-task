from cryptography.fernet import Fernet

class Authentication():
    __key = Fernet.generate_key()
    __instance = None

    def __init__(self):
        self.__fernet = Fernet(Authentication.__key)
        if Authentication.__instance != None:
            raise Exception("Cipher key class should be a Singleton")
        else:
            Authentication.__instance = self

    @staticmethod
    def get_instance():
        if Authentication.__instance == None:
            Authentication()
        return Authentication.__instance

    def encrypt(self, password):
        return self.__fernet.encrypt(password.encode())

    def decrypt(self, encrypted_password):
        password_to_byte = encrypted_password.encode('utf-8')
        print(encrypted_password)
        print(password_to_byte)
        value = ""
        try:
            value = self.__fernet.decrypt(password_to_byte).decode()
        except Exception as e:
            print("Ecpetion. %s" % e)
        finally:
            return value

    def authenticate(self, auth_dict):
        print(auth_dict.get('username'), auth_dict.get('password'))
        # Fetch user password from DB
        # decrypt the password in DB
        # compare password in DB with password in request
        return True


if __name__ == "__main__":
    a  = Authentication()
    en = a.encrypt("Kanmani")
    de = a.decrypt(en)
    print(en)
    print(de)