from fastapi import APIRouter, Depends
from database import supabase
from services.auth import AuthenticatedUser, get_current_user

router = APIRouter(prefix="/api/jobs", tags=["Jobs"])

@router.get("")
async def list_jobs(
    current_user: AuthenticatedUser = Depends(get_current_user),
):
    res = supabase.table("job_applications").select("*").eq(
        "user_id", current_user.id
    ).execute()
    return res.data
