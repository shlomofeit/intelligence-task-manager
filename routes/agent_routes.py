from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database.agent_db import AgentDB
from database.db_connection import DBConnection
from pydantic import BaseModel
from enum import Enum


# class RankValidation(Enum):
#     Junior = "Junior"
#     Senior = "Senior"
#     Commander = "Commander"


class AgentValidation(BaseModel):
    name: str | None = None
    specialty: str | None = None
    is_active: bool | None = None
    agent_rank: str | None = None
    


class NewAgentValidation(BaseModel):
    name: str
    specialty: str
    agent_rank: str


router = APIRouter()


@router.post("", status_code=201)
def creat_new_agent(data: NewAgentValidation):
    agent = data.model_dump()
    
    if agent["agent_rank"] not in ["Junior", "Senior", "Commander"]:
        raise HTTPException(400, "agent_rank is not valid")
    
    result = AgentDB.create_agent(agent)
    
    if result:
        return f"Agent created: {result}" 
    
    else:
        HTTPException(500, result)

@router.get("")
def get_all_agents_list():
    result = AgentDB.get_all_agents()

    return result


@router.get("/{id}")
def get_agent_by_id(id: int):
    result = AgentDB.get_agent_by_id(id)

    if not result:
        raise HTTPException(404, "Agent not found")
    return result


@router.put("/{id}/deactivate")
def agent_deactive(a_id: int):
    get_agent_by_id(a_id)

    result = AgentDB.deactivate_agent(a_id)

    return result


@router.get("/{id}/performance")
def get_agent_performance(id: int):
    get_agent_by_id(id)
    
    result = AgentDB.get_agent_performance(id)

    return result



@router.put("/{id}")
def update_agent(id: int, data: AgentValidation):
    agent = data.model_dump(exclude_unset=True)

    if "agent_rank" in agent:
        if agent["agent_rank"] not in ["Junior", "Senior", "Commander"]:
            raise HTTPException(400, "agent_rank is not valid")

    result = AgentDB.update_agent(id, agent)

    return result