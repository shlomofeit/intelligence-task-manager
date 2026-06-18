from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from enum import Enum


class RankValidation(Enum):
    pass

class AgentValidation(BaseModel):
    pass


router = APIRouter()


@router.post("")
def creat_new_agent(data: AgentValidation):
    pass


@router.get("")
def get_all_agents_list():
    pass


@router.get("/{id}")
def get_agent_by_id(id: int):
    pass


@router.put("/{id}")
def update_agent(id: int, data: AgentValidation):
    pass


@router.put("/{id}")
def agent_deactive(id: int):
    pass


@router.get("/{id}/performance")
def get_agent_performance(id: int):
    pass