from lib.config import conn
class Financials:
    # create Financials
    @classmethod
    def create_transaction(cls,Transaction_type,Transaction_amount,Transaction_date,Personnel_id,Project_id,Client_id, Supplier_id):
        cursor=conn.cursor()
        sql="""
             INSERT INTO Financials(Transaction_type,Transaction_amount,Transaction_date,Personnel_id,Project_id,Client_id, Supplier_id)
             OUTPUT INSERTED.Transaction_id
             VALUES(?,?,?,?,?,?,?)
            """
        cursor.execute(sql,( Transaction_type,Transaction_amount,Transaction_date,Personnel_id,Project_id,Client_id, Supplier_id))
        transaction_id = cursor.fetchone()[0]
        conn.commit()
        return transaction_id
        cursor.close()
        


    # fetch transaction by transaction id
    @classmethod
    def fetch_single_transaction(cls,Transaction_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Financials WHERE Transaction_id = ?  
            """
        cursor.execute(sql ,(Transaction_id, ))
        return cursor.fetchone()
        cursor.close()
         

     # fetch transaction by personnel id
    @classmethod
    def fetch_transaction_by_personnel_id(cls,Personnel_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Financials WHERE Personnel_id=?
            """
        cursor.execute(sql, (Personnel_id, ))
        return cursor.fetchone()
        cursor.close()


      # fetch transaction by project id
    @classmethod
    def fetch_transaction_by_project_id(cls,Project_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Financials WHERE Project_id=?
            """
        cursor.execute(sql, (Project_id, ))
        return cursor.fetchone()
        cursor.close()




    # fetch transaction by client id
    @classmethod
    def fetch_transaction_by_client_id(cls,Client_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Financials WHERE Client_id=?
            """
        cursor.execute(sql, (Client_id, ))
        return cursor.fetchone()
        cursor.close()
    
     # fetch transaction by Supplier id
    @classmethod
    def fetch_transaction_by_supplier_id(cls,Supplier_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Financials WHERE Supplier_id=?
            """
        cursor.execute(sql, (Supplier_id, ))
        return cursor.fetchone()
        cursor.close()

    # fetch all the transaction
    @classmethod
    def fetch_all_transactions(cls):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Financials
            """
        cursor.execute(sql)
        return cursor.fetchall()
        cursor.close()



    # update transaction
    @classmethod
    def update_transaction(cls,Transaction_id,  Transaction_type,Transaction_amount,Transaction_date,Personnel_id,Project_id,Client_id, Supplier_id):
        cursor=conn.cursor()
        sql="""
            UPDATE Financials SET Transaction_type =?,Transaction_amount =?,Transaction_date =?,Personnel_id =?,Project_id =?,Client_id =?, Supplier_id =? WHERE Transaction_id=?
            """
        cursor.execute(sql, (Transaction_type ,Transaction_amount ,Transaction_date ,Personnel_id ,Project_id ,Client_id , Supplier_id , Transaction_id))
        conn.commit()
        cursor.close()
        return Transaction_id
    
    # delete transaction
    @classmethod
    def delete_transactions(cls,Transaction_id):
        cursor = conn.cursor()
        sql="""
            DELETE FROM Financials WHERE Transaction_id=?
            """
        cursor.execute(sql ,(Transaction_id,))
        conn.commit()
        return Transaction_id
        cursor.close()

    # count transaction by transaction_id
    @classmethod
    def count_transaction_by_transaction_id(cls):
        cursor=conn.cursor()
        sql="""
            SELECT COUNT(*) FROM Financials
            """
        cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()
    

     # count transactions by personnel id
    @classmethod
    def count_transaction_by_personnel_id(cls,Personnel_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Financials WHERE Personnel_id=?
           """
       cursor.execute(sql,(Personnel_id))
       return cursor.fetchone()
       cursor.close()

    # count transactions by project id
    @classmethod
    def count_transaction_by_project_id(cls,Project_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Financials WHERE Project_id=?
           """
       cursor.execute(sql,(Project_id))
       return cursor.fetchone()
       cursor.close()

    # count transactions by client id
    @classmethod
    def count_transaction_by_client_id(cls,Client_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Financials WHERE Client_id=?
           """
       cursor.execute(sql,(Client_id))
       return cursor.fetchone()
       cursor.close()

        # count transactions by supplier id
    @classmethod
    def count_transaction_by_supplier_id(cls,Supplier_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Financials WHERE Supplier_id=?
           """
       cursor.execute(sql,(Supplier_id))
       return cursor.fetchone()
       cursor.close()