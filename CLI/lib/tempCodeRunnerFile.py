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
               CONSTRAINT check_email CHECK(Email LIKE '%_@%_.__%' AND Email NOT LIKE '%@%@%' AND Email NOT LIKE '%..%'),
               CONSTRAINT check_phone_number CHECK(Phone_Number LIKE '+254%' AND LEN(Phone_Number) = 13 AND Phone_Number NOT LIKE '%[^0-9]%'),
               CONSTRAINT check_identity_number CHECK (LEN(National_Identity_Number) BETWEEN 8 AND 9 AND National_Identity_Number NOT LIKE '%[^0-9]%')
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
               CONSTRAINT check_suppliers_Email CHECK(Email LIKE '%_@%_.__%' AND Email NOT LIKE '%@%@%' AND Email NOT LIKE '%..%'),
               CONSTRAINT check_Phone_Number CHECK(Phone_Number LIKE '+254%' AND LEN(Phone_Number) = 13 AND Phone_Number NOT LIKE '%[^0-9]%'),
               CONSTRAINT check_Status CHECK(Status IN ('Active','Inactive','Pending','Suspended')),
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
               CONSTRAINT client_foreign_key FOREIGN KEY (Client_id) REFERENCES Client(Id) ON DELETE NO ACTION,
               CONSTRAINT personnel_foreign_key FOREIGN KEY (Personnel_id) REFERENCES Personnel(Id) ON DELETE NO ACTION,
               CONSTRAINT check_budget CHECK ( Budget >= 0.00),
               CONSTRAINT check_status CHECK ( Status IN ('Pending','In progress','Completed','On hold','Cancelled')),
               CONSTRAINT Check_date CHECK (End_date > Start_date)
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
               CONSTRAINT personnel_foreign_key FOREIGN KEY (Personnel_id) REFERENCES Personnel(Id) ON DELETE CASCADE,
               CONSTRAINT check_expiry_date CHECK (Expiry_date > GETDATE()),
               CONSTRAINT check_status CHECK (status IN ('Active','Expired','Revoked','Pending'))
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
               Status VARCHAR(20) NOT NULL DEFAULT 'Active',
               CONSTRAINT check_status CHECK (Status IN ('Active', 'In Repair', 'Retired')),
               CONSTRAINT supplier_foreign_key FOREIGN KEY (Supplier_id) REFERENCES Suppliers(Id) ON DELETE NO ACTION,
               CONSTRAINT  check_quantity CHECK (Quantity >= 0),
               CONSTRAINT check_code_format CHECK (
                    Code LIKE 'EQ-[A-Z0-9]%' 
                    AND LEN(Code) >= 7          
                    AND Code NOT LIKE '%[^A-Z0-9-]%'
               ), 
               CONSTRAINT unique_equipment_supplier UNIQUE (Supplier_id, Name)
                              )
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
               CONSTRAINT check_status  CHECK (Status IN ('Available','Not Available')),  
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
              CONSTRAINT check_type CHECK( Type IN ('Personnel Wages','Supplier Payments','Client Payments')),
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
               SELECT 
               c.Id AS ClientID, c.Name AS ClientName, c.Email, c.Phone_Number,
               s.Id AS SupplierID, s.Name AS SupplierName, s.Status AS SupplierStatus,
               p.Id AS ProjectID, p.Name AS ProjectName, p.Budget, p.Status AS ProjectStatus,
               per.Name AS PersonnelName, per.Role AS PersonnelRole,
               fin.Type AS TransactionType, fin.Amount, fin.Transaction_date
               FROM Client c
               LEFT JOIN Projects p ON c.Id = p.Client_id
               LEFT JOIN Personnel per ON p.Personnel_id = per.Id
               LEFT JOIN Financials fin ON c.Id = fin.Client_id
               LEFT JOIN Suppliers s ON fin.Supplier_id = s.Id;
          """
          # client view
          # client should see his name ,email,phone number , project name , project status , project budget

          sql2="""
               CREATE VIEW Client_view AS
               SELECT 
               c.Name AS ClientName, c.Email, c.Phone_Number,
               p.Name AS ProjectName, p.Status AS ProjectStatus, p.Budget,
               p.Start_date, p.End_date
               FROM Client c
               LEFT JOIN Projects p ON c.Id = p.Client_id;
          """

          # personnel view
          # personnel should see his name, his wages his role and sub role, he should also know which project he is working on
          sql3="""
               CREATE VIEW Personnel_view AS
               SELECT 
               per.Name AS PersonnelName, per.Wages, per.Role,
               p.Name AS ProjectName, p.Status AS ProjectStatus
               FROM Personnel per
               LEFT JOIN Projects p ON per.Id = p.Personnel_id;
          """
          
          # finance view
          sql4 = """
               CREATE VIEW Finance_view AS
               SELECT 
               f.Type, f.Amount, f.Transaction_date,
               c.Name AS ClientName,
               s.Name AS SupplierName,
               per.Name AS PersonnelName,
               p.Name AS ProjectName
               FROM Financials f
               LEFT JOIN Client c ON f.Client_id = c.Id
               LEFT JOIN Suppliers s ON f.Supplier_id = s.Id
               LEFT JOIN Personnel per ON f.Personnel_id = per.Id
               LEFT JOIN Projects p ON f.Project_id = p.Id;
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

conn.commit()
conn.close()
    