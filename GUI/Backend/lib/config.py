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
               Id INT IDENTITY(1,1) PRIMARY KEY,
               Name VARCHAR(50) NOT NULL ,
               Email VARCHAR(100) NOT NULL UNIQUE,
               Phone_Number VARCHAR(13) NOT NULL UNIQUE,
               National_Identity_Number VARCHAR(9) NOT NULL UNIQUE,
               CONSTRAINT Client_check_email CHECK(Email LIKE '%_@%_.__%' AND Email NOT LIKE '%@%@%' AND Email NOT LIKE '%..%'),
               CONSTRAINT  Client_check_phone CHECK(Phone_Number LIKE '+254%' AND LEN(Phone_Number) = 13 AND Phone_Number NOT LIKE '%[^0-9]%'),
               CONSTRAINT Client_check_identity CHECK (LEN(National_Identity_Number) BETWEEN 8 AND 9 AND National_Identity_Number NOT LIKE '%[^0-9]%')
          );               
             """
        cursor.execute(sql1)

        sql2="""
          CREATE TABLE Suppliers(
               Id INT IDENTITY(1,1) PRIMARY KEY,
               Name VARCHAR(100) NOT NULL ,
               Email VARCHAR(100) NOT NULL UNIQUE,
               Phone_Number VARCHAR(13) NOT NULL UNIQUE,
               Status VARCHAR(20) NOT NULL,
               Remaining_amount DECIMAL(15,2) NOT NULL,
               CONSTRAINT Suppliers_check_email CHECK(Email LIKE '%_@%_.__%' AND Email NOT LIKE '%@%@%' AND Email NOT LIKE '%..%'),
               CONSTRAINT Suppliers_check_phone CHECK(Phone_Number LIKE '+254%' AND LEN(Phone_Number) = 13 AND Phone_Number NOT LIKE '%[^0-9]%'),
               CONSTRAINT Suppliers_check_status  CHECK(Status IN ('Active','Inactive','Pending','Suspended')),
               CONSTRAINT check_Remaining_amount CHECK( Remaining_amount >= 0.00 ) 
          ); 
            """
        cursor.execute(sql2)
        
        sql3="""
          CREATE TABLE Personnel(
               Id INT IDENTITY(1,1) PRIMARY KEY, 
               Name VARCHAR(50) NOT NULL ,
               National_Identity_Number VARCHAR(9) NOT NULL UNIQUE,
               Type VARCHAR(15) NOT NULL,
               Wages DECIMAL(15,2) NOT NULL,
               Role VARCHAR(25) NOT NULL,
               Code VARCHAR(6) NOT NULL UNIQUE,
               CONSTRAINT check_identity_Number CHECK (LEN(National_Identity_Number) BETWEEN 8 AND 9 AND National_Identity_Number NOT LIKE '%[^0-9]%'),
               CONSTRAINT check_type CHECK (Type IN ('Professional','Skilled','Unskilled')),                     
               CONSTRAINT check_wages CHECK (Wages >= 0.00),
               CONSTRAINT check_role CHECK( 
               (Type = 'Professional' AND Role IN ('Project Manager','Architect','Structural Engineer','Quantity Surveyor','Mechanical Engineer','Electrical Engineer','Site Supervisor'))OR
               (Type = 'Skilled' AND Role IN ('Mason','Plumber','Electrician','Carpenter','Welder', 'Painter','Roofer'))OR
               (Type = 'Unskilled' AND Role IN ('Laborer'))
               ),
               CONSTRAINT check_code CHECK (
               (Type = 'Professional' AND Code LIKE 'P[A-Z][A-Z][0-9][0-9][0-9]') OR
               (Type = 'Skilled' AND Code LIKE 'S[A-Z][A-Z][0-9][0-9][0-9]') OR
               (Type = 'Unskilled' AND Code LIKE 'U[A-Z][A-Z][0-9][0-9][0-9]')
               )
             );
           """
        cursor.execute(sql3)

        sql4="""
          CREATE TABLE Projects(
               Id INT IDENTITY(1,1) PRIMARY KEY,
               Client_id INT NOT NULL,
               Personnel_id INT NOT NULL,
               Name VARCHAR(100) NOT NULL UNIQUE,
               Budget DECIMAL(15,2) NOT NULL,
               Status VARCHAR(10) NOT NULL,
               Start_date DATE NOT NULL,
               End_date DATE NOT NULL,  
               CONSTRAINT client_foreign_key_1 FOREIGN KEY (Client_id) REFERENCES Client(Id) ON DELETE NO ACTION,
               CONSTRAINT personnel_foreign_key_1 FOREIGN KEY (Personnel_id) REFERENCES Personnel(Id) ON DELETE NO ACTION,
               CONSTRAINT check_budget CHECK ( Budget >= 0.00),
               CONSTRAINT Projects_check_status CHECK ( Status IN ('Pending','In progress','Completed','On hold','Cancelled')),
               CONSTRAINT Projects_check_date CHECK (End_date > Start_date)
          );
            """
        cursor.execute(sql4)

        sql5="""
          CREATE TABLE Certification(
               Id INT IDENTITY(1,1) PRIMARY KEY,
               Personnel_id INT NOT NULL ,
               Number VARCHAR(50) NOT NULL UNIQUE,
               Name VARCHAR(100) NOT NULL,
               Expiry_date DATE NOT NULL,
               Status VARCHAR(20) NOT NULL DEFAULT 'Active',
               CONSTRAINT personnel_foreign_key_2 FOREIGN KEY (Personnel_id) REFERENCES Personnel(Id) ON DELETE CASCADE,
               CONSTRAINT Certification_check_expiry_date CHECK (Expiry_date > GETDATE()),
               CONSTRAINT Certification_check_status CHECK (status IN ('Active','Expired','Revoked','Pending'))
          );
             """
        cursor.execute(sql5)

        sql6="""
          CREATE TABLE Equipment(
               Id INT IDENTITY(1,1) PRIMARY KEY,
               Supplier_id INT NOT NULL,
               Name VARCHAR(50) NOT NULL,
               Quantity INT NOT NULL,
               Code VARCHAR(50) NOT NULL UNIQUE,
               Date_Bought DATE NOT NULL,
               Status VARCHAR(20) NOT NULL DEFAULT 'Active' ,
               CONSTRAINT Equipment_check_status CHECK (Status IN ('Active','In Repair','Retired')),
               CONSTRAINT supplier_foreign_key_1 FOREIGN KEY (Supplier_id) REFERENCES Suppliers(Id) ON DELETE NO ACTION,
               CONSTRAINT  Equipment_check_quantity CHECK (Quantity >= 0),
               CONSTRAINT Equipment_check_code CHECK (
                    Code LIKE 'EQ-[A-Z0-9]%' 
                    AND LEN(Code) >= 7          
                    AND Code NOT LIKE '%[^A-Z0-9-]%'
               ), 
               CONSTRAINT unique_equipment_supplier UNIQUE (Supplier_id, Name)
          );
            """
        cursor.execute(sql6)
        sql7="""
          CREATE TABLE Materials(
               Id INT IDENTITY(1,1) PRIMARY KEY,
               Supplier_id INT NOT NULL,
               Name VARCHAR(50) NOT NULL,
               Quantity INT NOT NULL,
               Price DECIMAL(15,2)  NOT NULL,
               Status VARCHAR(20) NOT NULL DEFAULT 'Available',
               CONSTRAINT Materials_check_status  CHECK (Status IN ('Available','Not Available')),  
               CONSTRAINT check_quantity CHECK (Quantity >= 0),
               CONSTRAINT check_Price CHECK (Price >= 0),
               CONSTRAINT unique_material_supplier UNIQUE (Supplier_id, Name)
          );
             """
        cursor.execute(sql7)
        
        sql8="""
             CREATE TABLE Financials (
              Id INT IDENTITY(1,1) PRIMARY KEY,
              Personnel_id INT,
              Project_id INT,
              Client_id INT,
              Supplier_id INT,
              Type VARCHAR(25) NOT NULL,
              Amount DECIMAL(15,2) NOT NULL,
              Transaction_date DATE NOT NULL,
              CONSTRAINT personnel_financials_foreign_key FOREIGN KEY (Personnel_id) REFERENCES Personnel(Id) ON DELETE SET NULL ,
              CONSTRAINT project_financials_foreign_key FOREIGN KEY(Project_id) REFERENCES Projects(Id) ON DELETE SET NULL,
              CONSTRAINT client_financials_foreign_key FOREIGN KEY(Client_id) REFERENCES Client(Id) ON DELETE SET NULL,
              CONSTRAINT supplier_financials_foreign_key FOREIGN KEY(Supplier_id) REFERENCES Suppliers(Id) ON DELETE SET NULL, 
              CONSTRAINT Financials_check_type CHECK( Type IN ('Personnel Wages','Supplier Payments','Client Payments')),
              CONSTRAINT check_amount CHECK(Amount > 0)
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
             DROP TABLE IF EXISTS Personnel;
             """
        cursor.execute(sql6)

        sql7="""
                  DROP TABLE IF EXISTS Client;
             """ 
        cursor.execute(sql7)
        sql8="""
             DROP TABLE IF EXISTS Suppliers;
             """
        cursor.execute(sql8)

        conn.commit()

     def create_views(self):
          #  suppliers view
          # suppliers should be able to seee what materials/ equipment they are supplying

          #  admin view
          # admin should see everything
          sql1="""
               CREATE VIEW admin_view AS
               SELECT 
               Client.Id AS Client_ID, 
               Client.Name AS Client_Name, 
               Client.Email AS Client_Email,
               Client.Phone_Number AS Client_Phone_Number,
               Suppliers.Id AS SupplierID, 
               Suppliers.Name AS Supplier_Name, 
               Suppliers.Status AS Supplier_Status,
               Projects.Id AS ProjectID, 
               Projects.Name AS Project_Name,
               Projects.Budget AS Project_Budget,
               Projects.Status AS Project_Status,
               Personnel.Name AS Personnel_Name,
               Personnel.Type AS Personnel_Type,
               Personnel.Role AS Personnel_Role,
               Financials.Type AS Transactions_Type, 
               Financials.Amount AS Transaction_Amount, 
               Financials.Transaction_date AS  Transaction_date
               FROM Client
               LEFT JOIN Projects  ON Client.Id = Projects.Client_id
               LEFT JOIN Personnel ON Projects.Personnel_id = Personnel.Id
               LEFT JOIN Financials ON Client.Id = Financials.Client_id
               LEFT JOIN Suppliers  ON Financials.Supplier_id = Suppliers.Id;
          """
          cursor.execute(sql1)
          # client view
          # client should see his name ,email,phone number , project name , project status , project budget

          sql2="""
               CREATE VIEW client_view AS
               SELECT 
               Client.Name AS Client_Name, 
               Client.Email AS Client_Email,
               Client.Phone_Number AS Client_Phone_Number,
               Projects.Name AS Project_Name,       
               Projects.Status AS Project_Status,
               Projects.Budget AS Project_Budget,
               Projects.Start_date AS Project_Start_date , 
               Projects.End_date AS Project_End_date
               FROM Client LEFT JOIN Projects ON  Client.Id = Projects.Client_id;
          """

          cursor.execute(sql2)

          # personnel view
          # personnel should see his name, his wages his role and sub role, he should also know which project he is working on
          sql3="""
               CREATE VIEW personnel_view AS
               SELECT 
               Personnel.Name AS Personnel_Name,
               Personnel.Type AS Personnel_Type,
               Personnel.Role AS Personnel_Role,
               Personnel.Wages AS Personnel_Wages,
               Projects.Name AS Projects_Name,
               Projects.Status AS Project_Status
               FROM Personnel LEFT JOIN Projects ON Personnel.Id = Projects.Personnel_id;
          """
          cursor.execute(sql3)
          
          # finance view
          sql4 = """
               CREATE VIEW finance_view AS
               SELECT 
               Financials.Type AS Financials_Type, 
               Financials.Amount AS Financials_Amount, 
               Financials.Transaction_date AS Transaction_date,
               Client.Name AS Client_Name,
               Suppliers.Name AS Supplier_Name,
               Personnel.Name AS Personnel_Name,  
               Projects.Name AS Project_Name
               FROM Financials LEFT JOIN Client ON  Financials.Client_id = Client.Id LEFT JOIN Suppliers ON Financials.Supplier_id = Suppliers.Id LEFT JOIN Personnel ON Financials.Personnel_id = Personnel.Id LEFT JOIN Projects ON Financials.Project_id = Projects.Id;
               """
          cursor.execute(sql4)
          # Suppliers should see their supplied materials/equipment

          sql5 = """
               CREATE VIEW suppliers_view AS
               SELECT 
               Suppliers.Name AS Supplier_Name,
               Suppliers.Email AS Supplier_Email,
               Suppliers.Phone_Number AS Suppliers_Phone_Number,
               Suppliers.Remaining_amount AS Suppliers_Remaining_Amount,
               Materials.Name AS Materials_Name, 
               Materials.Quantity AS Materials_Quantity,
               Materials.Status AS Materials_Status,
               Equipment.Name AS Equipment_Name,
               Equipment.Quantity AS Equipment_Quantity,
               Equipment.Status AS Equipment_Status
               FROM Suppliers LEFT JOIN Materials ON Suppliers.Id = Materials.Supplier_id  LEFT JOIN Equipment  ON Suppliers.Id = Equipment.Supplier_id;
               """
          cursor.execute(sql5)
          conn.commit()
     
     def delete_views(self):
          sql1=" DROP VIEW IF EXISTS admin_view ; "
          cursor.execute(sql1)

          sql2="""
               DROP VIEW IF EXISTS client_view ;
               """
          cursor.execute(sql2)
          sql3="""
               DROP VIEW IF EXISTS personnel_view ;
                    """
          cursor.execute(sql3)
          sql4="""
               DROP VIEW IF EXISTS finance_view ;
               """
          cursor.execute(sql4)
          sql5="""
               DROP VIEW IF EXISTS suppliers_view ;
               """
          cursor.execute(sql5)
          conn.commit()
               


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

conn.commit()
conn.close()
    