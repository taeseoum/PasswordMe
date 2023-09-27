import sqlite3 


class EncryptedDB:
    def __init__(self, aes_encryption, db_path="passwords.db"):
        self.aes_encryption = aes_encryption
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            ### SQLite database syntax +

            ### AES Encryption syntax

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    platform TEXT NOT NULL,
                    iv BLOB NOT NULL,
                    tag BLOB NOT NULL,
                    encrypted_password BLOB NOT NULL
                );
            """)

    def create_table(self):
        #the attributes are going to be the columns obviously, 
        #attributes are: website, bla, bla, bla

        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                              website TEXT PRIMARY KEY,
                                iv BLOB NOT NULL,
                                tag BLOB NOT NULL,
                                encrypted_password BLOB NOT NULL
                                )
                              """)
            
    def insert(self, website, iv, tag, encrypted_password):
        with self.conn:
            self.conn.execute("INSERT INTO passwords (website, iv, tag, encrypted_password) VALUES (?, ?, ?, ?)", (website, iv, tag, encrypted_password))


    ### the website is what the person is searching for
    def get_data(self, website):
        cursor =self.conn.cursor()
        cursor.execute("SELECT iv, tag, encrypted_password FROM passwords WHERE website=?", (website,))
        return cursor.fetchone()