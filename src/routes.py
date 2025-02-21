from fastapi import APIRouter
from pydantic import BaseModel


from src.celery_app import process_sitemap, status

router = APIRouter()



class ParseRequest(BaseModel):
    url: str

@router.post("/parse")
async def parse(request: ParseRequest):
    global status
    task = process_sitemap.delay(request.url)
    status["task_id"] = task.id
    return {"status": status["last_run"], "task_id": task.id}

@router.get("/status")
def get_status():
    return status

@router.delete("/delete")
def reset_database():
    status["last_run"] = "None"
    return {"database is deleted"}


