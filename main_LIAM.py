from flask import Flask, g, session, redirect, url_for, request, render_template
import pyodbc
import secrets
from functools import wraps

app = Flask(__name__,  static_folder="assets")
app.secret_key = secrets.token_hex(16)  # Required for session
 

# Database connection decorator
def get_db_connection():
    if 'db_conn' not in g:
        g.db_conn = pyodbc.connect(
                    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                    "SERVER=localhost;"
                    "DATABASE=Housing Development;"
                    f"UID={session['db_creds']['username']};"
                    f"PWD={session['db_creds']['password']};"
                    "Encrypt=no;"
                    "Trusted_Connection=yes;"
                    "extra_params=MARS_Connection=Yes;"
                )
    return g.db_conn

#check if user has permissions
def check_user_role(connection, username, role_name):
    cursor = connection.cursor()

    sql0 =  f"""
            SELECT 1
            FROM sys.database_role_members AS DRM
            JOIN sys.database_principals AS DP1 ON DRM.role_principal_id = DP1.principal_id
            JOIN sys.database_principals AS DP2 ON DRM.member_principal_id = DP2.principal_id
            WHERE DP1.name = '{role_name}' AND DP2.name = '{username}';
            """  
    # cursor.execute(sql0).fetchone()
    if(cursor.execute(sql0).fetchone()):
        return True


@app.teardown_appcontext
def close_db_connection(e=None):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()
 

@app.route("/")
def inv_dir():
    return redirect(url_for("welcome_login"))

@app.route("/welcome", methods=['GET', 'POST'])
def welcome_login():
    error = None
    if request.method == "POST":
        # handle server login and save the login info globally in the project
        session['db_creds'] = {
            'username': request.form['username'],
            'password': request.form['password']
        }
       # Test connection
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            print("love")
            #test if connected
            cursor.execute("SELECT 1")
            cursor.close()
            print("love sosa")
            username = session["db_creds"]["username"]
            if check_user_role(conn, username, "ADMIN_OVR"):
                session["user_role"] = "ADMIN_OVR"
                return redirect(url_for("admin_dashboard"))
        except pyodbc.Error as e:
            session.pop('db_creds', None)
            return render_template('login.html', error=str(e))
 
        return redirect(url_for('dashboard'))
    
    return render_template("login.html", error=error)

@app.route("/set/cookies/<username>&<role>&<passw_>")
def set_cookies(username, role, passw_):
    resp = redirect(url_for('admin_dashboard'))
    resp.set_cookie("user", username)
    resp.set_cookie("pass_", passw_)
    resp.set_cookie("role", role)
    return resp
    

def fetch_admin_data():
    # execute a procedure that returns all the data
    sql_q = """
            SELECT * FROM dbo.Client;
            SELECT COUNT(*) FROM dbo.Client;
            """
    conn = get_db_connection()
    cursor = conn.cursor()

    s = cursor.execute(sql_q).fetchall()
    print(s)


@app.route("/admin/dashboard")
def admin_dashboard():
    if(request.cookies.get("role") != "ADMIN_OVR"):
        return redirect(url_for("welcome_login"))
    # utility function to fetch all the data
    #print(settings.user_role)
    fetch_admin_data()
    return render_template("admin_dashboard.html", user=request.cookies.get("user"))

# Logout route
@app.route('/logout')
def logout():
    session.pop('db_creds', None)
    if 'db_conn' in g:
        g.db_conn.close()
        g.pop('db_conn')
    return redirect(url_for('login'))


app.run(debug=True)