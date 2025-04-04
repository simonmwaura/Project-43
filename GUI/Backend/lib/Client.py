from lib.config import conn

class Client: 
    # create client
    @classmethod
    def create_client(cls, name, email, phone_number, identity_number):
        cursor = conn.cursor()
        sql = """INSERT INTO Client(Name, Email, Phone_Number, National_Identity_Number) 
                 OUTPUT INSERTED.Id
                 VALUES(?,?,?,?)"""
        cursor.execute(sql, (name, email, phone_number, identity_number))   
        
        client_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return client_id
        
    # get client by name
    @classmethod
    def fetch_single_client(cls, name):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Client WHERE Name=?
            """
        cursor.execute(sql, (name,)),
        result = cursor.fetchone()
        cursor.close()
        return result
        
    # update client by name
    @classmethod
    def update_single_client(cls, old_name, new_name, email, phone_number, identity_number):
        cursor = conn.cursor()
        sql="""
                UPDATE Client SET Name=?, Email=?, Phone_Number=?, National_Identity_Number=? WHERE Name=?
            """
        cursor.execute(sql,(new_name, email, phone_number, identity_number, old_name))
        conn.commit()
        cursor.close()
        return new_name

    # delete client by name
    @classmethod
    def delete_single_client(cls, name):
        cursor = conn.cursor()
        sql="""
               DELETE FROM Client WHERE Name =?
            """
        cursor.execute(sql,(name,))
        conn.commit()
        cursor.close()
        return name
        
    # fetch all clients
    @classmethod
    def fetch_all_clients(cls):
        cursor = conn.cursor()
        sql="""
             SELECT * FROM CLIENT
            """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        return results
        