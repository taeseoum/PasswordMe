from db.encrypted_db import EncryptedDB
from encryption.aes_encryption import AESEncryption
from encryption.master_key import MasterKey
import os

class MainWindow:
    def run(self):
        # This whole section is just to check if the user has already set a master password
        first_run = not os.path.exists(MasterKey.SALT_PATH)
        
        if first_run:
            master_password = input("Set your master password: ")
            confirm_password = input("Confirm your master password: ")
            if master_password != confirm_password:
                print("Passwords do not match!")
                return
        else:
            master_password = input("Enter your master password: ")

        try:
            master_key = MasterKey(master_password)
        except ValueError as e:
            print(e)  
            return

        aes_encryption = AESEncryption(master_key.key)
        db = EncryptedDB(aes_encryption)

        while True:
            choice = input("\n1.Store a new password\n2.Get password from database\n3.Exit\n\nEnter your choice: ")

            if choice == "1":
                website = input("Enter website: ")
                password = input("Enter password: ")
                iv, tag, encrypted_password = aes_encryption.encrypt(password)
                db.insert(website, iv, tag, encrypted_password)
                print("done! It should be in the database,,,,it really should idk")

            elif choice == "2":
                website = input("Enter website: ")
                data = db.get_data(website)
                if data:
                    decrypted_password = aes_encryption.decrypt(*data)
                    print(f"Your password is: {decrypted_password}")
                else:
                    print("No password found, bruh what you doing")

            elif choice == "3":
                print("use me next time when you need it!")
                break



