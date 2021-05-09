from cryptography.fernet import Fernet

class Authentication():
    __key = Fernet.generate_key()

    def __init__(self):
        self.__fernet = Fernet(Authentication.__key)


    def encrypt(self, password):
        return self.__fernet.encrypt(password.encode())

    def decrypt(self, encrypted_password):
        return self.__fernet.decrypt(encrypted_password).decode()

    def authenticate(self, auth_dict):
        print(auth_dict.get('username'), auth_dict.get('password'))
        # Fetch user password from DB

        # decrypt the password in DB
        # compare password in DB with password in request
        return True


if __name__ == "__main__":
    a  = Authentication()
    en = a.encrypt("Kanmani")
    print(type(en))
    print(en)
    de = a.decrypt(en)
    print(type(de))
    print(de)