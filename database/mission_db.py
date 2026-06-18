from database.db_connection import DBConnection
from database.agent_db import AgentDB
from utils.mission_utils import risk_calculator


class MissionDB:
    DBConnection().connect()

    @staticmethod
    def create_mission(data: dict):

        try:
            conn = DBConnection().get_connection()

            query = f"INSERT INTO missions (title, description, location, difficulty, importance, status, risk_level) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            risk = risk_calculator(data["difficulty"], data["importance"])
            values = [data["title"], data["description"], data["location"], data["difficulty"], data["importance"], data["status"], risk]

            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            new_id = cursor.lastrowid

            return MissionDB.get_mission_by_id(new_id)
        
        except Exception as e:
            return {"message": f"error while creating a new mission: {e}"}
        
        finally:
            cursor.close()
            


    @staticmethod
    def get_all_missions():
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions")

            result = cursor.fetchall()

            return result if result else []
        
        finally:
            cursor.close()
        

    @staticmethod
    def get_mission_by_id(id):
        try:
            conn = DBConnection.get_connection()

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM missions WHERE id = %s", [id])

            result = cursor.fetchone()

            return result if result else None
        
        finally:
            cursor.close()


    @staticmethod
    def assign_mission(m_id, a_id):

        query_values = [a_id, m_id]
        query = f"UPDATE missions SET assigned_agent_id = %s WHERE id = %s"
        
        conn = DBConnection().get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, query_values)
            conn.commit()

            MissionDB.update_mission_status(m_id, "ASSIGNED")

            return "success"
        
        except Exception as e:
            return {"message": f"error while updating the mission: {e}"}
                
        finally:
            cursor.close()
    

    @staticmethod
    def update_mission_status(id, status):
        mission = MissionDB.get_mission_by_id(id)
        
        old_status = mission["status"]

        if status == "IN_PROGRESS" and old_status != "ASSIGNED":
            raise ValueError("Mission can start only with ASSIGNED status") # role 8
        
        if status in ["FAILED", "COMPLETED"] and old_status != "IN_PROGRESS":
            raise ValueError("Only mission IN_PROGRESS can change the status to failed or completed") # role 9
        
        if status == "CANCELLED" and old_status not in ["NEW", "ASSIGNED"]:
            raise ValueError("A mission can only be canceled in NEW or ASSIGNED status")
        
        query = f"UPDATE missions SET status = %s WHERE id = %s"

        conn = DBConnection().get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(query, [status, id])
            conn.commit()
            
            return "success"
        
        except Exception as e:
            return f"error while updating the mission: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def get_open_missions_by_agent(id):
        query = f"SELECT * FROM missions WHERE assigned_agent_id = %s AND (status = 'ASSIGNED' OR status = 'IN_PROGRESS')"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor()
            cursor.execute(query, [id])

            result = cursor.fetchall()
            
            return result if result else []
        
        except Exception as e:
            return f"error while updating the agent: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def count_all_missions():
        query = f"SELECT COUNT(*) AS COUNT FROM missions"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            
            return cursor.fetchall()[0]["COUNT"]
        
        except Exception as e:
            return f"error while counting missions: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def count_by_status(status):
        query = f"SELECT COUNT(*) AS COUNT FROM missions WHERE status = %s"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, [status])
            
            return cursor.fetchall()[0]["COUNT"]
        
        except Exception as e:
            return f"error while counting missions: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def count_open_missions():
        query = f"SELECT COUNT(*) AS COUNT FROM missions WHERE status != 'COMPLETED' AND status != 'FAILED' AND status != 'CANCELLED'"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            
            return cursor.fetchall()[0]["COUNT"]
        
        except Exception as e:
            return f"error while counting missions: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def count_critical_missions():
        query = f"SELECT COUNT(*) AS COUNT FROM missions WHERE risk_level = 'CRITICAL'"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            
            return cursor.fetchall()[0]["COUNT"]
        
        except Exception as e:
            return f"error while counting missions: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def get_top_agent():
        query = f"SELECT * FROM agents WHERE completed_missions = (SELECT MAX(completed_missions) FROM agents)"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            
            result = cursor.fetchone()
            return result if result else None
        
        except Exception as e:
            return f"error while counting missions: {e}"
        
        finally:
            cursor.close()