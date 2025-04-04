import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Housing Development;"
    "Trusted_Connection=yes;"
    "Encrypt=no"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor() 
print("Connection successful!")

class Database:
    def create_tables(self):
        sql1="""
                CREATE TABLE Client(
                 Client_id VARCHAR(25) PRIMARY KEY,
                 Client_name VARCHAR(50) NOT NULL UNIQUE,
                 Client_email VARCHAR(100) NOT NULL UNIQUE,
                 Client_phone_number VARCHAR(25) NOT NULL,

                );               
             """
        cursor.execute(sql1)

        sql2="""
               CREATE TABLE Suppliers(
               Supplier_id VARCHAR(25) PRIMARY KEY,
               Supplier_name VARCHAR(100) NOT NULL UNIQUE,
               Supplier_email VARCHAR(100) NOT NULL,
               Supplier_phone_number VARCHAR(25) NOT NULL,
               Supplier_status VARCHAR(20) CHECK (Supplier_status IN ('Paid','Unpaid')),
               Remaining_amount DECIMAL(15,2) NOT NULL 
              ); 
            """
        cursor.execute(sql2)
        
        sql3="""
             CREATE TABLE Personnel(
              Personnel_id VARCHAR(25) PRIMARY KEY,
              Personnel_name VARCHAR(50) NOT NULL UNIQUE,
              Personnel_code VARCHAR(50) NOT NULL UNIQUE,
              Personnel_wages DECIMAL(15,2) NOT NULL,
              Personnel_role VARCHAR(50) NOT NULL,
              Personnel_type VARCHAR(50) NOT NULL CHECK(Personnel_type IN ('Professional','Skilled','Unskilled')),
              
             );
              """
        cursor.execute(sql3)

        sql4="""
                 CREATE TABLE Projects(
                 Project_id VARCHAR(25) PRIMARY KEY,
                 Project_name VARCHAR(100) NOT NULL UNIQUE,
                 Project_start_date DATE NOT NULL,
                 Project_end_date DATE NOT NULL,
                 Project_budget DECIMAL(18,2) NOT NULL,
                 Client_id INT,
                 Project_status VARCHAR(50) NOT NULL CHECK(Project_status IN ('In progress','Completed')), 
                 CONSTRAINT client_project_foreign_key FOREIGN KEY (Client_id) REFERENCES Client(Client_id) ON DELETE CASCADE,
                 );
            """
        cursor.execute(sql4)

        sql5="""
              CREATE TABLE Certification(
                Certification_id VARCHAR(25) PRIMARY KEY,
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
                Equipment_id VARCHAR(25) PRIMARY KEY,
                Supplier_id INT NOT NULL,
                Equipment_name VARCHAR(20) NOT NULL,
                Equipment_quantity INT NOT NULL,
                Date_Bought DATE NOT NULL,
                Equipment_status VARCHAR(20) CHECK (Equipment_status IN ('Active', 'In Repair', 'Retired')),
                CONSTRAINT supplier_equipment_foreign_key FOREIGN KEY (Supplier_id) REFERENCES Suppliers(Supplier_id)
              );
            """
        cursor.execute(sql6)
        sql7="""
             CREATE TABLE Materials(
               Material_id VARCHAR(25) PRIMARY KEY,
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
              Transaction_id VARCHAR(25) PRIMARY KEY,
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
     
    def create_roles(self):
        c_sql =     """
                    CREATE LOGIN ovrAdmin WITH PASSWORD = 'SLS_ADMIN@2025';
                    """
        cursor.execute(c_sql)

        c_sql2 =    """
                    CREATE USER ovrAdmin FOR LOGIN ovrAdmin;
                    """
        cursor.execute(c_sql2)

        c_sql3 =    """
                    CREATE ROLE ADMIN_OVR;
                    GRANT CONTROL ON DATABASE::"Housing Development" TO ADMIN_OVR;
                    ALTER ROLE ADMIN_OVR ADD MEMBER ovrAdmin;
                    """
        cursor.execute(c_sql3)

        c_sql4 =    """
                    CREATE ROLE SUPPLY_MANAGER;
                    CREATE ROLE PROJECTS_MANAGER;
                    CREATE ROLE FINANCE_MANAGER;
                    CREATE ROLE HUMAN_RESOURCE_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Equipment TO SUPPLY_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Materials TO SUPPLY_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Suppliers TO SUPPLY_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Client TO PROJECTS_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Projects TO PROJECTS_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Financials TO FINANCE_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Personnel TO HUMAN_RESOURCE_MANAGER;
                    GRANT SELECT, INSERT, UPDATE, DELETE, ALTER ON dbo.Certification TO HUMAN_RESOURCE_MANAGER;
                    """
        
        cursor.execute(c_sql4)

        conn.commit()

    def create_procedures(self):
        sql0 = """
               
               CREATE PROCEDURE GetAllEquipment AS BEGIN SELECT * FROM dbo.Equipment; END;
               CREATE PROCEDURE GetAllMaterials AS BEGIN SELECT * FROM dbo.Materials; END;
               CREATE PROCEDURE GetAllSuppliers AS BEGIN SELECT * FROM dbo.Suppliers; END;
               CREATE PROCEDURE CountAllSuppliers AS BEGIN SELECT COUNT(*) FROM dbo.Suppliers; END;
               CREATE PROCEDURE CountUnpaidSuppliers AS BEGIN SELECT COUNT(*) FROM dbo.Suppliers WHERE Supplier_status = 'Unpaid'; END;
               CREATE PROCEDURE GetUnpaidAmountTotal AS BEGIN SELECT SUM(Remaining_amount) AS total FROM dbo.Suppliers WHERE Supplier_status = 'Unpaid'; END;

               GRANT EXECUTE ON GetAllEquipment TO SUPPLY_MANAGER;
               GRANT EXECUTE ON GetAllMaterials TO SUPPLY_MANAGER;
               GRANT EXECUTE ON GetAllSuppliers TO SUPPLY_MANAGER;
               GRANT EXECUTE ON CountAllSuppliers TO SUPPLY_MANAGER;
               GRANT EXECUTE ON CountUnpaidSuppliers TO SUPPLY_MANAGER;
               GRANT EXECUTE ON GetUnpaidAmountTotal TO SUPPLY_MANAGER;


               CREATE PROCEDURE GetAllProjects AS BEGIN SELECT * FROM dbo.Projects; END;
               CREATE PROCEDURE GetTotalProjects AS BEGIN SELECT COUNT(*) FROM dbo.Projects; END;
               CREATE PROCEDURE GetPostCovidProjects AS BEGIN SELECT * FROM dbo.Projects WHERE Project_start_date > '1/1/2021'; END;
               CREATE PROCEDURE GetUnfinishedProjectsCount AS BEGIN SELECT COUNT(*) FROM dbo.Projects WHERE Project_status = 'In progress'; END;

               GRANT EXECUTE ON GetAllProjects TO PROJECTS_MANAGER;
               GRANT EXECUTE ON GetTotalProjects TO PROJECTS_MANAGER;
               GRANT EXECUTE ON GetPostCovidProjects TO PROJECTS_MANAGER;
               GRANT EXECUTE ON GetUnfinishedProjectsCount TO PROJECTS_MANAGER;
               

               CREATE PROCEDURE GetAllClients AS BEGIN SELECT * FROM dbo.Client; END;
               CREATE PROCEDURE GetTotalClients AS BEGIN SELECT COUNT(*) FROM dbo.Client; END;
               
               GRANT EXECUTE ON GetAllClients TO PROJECTS_MANAGER;
               GRANT EXECUTE ON GetTotalClients TO PROJECTS_MANAGER;
               

               CREATE PROCEDURE GetAllFinancials AS BEGIN SELECT * FROM dbo.Financials; END;
               CREATE PROCEDURE GetTotalFinancials AS BEGIN SELECT COUNT(*) FROM dbo.Financials; END;
               CREATE PROCEDURE GetAllFinancials AS BEGIN SELECT * FROM dbo.Financials; END;


               GRANT EXECUTE ON GetAllFinancials TO FINANCE_MANAGER;


               CREATE PROCEDURE GetAllPersonnel AS BEGIN SELECT * FROM dbo.Personnel; END;
               CREATE PROCEDURE GetAllCerifications AS BEGIN SELECT * FROM dbo.Cerification; END;

               
               GRANT EXECUTE ON GetAllPersonnel TO HUMAN_RESOURCE_MANAGER;
               GRANT EXECUTE ON GetAllCertifications TO HUMAN_RESOURCE_MANAGER;

               
              
               


               """
        
        cursor.execute(sql0)
        conn.commit()


    def delete_existing_data(self):
        sql0 = """
               DROP ROLE IF EXISTS ADMIN_OVR;
               DROP ROLE IF EXISTS SUPPLY_MANAGER;
               DROP ROLE IF EXISTS PROJECTS_MANAGER;
               DROP ROLE IF EXISTS FINANCE_MANAGER;
               DROP ROLE IF EXISTS HUMAN_RESOURCE_MANAGER;
               """
        cursor.execute(sql0)

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

# db_obj=Database()
# db_obj.delete_existing_data()
# print("<------------EXISTING DATA HAS BEEN DROPPED------------->")
# print("<------------CREATING THE TABLES AND ROLES---------->")
# db_obj.create_tables()
# db_obj.create_roles()
# print("<-------------THE TABLES AND ROLES HAVE BEEN CREATED-------------->")

# cursor.close()
# conn.close()
    