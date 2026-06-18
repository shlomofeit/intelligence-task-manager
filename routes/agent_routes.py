from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database.agent_db import AgentDB
from database.db_connection import DBConnection
from pydantic import BaseModel
from enum import Enum


class RankValidation(Enum):
    Junior = "Junior",
    Senior = "Senior",
    Commander = "Commander"


class AgentValidation(BaseModel):
    name: str | None = None
    specialty: str | None = None
    is_active: bool | None = None
    agent_rank: RankValidation | None = None


class NewAgentValidation(BaseModel):
    name: str
    specialty: str
    agent_rank: RankValidation


router = APIRouter()


@router.post("", status_code=201)
def creat_new_agent(data: NewAgentValidation):
    # conn = DBConnection().get_connection()
    agent = data.model_dump()

    if data["agent_rank"] not in ["Junior", "Senior", "Commander"]:
        raise HTTPException(400, f"{agent["agent_rank"]} is invalid value")
    
    result = AgentDB.create_agent(data)
    # conn.close()
    
    if isinstance(result, dict):
        return result #"Agent created"
    
    else:
        HTTPException(500, result)

@router.get("")
def get_all_agents_list():
    result = AgentDB.get_all_agents()

    return result


@router.get("/{id}")
def get_agent_by_id(id: int):
    result = AgentDB.get_agent_by_id(id)

    return result


@router.put("/{id}")
def update_agent(id: int, data: AgentValidation):
    agent = data.model_dump(exclude_unset=True)

    result = AgentDB.update_agent(id, agent)

    return result


@router.put("/{id}")
def agent_deactive(id: int):
    result = AgentDB.deactivate_agent(id)

    return result


@router.get("/{id}/performance")
def get_agent_performance(id: int):
    result = AgentDB.get_agent_performance(id)

    return result