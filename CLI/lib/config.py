import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Housing Development;"
    "Trusted_Connection=yes;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor() 
print("<-----------------Connection successful----------------->")


class Database:
     def create_tables(self):
        sql1="""
               CREATE TABLE Client(
                    Client_id INT IDENTITY(1,1) PRIMARY KEY,
                    Client_name VARCHAR(50) NOT NULL UNIQUE,
                    Client_email VARCHAR(100) NOT NULL UNIQUE,
                    Client_phone_number VARCHAR(10) NOT NULL UNIQUE,
                    Client_identity_number VARCHAR(9) NOT NULL UNIQUE,

                    CONSTRAINT check_email CHECK(Client_email LIKE '%@%.%'),
                    CONSTRAINT check_phone_number CHECK(Client_phone_number LIKE '07%' AND LEN(Client_phone_number) = 10),
                    CONSTRAINT check_identity_number CHECK (LEN(Client_identity_number) BETWEEN 8 AND 9)
               );               
             """
        cursor.execute(sql1)

        sql2="""
               CREATE TABLE Suppliers(
                    Supplier_id INT IDENTITY(1,1) PRIMARY KEY,
                    Supplier_name VARCHAR(100) NOT NULL UNIQUE,
                    Supplier_email VARCHAR(100) NOT NULL UNIQUE,
                    Supplier_phone_number VARCHAR(10) NOT NULL UNIQUE,
                    Supplier_identity_number VARCHAR(9) NOT NULL UNIQUE,
                    Supplier_status VARCHAR(20) NOT NULL,
                    Remaining_amount DECIMAL(15,2) NOT NULL,

                    CONSTRAINT check_supplier_email CHECK(Supplier_email LIKE '%_@__%.__%'),
                    CONSTRAINT check_supplier_phone_number CHECK(Supplier_phone_number LIKE '07%' AND LEN(Supplier_phone_number) = 10),
                    CONSTRAINT check_supplier_identity_number CHECK(LEN(Supplier_identity_number) BETWEEN 8 AND 9),
                    CONSTRAINT check_status CHECK(Supplier_status IN ('Active','Inactive','Pending','Suspended')),
                    CONSTRAINT check_remaining_amount CHECK(Remaining_amount >= 0.00)
              ); 
            """
        cursor.execute(sql2)
        
        sql3="""
               CREATE TABLE Personnel(
                    Personnel_id INT IDENTITY(1,1) PRIMARY KEY, 
                    Personnel_name VARCHAR(50) NOT NULL UNIQUE,
                    Personnel_identity_number VARCHAR(9) NOT NULL UNIQUE,
                    Personnel_code VARCHAR(50) NOT NULL UNIQUE,
                    Personnel_wages DECIMAL(15,2) NOT NULL,
                    Personnel_type VARCHAR(50) NOT NULL,
                    Personnel_role VARCHAR(50) NOT NULL,

                    CONSTRAINT check_personnel_identity_number CHECK (LEN(Personnel_identity_number) BETWEEN 8 AND 9),
                    CONSTRAINT check_personnel_type CHECK (Personnel_type IN ('Professional','Skilled','Unskilled')),                     
                    CONSTRAINT check_personnel_wages CHECK (Personnel_wages >= 0.00),
                    CONSTRAINT check_personnel_role CHECK(
                    (Personnel_type = 'Professional' AND Personnel_role IN (
                    'Project Manager','Architect','Structural Engineer','Quantity Surveyor','Mechanical Engineer','Electrical Engineer','Site Supervisor)) OR
                    (Personnel_type = 'Skilled' AND Personnel_role IN ('Mason','Plumber','Electrician','Carpenter','Welder', 'Painter','Roofer'))   OR
                    (Personnel_type = 'Unskilled' AND Personnel_role IN ('Laborer'))
                    ),
                    CONSTRAINT check_personnel_code CHECK (
                    (Personnel_type = 'Professional' AND Personnel_code LIKE 'P[A-Z][A-Z][0-9][0-9][0-9]') OR
                    (Personnel_type = 'Skilled' AND Personnel_code LIKE 'S[A-Z][A-Z][0-9][0-9][0-9]') OR
                    (Personnel_type = 'Unskilled' AND Personnel_code LIKE 'U[A-Z][A-Z][0-9][0-9][0-9]')
                    )

             );
           """
        cursor.execute(sql3)

        sql4="""
                 CREATE TABLE Projects(
                 Project_id INT IDENTITY(1,1) PRIMARY KEY,
                 Client_id INT NOT NULL,
                 Personnel_id INT NOT NULL,
                 Project_name VARCHAR(100) NOT NULL UNIQUE,
                 Project_start_date DATE NOT NULL,
                 Project_end_date DATE NOT NULL,
                 Project_budget DECIMAL(15,2) NOT NULL,
                 Project_status VARCHAR(10) NOT NULL,

 
                 CONSTRAINT client_project_foreign_key FOREIGN KEY (Client_id) REFERENCES Client(Client_id) ON DELETE CASCADE,
                 CONSTRAINT personnel_project_foreign_key FOREIGN KEY (Personnel_id) REFERENCES Personnel(Personnel_id) ON DELETE CASCADE,
                 CONSTRAINT check_project_budget CHECK ( Project_budget >= 0.00),
                 CONSTRAINT check_project_status CHECK ( Project_status IN ('Pending','In progress','Completed','On hold','Cancelled'),)
                 CONSTRAINT Check_project_date CHECK (Project_end_date > Project_start_date)
                 );
            """
        cursor.execute(sql4)

        sql5="""
              CREATE TABLE Certification(
                Certification_id INT IDENTITY(1,1) PRIMARY KEY,
                Personnel_id INT NOT NULL ,
                Certification_number VARCHAR(100) NOT NULL UNIQUE,
                Certification_name VARCHAR(150) NOT NULL,
                Certification_expiry_date DATE NOT NULL,
                Certification_status VARCHAR(20) NOT NULL DEFAULT 'Active',


                CONSTRAINT personnel_certification_foreign_key FOREIGN KEY (Personnel_id) REFERENCES Personnel(Personnel_id) ON DELETE CASCADE,
                CONSTRAINT check_certification_expiry_date CHECK (Certfification_expiry_date > GETDATE()),
                CONSTRAINT check_certification_status CHECK (Certification_status IN ('Active','Expired','Revoked','Pending')),
                CONSTRAINT check_skilled_personnel_only CHECK (
            EXISTS (
                SELECT 1 FROM Personnel p 
                WHERE p.Personnel_id = Personnel_id 
                AND p.Personnel_type = 'Skilled'
            )
        )
              );
             """
        cursor.execute(sql5)

        sql6="""
              CREATE TABLE Equipment(
                Equipment_id INT IDENTITY(1,1) PRIMARY KEY,
                Supplier_id INT NOT NULL,
                Equipment_name VARCHAR(20) NOT NULL,
                Equipment_quantity INT NOT NULL,
                Equipment_code VARCHAR(50) NOT NULL UNIQUE,
                Date_Bought DATE NOT NULL,
                Equipment_status VARCHAR(20) CHECK (Equipment_status IN ('Active', 'In Repair', 'Retired')),
                CONSTRAINT supplier_equipment_foreign_key FOREIGN KEY (Supplier_id) REFERENCES Suppliers(Supplier_id)
              );
            """
        cursor.execute(sql6)
        sql7="""
             CREATE TABLE Materials(
               Material_id INT IDENTITY(1,1) PRIMARY KEY,
               Supplier_id INT NOT NULL,
               Material_name VARCHAR(50) NOT NULL,
               Material_quantity INTEGER NOT NULL,
               Material_price DECIMAL(15,2)  NOT NULL,
               Material_status VARCHAR(20) CHECK (Material_status IN ('Available','Not Available')),
               CONSTRAINT supplier_material_foreign_key FOREIGN KEY(Supplier_id) REFERENCES Suppliers(Supplier_id) ON DELETE CASCADE
             );
             """
        cursor.execute(sql7)
        
        sql8="""
             CREATE TABLE Financials (
              Transaction_id INT IDENTITY(1,1) PRIMARY KEY,
              Transaction_type VARCHAR(25) NOT NULL CHECK( Transaction_type IN ('Personnel Wages','Supplier Payments','Client Payments')),
              Transaction_amount DECIMAL(15,2) NOT NULL,
              Transaction_date DATE NOT NULL,
              Personnel_id INT,
              Project_id INT,
              Client_id INT,
              Supplier_id INT,
              CONSTRAINT personnel_financials_foreign_key FOREIGN KEY (Personnel_id) REFERENCES Personnel(Personnel_id)  ,
              CONSTRAINT project_financials_foreign_key FOREIGN KEY(Project_id) REFERENCES Projects(Project_id) ,
              CONSTRAINT client_financials_foreign_key FOREIGN KEY(Client_id) REFERENCES Client(Client_id) ,
              CONSTRAINT supplier_financials_foreign_key FOREIGN KEY(Supplier_id) REFERENCES Suppliers(Supplier_id) 
             );
             """
        cursor.execute(sql8)
       
        conn.commit()

     def delete_tables(self):
        sql1="""
             DROP TABLE IF EXISTS Financials;
             """
        cursor.execute(sql1)

        sql2="""
              DROP TABLE IF EXISTS Materials;
              """
        cursor.execute(sql2)

        sql3="""
              DROP TABLE IF EXISTS Equipment;
              """
        cursor.execute(sql3)

        sql4="""
              DROP TABLE IF EXISTS Certification;
              """
        cursor.execute(sql4)

        sql5="""
             DROP TABLE IF EXISTS Projects;
             """
        cursor.execute(sql5)

        sql6="""
             DROP TABLE IF EXISTS Personnel
             """
        cursor.execute(sql6)

        sql7="""
                  DROP TABLE IF EXISTS Client
             """ 
        cursor.execute(sql7)
        sql8="""
             DROP TABLE IF EXISTS Suppliers
             """
        cursor.execute(sql8)

        conn.commit()

     def create_views(self):
          #  suppliers view
          # suppliers should be able to seee what materials/ equipment they are supplying

          #  admin view
          # admin should see everything
          sql1="""
               CREATE VIEW Admin_view AS 
               SELECT Client_id,Client_name,CLient_phone_number
          """
          # client view
          # client should see his name ,email,phone number , project name , project status , project budget

          sql2="""
               CREATE VIEW Client_view AS
               SELECT Client_id , Client_name ,Client_phone_number ,
               FROM Client;
          """

          # personnel view
          # personnel should see his name, his wages his role and sub role, he should also know which project he is working on
          sql3="""
               CREATE VIEW Personnel_view AS 
               SELECT Personnel_name , Personnel_wages, Personnel_role,
               sub_role
          """
          
          # finance view
          sql4 = """
               CREATE VIEW Finance_view AS 
               SELECT Transaction_type,Transaction_date,Personnel_id,Project_id,Client_id,Supplier_id
               """
     
     def delete_views(self):
          sql1=" DROP VIEW IF EXISTS admin_view ; "
          cursor.execute(sql1)

          sql2="""
               DROP VIEW IF EXISTS Personnel_view ;
               """
          cursor.execute(sql2)
          sql3="""
               DROP VIEW IF EXISTS Client_view ;
                    """
          cursor.execute(sql3)
          sql4="""
               DROP VIEW IF EXISTS Finance_view ;
               """
          cursor.execute(sql4)
          cursor.commit()
               


db_obj=Database()
db_obj.delete_tables()
db_obj.delete_views()
print("<------------THE TABLES HAVE BEEN DROPPED------------->")
print("<------------THE VIEWS HAVE BEEN DROPPED------------->")
print("<------------CREATING THE TABLES---------->")
db_obj.create_tables()
db_obj.create_views()
print("<-------------THE TABLES HAVE BEEN CREATED-------------->")
print("<------------THE TABLES HAVE BEEN CREATED------------->")

# conn.close()
# conn.close()
    