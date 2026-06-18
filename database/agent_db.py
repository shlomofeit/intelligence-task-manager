from database.db_connection import DBConnection


class AgentDB:
    DBConnection().connect()
    conn = DBConnection().get_connection()

    @staticmethod
    def create_agent(data: dict):

        try:
            conn = DBConnection().get_connection()

            query = f"INSERT INTO agents (name, specialty, agent_rank) VALUES (%s, %s, %s)"
            values = [data["name"], data["specialty"], data["agent_runk"]]
            
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()

            new_id = cursor.lastrowid

            return AgentDB().get_agent_by_id(new_id)
        
        # except Exception as e:
        #     print(f"NNN: {e}")
        #     return f"error while creating a new agent: {e}"
        
        finally:
            cursor.close()
            


    @staticmethod
    def get_all_agents():
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents")

            result = cursor.fetchall()

            return result if result else []
        
        finally:
            cursor.close()
        

    @staticmethod
    def get_agent_by_id(id):
        try:
            conn = DBConnection.get_connection()

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents WHERE id = %s", [id])

            result = cursor.fetchone()

            return result if result else None
        
        finally:
            cursor.close()


    @staticmethod
    def update_agent(id, data: dict):
        query_keys = ", ".join(f"{f} = %s" for f in data)
        query_values = list(data.values()) + [id]
        query = f"UPDATE agents SET {query_keys} WHERE id = %s"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor()
            cursor.execute(query, query_values)
            conn.commit()

            result = cursor.rowcount

            if result > 0:
                return "agent update completed successfully"
        
            return "agent not found"
        
        except Exception as e:
            return {"message": f"error while updating the agent: {e}"}
        
        finally:
            cursor.close()


    @staticmethod
    def deactivate_agent(id):
        query = f"UPDATE agents SET is_active = FALSE WHERE id = %s"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor()
            cursor.execute(query, [id])
            conn.commit()

            if cursor.rowcount == 0:
                return "agent not found"
            
            return "the inactive agent update was successful"
        
        except Exception as e:
            return f"error while updating the agent: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def increment_completed(id):
        query = f"UPDATE agents SET completed_missions = completed_missions + 1 WHERE id = %s"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor()
            cursor.execute(query, [id])
            conn.commit()

            if cursor.rowcount == 0:
                return "agent not found"
            
            return "success"
        
        except Exception as e:
            return f"error while updating the agent: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def increment_failed(id):
        query = f"UPDATE agents SET failed_missions = failed_missions + 1 WHERE id = %s"

        try:
            conn = DBConnection().get_connection()

            cursor = conn.cursor()
            cursor.execute(query, [id])
            conn.commit()

            if cursor.rowcount == 0:
                return "agent not found"
            
            return "success"
        
        except Exception as e:
            return f"error while updating the agent: {e}"
        
        finally:
            cursor.close()


    @staticmethod
    def get_agent_performance(id):
        agent = AgentDB.get_agent_by_id(id)

        if not agent:
            return "agent not found"
        
        completed = agent["completed_missions"]
        failed = agent["failed_missions"]
        total = completed + failed
        success_rate = (completed / total) * 100 if total > 0 else 0

        return {
            "completed": completed,
            "failed": failed,
            "total": total,
            "success_rate": success_rate
        }


    @staticmethod
    def count_active_agents():
        try:
            conn = DBConnection.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS COUNT FROM agents WHERE is_active = TRUE")

            result = cursor.fetchall()[0]["COUNT"]

            return result
        
        finally:
            cursor.close()


