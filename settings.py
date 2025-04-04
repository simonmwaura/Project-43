import pyodbc

conn = None
cursor = None
user_role = None

def connect_db(username, password):

    connection_string = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=localhost;"
        "DATABASE=Housing Development;"
        f"UID={username};"
        f"PWD={password};"
        "Trusted_Connection=yes;"
        "Encrypt=no"
    )
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        global user_role
        if(conn != None):
            sql0 =  f"""
                SELECT DP1.name AS RoleName, DP2.name AS UserName
                FROM sys.database_role_members AS DRM
                JOIN sys.database_principals AS DP1 ON DRM.role_principal_id = DP1.principal_id
                JOIN sys.database_principals AS DP2 ON DRM.member_principal_id = DP2.principal_id
                WHERE DP2.name = '{username}';

                """ 
            cursor.execute(sql0)

            rp=cursor.fetchall()
            user_role = rp[0][0]
            return "Login Successful!"
        else:
            return "Login Failed!"
    except Exception as e:
        print(e)
        return e
    #print("Connection successful!")
