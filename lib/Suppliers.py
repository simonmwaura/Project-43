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
        cursor.execute(sql, (Supplier_id, ))
        result = cursor.fetchone()
        return (
                "Supplier Details:\n"
                "ID: {0}\nName: {1}\nEmail: {2}\nPhone: {3}\n"
                "ID Number: {4}\nStatus: {5}\nBalance Due: KES {6:,.2f}"
            ).format(
                result[0], result[1], result[2], result[3],
                result[4], result[5], float(result[6])
            )
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
        cursor.execute(sql ,( Supplier_id, ))
        conn.commit()
        return Supplier_id
        cursor.close()

    # fetch all suppliers
    @classmethod
    def fetch_all_supplier(cls):
        cursor=conn.cursor()
        sql="""
               SELECT * FROM Suppliers ORDER BY Supplier_id
            """ 
        cursor.execute(sql) 
        results = cursor.fetchall()
        header = "{:<5} {:<30} {:<15} {:<10} {:>15}".format(
                "ID", "Supplier Name", "Phone", "Status", "Balance (KES)"
            )
        separator = "-" * 80
        rows = [header, separator]

        for sup in results:
                rows.append("{:<5} {:<30} {:<15} {:<10} {:>15,.2f}".format(
                    sup[0],
                    sup[1][:28],  
                    sup[3],
                    sup[5],
                    float(sup[6])
                ))
            
        return "\n".join(rows)
        cursor.close()

    # count all suppliers
    @classmethod
    def count_suppliers(cls):
        cursor=conn.cursor()
        sql="""
                 SELECT COUNT(*) FROM Suppliers
            """
        count = cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()


