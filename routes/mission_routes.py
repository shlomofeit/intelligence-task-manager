from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from enum import Enum


class StatusValidation(Enum):
    pass

class MissionValidation(BaseModel):
    pass


router = APIRouter()


@router.post("")
def mission_creator(data: MissionValidation):
    pass


@router.get("")
def get_all_missions_list():
    pass


@router.get("/{id}")
def get_mission_by_id(id: int):
    pass


@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(a_id: int, m_id: int):
    pass


@router.put("/{id}/start")
def start_misiion(id: int):
    pass


@router.put("/{id}/complete")
def complete_mission(id: int):
    pass


@router.put("/{id}/fail")
def fail_mission(id: int):
    pass


@router.put("/{id}/cancel")
def cancel_mission(id: int):
    pass