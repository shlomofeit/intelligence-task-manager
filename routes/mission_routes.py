from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from enum import Enum


class StatusValidation(Enum):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class MissionValidation(BaseModel):
    title: str
    description: str
    location: str
    difficulty: int
    importance: int
    status: StatusValidation | None = None


router = APIRouter()


@router.post("")
def mission_creator(data: MissionValidation):
    mission = data.model_dump()
    mission["status"] = "NEW"

    result = MissionDB.create_mission(mission)

    return result

@router.get("")
def get_all_missions_list():
    result = MissionDB.get_all_missions()

    return result


@router.get("/{id}")
def get_mission_by_id(id: int):
    result = MissionDB.get_mission_by_id(id)

    if not result:
        raise HTTPException(404, "mission not found")

    return result

@router.put("/{id}/assign/{agent_id}")
def assign_mission_to_agent(id: int, agent_id: int):
    agent = AgentDB.get_agent_by_id(agent_id)
    if not agent:
        raise HTTPException(404, "agent not found")
    
    if not agent["is_active"]:
        raise HTTPException(400, "It is not possible to attach a mission to an inactive agent.") # role 4
    

    mission = MissionDB.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404, "mission not found")
    
    if mission["status"] != "NEW":
        raise HTTPException(400, "Cannot assign a task that is not in NEW status") # role 7
    

    open_missions = MissionDB.get_open_missions_by_agent(agent_id)
    if len(open_missions) > 2:
        raise HTTPException(400, "you cannot have more than 3 tasks per agent") # role 5
    
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        raise HTTPException(400, "Only an Commander agent can accept a CRITICAL mission") # role 6
    
    result = MissionDB.assign_mission(id, agent_id)

    return result


@router.put("/{id}/start", status_code=201)
def start_misiion(id: int):
    get_mission_by_id(id)
    
    try:
        MissionDB.update_mission_status(id, "IN_PROGRESS")

    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{id}/complete")
def complete_mission(id: int):
    mission = get_mission_by_id(id)
    
    try:
        MissionDB.update_mission_status(id, "COMPLETED")
        AgentDB.increment_completed(mission["assigned_agent_id"])

    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{id}/fail")
def fail_mission(id: int):
    mission = get_mission_by_id(id)
    
    try:
        MissionDB.update_mission_status(id, "FAILED")
        AgentDB.increment_failed(mission["assigned_agent_id"])

    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{id}/cancel")
def cancel_mission(id: int):
    get_mission_by_id(id)
    
    try:
        MissionDB.update_mission_status(id, "CANCELLED")

    except ValueError as e:
        raise HTTPException(400, str(e))