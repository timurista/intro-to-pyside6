from fastapi import APIRouter
from .. import crud, schemas

router = APIRouter()

@router.get("/")
async def get_checklists():
    return crud.get_checklists()

@router.get("/{checklist_id}")
async def get_checklist(checklist_id: int):
    return crud.get_checklist(checklist_id)

@router.post("/")
async def create_checklist(checklist: schemas.ChecklistCreate):
    return crud.create_checklist(checklist)

@router.put("/{checklist_id}")
async def update_checklist(checklist_id: int, checklist: schemas.ChecklistUpdate):
    return crud.update_checklist(checklist_id, checklist)

@router.delete("/{checklist_id}")
async def delete_checklist(checklist_id: int):
    return crud.delete_checklist(checklist_id)
