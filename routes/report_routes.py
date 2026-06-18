from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from enum import Enum


router = APIRouter()


@router.get("/summary")
def get_summary():
    pass


@router.get("/missions-by-status ")
def get_missions_by_status():
    pass


@router.get("/top-agent")
def get_top_agent():
    pass