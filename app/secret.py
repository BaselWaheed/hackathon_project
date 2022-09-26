from cryptography.fernet import Fernet

key = b'8uyyS1R5xCv3hjJ2YpWN1YjXgqkcq-HaMFhtQOxPzdA='

class Data:
    @staticmethod
    def encrypt(data):
        root = Fernet(key) 
        encrypted_data = root.encrypt(data.encode())
        return encrypted_data
        

    @staticmethod
    def decrpyt(data):
        root = Fernet(key) 
        try :
            decrypted_data = root.decrypt(data).decode()
        except:
            decrypted_data = False
        return decrypted_data
