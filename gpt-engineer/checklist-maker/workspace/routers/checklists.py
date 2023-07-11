from fastapi import APIRouter
from ..models import Checklist
from ..services import ChecklistService

router = APIRouter()

@router.get("/checklists")
async def get_checklists(user_id: int):
    return ChecklistService.get_checklists(user_id)

@router.post("/checklists")
async def create_checklist(checklist: Checklist):
    return ChecklistService.create_checklist(checklist)

@router.put("/checklists/{checklist_id}")
async def update_checklist(checklist_id: int, checklist: Checklist):
    return ChecklistService.update_checklist(checklist_id, checklist)

@router.delete("/checklists/{checklist_id}")
async def delete_checklist(checklist_id: int):
    return ChecklistService.delete_checklist(checklist_id)
