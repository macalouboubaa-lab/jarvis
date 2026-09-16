from fastapi import APIRouter
from database import supabase

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("")
async def list_jobs():
    res = supabase.table("job_applications").select("*").execute()
    return res.data
