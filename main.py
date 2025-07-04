# Entrypoint

from fastapi import FastAPI, HTTPException
from task_manager import TaskManager
from tasks import add, fib
from starlette.responses import FileResponse 

MAX_CONCURRENT_TASKS = 3

app = FastAPI()
manager = TaskManager(MAX_CONCURRENT_TASKS)

TASK_MAP = {
    "add": add,
    "fib": fib
}

@app.get("/")
def read_root():
    return FileResponse('index.html')

@app.post("/run/{task_type}")
async def run_task(task_type: str, params: dict):
    if task_type not in TASK_MAP:
        raise HTTPException(status_code=404, detail="Task type not found")
    task_id = manager.submit_task(TASK_MAP[task_type], params)
    return {"message": f"Task {task_id} started.", "task_id": task_id}

@app.get("/task/{task_id}/status")
def get_status(task_id: str):
    return manager.get_status(task_id)

@app.get("/task/{task_id}/result")
def get_result(task_id: str):
    return manager.get_result(task_id)

@app.post("/task/{task_id}/pause")
def pause_task(task_id: str):
    manager.pause_task(task_id)
    return {"message": f"Task {task_id} paused."}

@app.post("/task/{task_id}/resume")
def resume_task(task_id: str):
    manager.resume_task(task_id)
    return {"message": f"Task {task_id} resumed."}

@app.delete("/task/{task_id}")
def cancel_task(task_id: str):
    manager.cancel_task(task_id)
    return {"message": f"Task {task_id} cancelled."}
