from lib.config import conn
class Client:
    
    # create client
    @classmethod
    def create_client(cls, Client_name, Client_email, Client_phone_number, Client_identity_number):
        cursor = conn.cursor()
        sql = """INSERT INTO Client(Client_name,Client_email,Client_phone_number,Client_identity_number) 
                 OUTPUT INSERTED.Client_id
                 VALUES(?,?,?,?)"""
        cursor.execute(sql, (Client_name, Client_email, Client_phone_number, Client_identity_number))   
        
        client_id = cursor.fetchone()[0]
        conn.commit()
        return client_id
        cursor.close()

    # get client by id
    @classmethod
    def fetch_single_client(cls, Client_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Client WHERE Client_id=?
            """
        cursor.execute(sql, (Client_id,)),
        return cursor.fetchone()
        cursor.close()

    # update client by id
    @classmethod
    def update_single_client(cls, Client_id, Client_name, Client_email, Client_phone_number, Client_identity_number):
        cursor = conn.cursor()
        sql="""
                UPDATE Client SET Client_name=?,Client_email=?,Client_phone_number=?,Client_identity_number=? WHERE Client_id=?
            """
        cursor.execute(sql,(Client_name, Client_email, Client_phone_number, Client_identity_number, Client_id))
        conn.commit()
        
        cursor.close()
        return Client_id


    # delete user by id
    @classmethod
    def delete_single_user(cls, Client_id):
        cursor = conn.cursor()
        sql="""
               DELETE FROM Client WHERE Client_id =?
            """
        cursor.execute(sql,( Client_id,))
        conn.commit()
        return Client_id
        cursor.close()


    # fetch all clients
    @classmethod
    def fetch_all_clients(cls):
        cursor = conn.cursor()
        sql="""
             SELECT * FROM CLIENT
            """
        cursor.execute(sql)
        return cursor.fetchall()
        cursor.close()