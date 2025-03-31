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
        cursor.close()
        return certification_id
     
    #fetch a certificate by certificate id
    @classmethod
    def fetch_single_certificate(cls ,Certification_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Certification WHERE Certification_id =?
            """
        cursor.execute(sql, (Certification_id, ))
        conn.commit()
        result = cursor.fetchone()
        cursor.close()
        result(
                f"Certification ID: {result[0]}\n"
                f"Personnel ID: {result[1]}\n"
                f"Number: {result[2]}\n"
                f"Name: {result[3]}\n"
                f"Expiry: {result[4].strftime('%Y-%m-%d')}"
        )


    # fetch a certificate by personnel id
    @classmethod
    def fetch_certificate_by_personnel_id(cls,Personnel_id):
        cursor=conn.cursor()
        sql="""
              SELECT * FROM Certification WHERE Personnel_id = ?
            """
        cursor.execute(sql,(Personnel_id, ))
        conn.commit()
        result = cursor.fetchall()
        cursor.close()

        output = [f"Certifications for Personnel ID {Personnel_id}:"]
        for cert in result:
            output.append(
                f"\nID: {cert[0]} | Number: {cert[2]}"
                f"\nName: {cert[3]}"
                f"\nExpiry: {cert[4].strftime('%Y-%m-%d')}\n"
                f"{'-'*40}"
            )
        return "\n".join(output) 
        

    # fetch all certifcates
    @classmethod
    def fetch_all_certificate(cls):
        cursor= conn.cursor()
        sql="""
            SELECT * FROM Certification
            """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        output = ["All Certifications:"]
        for cert in results:
            output.append(
                f"{cert[0]:<5} {cert[1]:<10} {cert[2]:<15} {cert[3][:20]:<20} {cert[4].strftime('%Y-%m-%d')}"
            )
        return "\n".join(output)
    
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
    