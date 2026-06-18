from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from database.mission_db import MissionDB
from database.agent_db import AgentDB
from pydantic import BaseModel
from enum import Enum


router = APIRouter()


@router.get("/summary")
def get_summary():
    result = {
        "active_agents_count": AgentDB.count_active_agents(),
        "total_missions": MissionDB.count_all_missions(),
        "open_missions": MissionDB.count_open_missions(),
        "completed_missions": MissionDB.count_by_status("COMPLETED"),
        "failed_missions": MissionDB.count_by_status("FAILED"),
        "critical_missions": MissionDB.count_critical_missions()
    }

    return result


@router.get("/missions-by-status")
def get_missions_by_status():
    result = {
        "open": MissionDB.count_by_status("ASSIGNED"),
        "in_progress": MissionDB.count_by_status("IN_PROGRESS"),
        "completed": MissionDB.count_by_status("COMPLETED"),
        "failed": MissionDB.count_by_status("FAILED"),
        "canceled": MissionDB.count_by_status("CANCELLED")
    }

    return result


@router.get("/top-agent")
def get_top_agent():
    result = MissionDB.get_top_agent()

    if not result:
        raise HTTPException(404, "no agents found")

    return result