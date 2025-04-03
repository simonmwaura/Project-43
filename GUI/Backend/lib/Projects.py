from lib.config import conn
class Projects:
    # create Projects
    @classmethod
    def create_projects(cls, Project_name, Project_start_date,Project_end_date,Project_budget,Client_id,Project_status):
        cursor=conn.cursor()
        sql="""
             INSERT INTO Projects(Project_name,Project_start_date,Project_end_date,Project_budget,Client_id,Project_status)
             OUTPUT INSERTED.Project_id
             VALUES(?,?,?,?,?,?)
            """
        cursor.execute(sql,( Project_name,Project_start_date,Project_end_date,Project_budget,Client_id,Project_status))
        projects_id = cursor.fetchone()[0]
        conn.commit()
        return projects_id
        cursor.close()
        


    # fetch project by project id
    @classmethod
    def fetch_single_project_id(cls,Project_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Projects WHERE Projects_id = ?  
            """
        cursor.execute(sql ,(Project_id, ))
        return cursor.fetchone()
        cursor.close()
         


    # fetch projects by client id
    @classmethod
    def fetch_projects_by_client_id(cls,Client_id):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Projects WHERE Client_id=?
            """
        cursor.execute(sql, (Client_id, ))
        return cursor.fetchone()
        cursor.close()


    # fetch all the projects
    @classmethod
    def fetch_all_projects(cls):
        cursor = conn.cursor()
        sql="""
            SELECT * FROM Projects
            """
        cursor.execute(sql)
        return cursor.fetchall()
        cursor.close()


    # update projects
    @classmethod
    def update_projects(cls,  Project_id,  Project_name, Project_start_date, Project_end_date, Project_budget, Client_id,Project_status):
        cursor=conn.cursor()
        sql="""
            UPDATE Projects SET Project_name = ?, Project_start_date=?, Project_end_date=?, Project_budget=?, Client_id=?,Project_status=? WHERE Project_id=?
            """
        cursor.execute(sql, (Project_name, Project_start_date, Project_end_date, Project_budget, Client_id,Project_status,Project_id))
        conn.commit()
        cursor.close()
        return Project_id
    
    # delete projects
    @classmethod
    def delete_projects(cls,Projects_id):
        cursor = conn.cursor()
        sql="""
            DELETE FROM Projects WHERE Project_id=?
            """
        cursor.execute(sql ,(Projects_id,))
        conn.commit()
        return Projects_id
        cursor.close()

    # count projects by project_id
    @classmethod
    def count_projects_by_project_id(cls):
        cursor=conn.cursor()
        sql="""
            SELECT COUNT(*) FROM Projects
            """
        cursor.execute(sql)
        return cursor.fetchone()
        cursor.close()

    # count projects by client id
    @classmethod
    def count_projects_by_client_id(cls,Client_id):
       cursor=conn.cursor()
       sql="""
              SELECT COUNT(*) FROM Projects WHERE Client_id=?
           """
       cursor.execute(sql,(Client_id))
       return cursor.fetchone()
       cursor.close()