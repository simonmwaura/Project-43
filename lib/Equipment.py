from lib.config import conn ,cursor
class Equipment:
    #create Equipment
    @classmethod
    def create_Equipment(cls,Supplier_id,Equipment_name,Equipment_quantity,Equipment_code ,Date_Bought,Equipment_status):
        cursor =conn.cursor()
        sql="""
            INSERT INTO Equipment(Supplier_id,Equipment_name, Equipment_quantity,Equipment_code ,Date_Bought ,Equipment_status)
            OUTPUT INSERTED.Equipment_id
            VALUES(?,?,?,?)
            """
        cursor.execute(sql, (Supplier_id,  Equipment_name, Equipment_quantity, Equipment_code ,Date_Bought,Equipment_status))
        Equipment_id= cursor.fetchone()[0]
        conn.commit()
        return Equipment_id
        cursor.close()
     
    #fetch a Equipment by Equipment id
    @classmethod
    def fetch_single_Equipment(cls ,Equipment_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Equipment WHERE Equipment_id =?
            """
        cursor.execute(sql, (Equipment_id, ))
        conn.commit()
        return cursor.fetchone()
        cursor.close()

    # fetch a Equipment by Supplier id
    @classmethod
    def fetch_Equipment_by_Supplier_id(cls,Supplier_id):
        cursor=conn.cursor()
        sql="""
              SELECT * FROM Equipment WHERE Supplier_id = ?
            """
        cursor.execute(sql,(Supplier_id, ))
        conn.commit()
        return cursor.fetchone()
        cursor.close()
        

    # fetch all certifcates
    @classmethod
    def fetch_all_Equipment(cls):
        cursor= conn.cursor()
        sql="""
            SELECT * FROM Equipment
            """
        cursor.execute(sql)
        return cursor.fetchall()
        cursor.close()
    
    # delete a Equipment by id
    @classmethod
    def delete_Equipment(cls, Equipment_id):
        cursor = conn.cursor()
        sql="""
            DELETE FROM Equipment WHERE Equipment_id=?
            """
        cursor.execute(sql, (Equipment_id, ))
        conn.commit()
        return Equipment_id
        cursor.close()

    # update a Equipment by id
    @classmethod
    def update_Equipment(cls ,
                         Equipment_id ,Supplier_id ,Equipment_name,Equipment_quantity,Equipment_code,
                         Date_Bought,Equipment_status):
        cursor= conn.cursor()
        sql="""
            
             UPDATE Equipment SET Supplier_id=?,Equipment_name=?,Equipment_quantity=?,Equipment_code, Date_Bought,Equipment_status=? WHERE Equipment_id=?
            """
        cursor.execute(sql,(( Supplier_id ,Equipment_name, Equipment_quantity, Equipment_code , Date_Bought,Equipment_status, Equipment_id)))
        conn.commit()
        cursor.close()
        return Equipment_id

    
    # count certicates by Equipment_id
    @classmethod
    def count_Equipment(cls):
        cursor=conn.cursor()
        sql="""
            SELECT COUNT(*) FROM Equipment
            """
        cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()

    # count Equipment by Supplier_id
    @classmethod 
    def count_Equipment_by_Supplier_id(cls,Supplier_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Equipment WHERE Supplier_id=?
           """
       cursor.execute(sql,(Supplier_id,))
       return cursor.fetchone()
       cursor.close()
    