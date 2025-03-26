import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Housing Development;"
    "Trusted_Connection=yes;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor() 
print("Connection successful!")

class Database:
    def create_tables(self):
        sql1="""
                CREATE TABLE Client(
                 Client_id INT IDENTITY(1,1) PRIMARY KEY,
                 Client_name VARCHAR(50) NOT NULL UNIQUE,
                 Client_email VARCHAR(100) NOT NULL UNIQUE,
                 Client_phone_number VARCHAR(25) NOT NULL,
                 Client_identity_number INT NOT NULL UNIQUE
                );               
             """
        cursor.execute(sql1)

        sql2="""
               CREATE TABLE Suppliers(
               Supplier_id INT IDENTITY(1,1) PRIMARY KEY,
               Supplier_name VARCHAR(100) NOT NULL UNIQUE,
               Supplier_email VARCHAR(100) NOT NULL,
               Supplier_phone_number VARCHAR(25) NOT NULL,
               Supplier_identity_number INT NOT NULL UNIQUE,
               Supplier_status VARCHAR(20) CHECK (Supplier_status IN ('Active','Inactive','Pending','Suspended')),
               Remaining_amount DECIMAL(15,2) NOT NULL 
              ); 
            """
        cursor.execute(sql2)
        
        sql3="""
             CREATE TABLE Personnel(
              Personnel_id INT IDENTITY(1,1) PRIMARY KEY,
              Personnel_name VARCHAR(50) NOT NULL UNIQUE,
              Personnel_identity_number INT NOT NULL UNIQUE,
              Personnel_code VARCHAR(50) NOT NULL UNIQUE,
              Personnel_wages DECIMAL(15,2) NOT NULL,
              Personnel_type VARCHAR(50) NOT NULL CHECK(Personnel_type IN ('Professional','Skilled','Unskilled')),
              Personnel_role VARCHAR(50) NOT NULL,
             );
              """
        cursor.execute(sql3)

        sql4="""
                 CREATE TABLE Projects(
                 Project_id INT IDENTITY(1,1) PRIMARY KEY,
                 Project_name VARCHAR(100) NOT NULL UNIQUE,
                 Project_start_date DATE NOT NULL,
                 Project_end_date DATE NOT NULL,
                 Project_budget DECIMAL(18,2) NOT NULL,
                 Client_id INT,
                 Project_status VARCHAR(50) NOT NULL CHECK(Project_status IN ('Pending','In progress','Completed','On hold')), 
                 CONSTRAINT client_project_foreign_key FOREIGN KEY (Client_id) REFERENCES Client(Client_id) ON DELETE CASCADE,
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
                CONSTRAINT personnel_certification_foreign_key FOREIGN KEY (Personnel_id) REFERENCES Personnel(Personnel_id) ON DELETE CASCADE
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

db_obj=Database()
db_obj.delete_tables()
print("<------------THE TABLES HAVE BEEN DROPPED------------->")
print("<------------CREATING THE TABLES---------->")
db_obj.create_tables()
print("<-------------THE TABLES HAVE BEEN CREATED-------------->")

# cursor.close()
# conn.close()
    