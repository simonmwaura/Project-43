from lib.config import conn 
class Personnel:
    # create personnel
    def create_personnel(cls,Personnel_name,Personnel_identity_number,Personnel_code,Personnel_wages,Personnel_type,Personnel_role):
        cursor = conn.cursor()
        sql="""
               INSERT INTO Personnel(Personnel_name,Personnel_identity_number,Personnel_code,Personnel_wages,Personnel_type,Personnel_role)
               OUTPUT INSERTED.Personnel.id
               VALUES(?,?,?,?,?,?)
            """
        cursor.execute(sql,( Personnel_name, Personnel_identity_number, Personnel_code,  Personnel_wages, Personnel_type, Personnel_role))

        personnel_id = cursor.fetchone()[0]
        conn.commit()
        return personnel_id
        cursor.close()
    #  get personnel by id
    def fetch_single_personnel(cls,Personnel_id):
        cursor = conn.cursor()
        sql="""
             SELECT * FROM Personnel WHERE Personnel_id=?
            """
        cursor.execute(sql, (Personnel_id, ))
        return cursor.fetchone()
        cursor.close
    #  fetch all personnel
    def fetch_all_personnel(cls):
        cursor=conn.cursor()
        sql="""
                SELECT * FROM Personnel
            """
        cursor.execute(sql)
        return cursor.fetchall()
        cursor.close
    # update personnel by id

    def update_all_personnel(cls , Personnel_id, Personnel_name, Personnel_identity_number, Personnel_code, Personnel_wages, Personnel_type, Personnel_role):
        cursor=conn.cursor()
        sql="""
            UPDATE Personnel SET Personnel_name=?,Personnel_identity_number=?,Personnel_code=?,Personnel_wages=?,Personnel_type=?,Personnel_role=? WHERE Personnel_id=?
            """
        cursor.execute(sql,( Personnel_name,  Personnel_identity_number, Personnel_code, Personnel_wages, Personnel_type, Personnel_role,Personnel_id))
        conn.commit()
        cursor.close()
        return Personnel_id
    
    # delete personnel by id
    def delete_single_personnel(cls, Personnel_id):
        cursor = conn.cursor()
        sql="""
               DELETE FROM Personnel WHERE Personnel_id=?
            """
        cursor.execute(sql,(Personnel_id,))
        conn.commit()
        return Personnel_id
        cursor.close()


    # count personnel
    @classmethod
    def count_personnel(cls):
        cursor=conn.cursor
        sql="""
             SELECT COUNT(*) FROM Personnel
            """
        cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()
