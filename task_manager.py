# Task control logic

import uuid
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class TaskState:
    def __init__(self, func, args):
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args
        self.status = "queued"
        self.result = None
        self.lock = threading.Condition()
        self.paused = False
        self.cancelled = False
        self.thread = None

    def run(self):
        with self.lock:
            if self.cancelled:
                self.status = "cancelled"
                return
            self.status = "running"
        try:
            self.result = self.func(self.args, self)
            with self.lock:
                if not self.cancelled:
                    self.status = "completed"
        except Exception as e:
            self.status = f"error: {str(e)}"

class TaskManager:
    def __init__(self, max_concurrent_tasks=3):
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
        self.tasks = {}
        self.lock = threading.Lock()

    def submit_task(self, func, args):
        task = TaskState(func, args)
        self.tasks[task.id] = task
        future = self.executor.submit(task.run)
        task.thread = future
        return task.id

    def get_status(self, task_id):
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        return {"task_id": task.id, "status": task.status}

    def get_result(self, task_id):
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}
        if task.status != "completed":
            return {"error": f"Task not completed. Current status: {task.status}"}
        return {"result": task.result}

    def pause_task(self, task_id):
        task = self.tasks.get(task_id)
        if task and task.status == "running":
            with task.lock:
                task.paused = True
                task.status = "paused"
                task.lock.notify_all()

    def resume_task(self, task_id):
        task = self.tasks.get(task_id)
        if task and task.paused:
            with task.lock:
                task.paused = False
                task.status = "running"
                task.lock.notify_all()

    def cancel_task(self, task_id):
        task = self.tasks.get(task_id)
        if task:
            with task.lock:
                task.status = "cancelled"
                task.cancelled = True
                task.lock.notify_all()
