from lib.config import conn 
class Suppliers:
    #  create suppliers
    @classmethod
    def create_suppliers(cls, Supplier_name, Supplier_email, Supplier_phone_number, Supplier_identity_number, Supplier_status, Remaining_amount):
        cursor=conn.cursor()
        sql="""
                INSERT INTO Suppliers(Supplier_name,Supplier_email,Supplier_phone_number,Supplier_identity_number,Supplier_status,Remaining_amount)
                OUTPUT INSERTED.Supplier_id
                 VALUES(?,?,?,?,?,?)
            """
        cursor.execute(sql,( Supplier_name, Supplier_email, Supplier_phone_number, Supplier_identity_number,Supplier_status,Remaining_amount))
        supplier_id=cursor.fetchone()[0]
        conn.commit()
        return supplier_id 
        cursor.close()
    
    # get supplier by id
    @classmethod
    def fetch_single_supplier(cls,Supplier_id):
        cursor= conn.cursor()
        sql="""
                SELECT * FROM Suppliers WHERE Supplier_id =?
            """
        cursor.execute(sql, (Supplier_id,))
        return cursor.fetchone()
        cursor.close()

    # update supplier by id
    @classmethod
    def update_supplier_by_id(cls, Supplier_id, Supplier_name, Supplier_email, Supplier_phone_number, Supplier_identity_number, Supplier_status, Remaining_amount):
        cursor = conn.cursor()  
        sql="""
            UPDATE Suppliers SET Supplier_name =?,Supplier_email=?,Supplier_phone_number=?,Supplier_identity_number=?,Supplier_status=?,Remaining_amount=? WHERE Supplier_id =?
            """
        cursor.execute(sql, (Supplier_name, Supplier_email, Supplier_phone_number, Supplier_identity_number, Supplier_status, Remaining_amount, Supplier_id))
        conn.commit()
        cursor.close()
        return Supplier_id
    
    # delete supplier by id
    @classmethod
    def delete_single_supplier(cls,Supplier_id):
        cursor=conn.cursor()
        sql="""
                 DELETE FROM Suppliers where Supplier_id=?
            """
        cursor.execute(sql ,(Supplier_id))
        conn.commit()
        return Supplier_id
        cursor.close()

    # fetch all suppliers
    @classmethod
    def fetch_all_supplier(cls):
        cursor=conn.cursor()
        sql="""
               SELECT * FROM Suppliers
            """ 
        cursor.execute(sql) 
        return cursor.fetchall()
        cursor.close()

    # count all suppliers
    @classmethod
    def count_suppliers(cls):
        cursor=conn.cursor()
        sql="""
                 SELECT COUNT(*) FROM Suppliers
            """
        cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()


