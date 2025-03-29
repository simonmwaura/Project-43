from lib.config import conn ,cursor
class Materials:
    #create Materials
    @classmethod
    def create_Materials(cls,Supplier_id,Material_name,Material_quantity,Material_price ,Material_status):
        cursor =conn.cursor()
        sql="""
            INSERT INTO Materials(Supplier_id,Material_name, Material_quantity,Material_price , Material_status)
            OUTPUT INSERTED.Material_id
            VALUES(?,?,?,?)
            """
        cursor.execute(sql, (Supplier_id,  Material_name, Material_quantity, Material_price ,Material_status))
        Material_id= cursor.fetchone()[0]
        conn.commit()
        return Material_id
        cursor.close()
     
    #fetch a Material by Material id
    @classmethod
    def fetch_single_Material(cls ,Material_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Materials WHERE Material_id =?
            """
        cursor.execute(sql, (Material_id, ))
        conn.commit()
        return cursor.fetchone()
        cursor.close()

    # fetch a Material by Supplier id
    @classmethod
    def fetch_Materials_by_Supplier_id(cls,Supplier_id):
        cursor=conn.cursor()
        sql="""
              SELECT * FROM Materials WHERE Supplier_id = ?
            """
        cursor.execute(sql,(Supplier_id, ))
        conn.commit()
        return cursor.fetchone()
        cursor.close()
        

    # fetch all certifcates
    @classmethod
    def fetch_all_Materials(cls):
        cursor= conn.cursor()
        sql="""
            SELECT * FROM Materials
            """
        cursor.execute(sql)
        return cursor.fetchall()
        cursor.close()
    
    # delete a Material by id
    @classmethod
    def delete_Materials(cls, Material_id):
        cursor = conn.cursor()
        sql="""
            DELETE FROM Materials WHERE Certfification_id=?
            """
        cursor.execute(sql, (Material_id, ))
        conn.commit()
        return Material_id
        cursor.close()

    # update a Material by id
    @classmethod
    def update_Materials(cls ,
                         Material_id ,Supplier_id ,Material_name,Material_quantity,Material_price,Material_status):
        cursor= conn.cursor()
        sql="""
            
             UPDATE Materials SET Supplier_id=?,Material_name=?,Material_quantity=?,Material_price, Material_status=? WHERE Material_id=?
            """
        cursor.execute(sql,(( Supplier_id ,Material_name, Material_quantity, Material_price , Material_status, Material_id)))
        conn.commit()
        cursor.close()
        return Material_id

    
    # count materials by Material_id
    @classmethod
    def count_Materials(cls):
        cursor=conn.cursor()
        sql="""
            SELECT COUNT(*) FROM Materials
            """
        cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()

    # count Materials by Supplier_id
    @classmethod 
    def count_Materials_by_Supplier_id(cls,Supplier_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Materials WHERE Supplier_id=?
           """
       cursor.execute(sql,(Supplier_id,))
       return cursor.fetchone()
       cursor.close()
    