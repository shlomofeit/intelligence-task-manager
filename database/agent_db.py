from db_connection import DBConnection
from pydantic import BaseModel
from enum import Enum


class AgentRunkValidation(str, Enum):
    pass

class AgentValidate(BaseModel):
    name: str
    specialty: str
    is_active: bool
    completed_missions: int
    failed_missions: int
    agent_rank: AgentRunkValidation


class AgentDB:
    DBConnection().connect()

    @classmethod
    def create_agent(data: AgentValidate):
        pass


    @classmethod
    def get_all_agents(cls):
        conn = DBConnection.get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM agents")
            result = cursor.fetchall()
            return result
        finally:
            cursor.close()
        

    @classmethod
    def get_agent_by_id(id):
        pass


    @classmethod
    def update_agent(id, data: AgentValidate):
        pass


    @classmethod
    def deactivate_agent(id):
        pass


    @classmethod
    def increment_completed(id):
        pass


    @classmethod
    def increment_failed(id):
        pass


    @classmethod
    def get_agent_performance(id):
        pass


    @classmethod
    def count_active_agents():
        pass



print(AgentDB().get_all_agents())