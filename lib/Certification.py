from lib.config import conn
class Certification:
    #create certificate
    @classmethod
    def create_certficate(cls,Personnel_id,Certification_number,Certification_name,Certification_expiry_date):
        cursor =conn.cursor()
        sql="""
            INSERT INTO Certification(Personnel_id, Certification_number,Certification_name,Certification_expiry_date)
            OUTPUT INSERTED.Certificate_id
            VALUES(?,?,?,?)
            """
        cursor.execute(sql, (Personnel_id, Certification_number, Certification_name, Certification_expiry_date))

        certification_id= cursor.fetchone()[0]
        conn.commit()
        return certification_id
        cursor.close()
     
    #fetch a certificate by certificate id
    @classmethod
    def fetch_single_certificate(cls ,Certification_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Certification WHERE Certification_id =?
            """
        cursor.execute(sql, (Certification_id, ))
        conn.commit()
        return cursor.fetchone()
        cursor.close()

    # fetch a certificate by personnel id
    @classmethod
    def fetch_certificate_by_personnel_id(cls,Personnel_id):
        cursor=conn.cursor()
        sql="""
              SELECT * FROM Certification WHERE Personnel_id = ?
            """
        cursor.execute(sql,(Personnel_id, ))
        conn.commit()
        return cursor.fetchone()
        cursor.close()
        

    # fetch all certifcates
    @classmethod
    def fetch_all_certificate(cls):
        cursor= conn.cursor()
        sql="""
            SELECT * FROM Certification
            """
        cursor.execute(sql)
        return cursor.fetchall()
        cursor.close()
    
    # delete a certificate by id
    @classmethod
    def delete_certificate(cls, Certification_id):
        cursor = conn.cursor()
        sql="""
            DELETE FROM Certification WHERE Certfification_id=?
            """
        cursor.execute(sql, (Certification_id, ))
        conn.commit()
        return Certification_id
        cursor.close()

    # update a certificate by id
    @classmethod
    def update_certificate(cls ,Certification_id ,Certification_number,Certification_name,Certification_expiry_date):
        cursor= conn.cursor()
        sql="""
            
             UPDATE Certification SET Certification_number=?,Certification_name=?,Certification_expiry_date=? WHERE Certification_id=?
            """
        cursor.execute(sql,(( Certification_number,Certification_name, Certification_expiry_date, Certification_id)))
        conn.commit()
        cursor.close()
        return Certification_id

    
    # count certicates by Certification_id
    @classmethod
    def count_certificate(cls):
        cursor=conn.cursor()
        sql="""
            SELECT COUNT(*) FROM Certification
            """
        cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()

    # count certificates by personnel_id
    @classmethod 
    def count_certficate_by_personnel_id(cls,Personnel_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Certification WHERE Personnel_id=?
           """
       cursor.execute(sql,(Personnel_id,))
       return cursor.fetchone()
       cursor.close()
    