# Task API

## Setup
1. Download repo
2. Install requirements
   ``` pip install -r requirements.txt ```
3. Run application
   ``` uvicorn main:app --reload ```
4. Go to localhost to see further info, testing, and UI
   http://127.0.0.1:8000

## Implementation
- TaskManager class
  - limits concurrency via ThreadPoolExecutor
  - if tasks exceed max (3) they are queued (not rejected)
  - tracks tasks in dictionary using {task_id} as key
  - implements API to submit, pause, resume, cancel, check status, check result
- TaskState class to track each task's state and behavior
  - function and args, task metadata
  - uses Condition lock to pause and resume tasks
- ```tasks.py``` dummy tasks
  - simulates long-running tasks using ```sleep```
  - periodically checks ```paused``` and ```cancelled``` flags
  - returns result on completion
- ``` main.py ``` API layer
  - FastAPI for HTTP endpoints
  - /run/{taskType} to start a task
  - /task/{id}/status to get current state
  - /task/{id}/result to fetch result (if completed)
  - /task/{id}/pause|resume|cancel for lifecycle control   


## Usage
To create a task, send a POST request to /run with a JSON body containing the task details. The response will include a task_id that you can use to pause, resume, check the status, check the result, or cancel the task.

To create a task, you can use the following curl command:

```curl -X POST http://127.0.0.1:8000/run/add -H "Content-Type: application/json" -d '{"a": 2, "b": 3}'``` \
```curl -X POST http://127.0.0.1:8000/run/fib -H "Content-Type: application/json" -d '{"n": 10}'```

To pause a running task, use: ```
curl -X POST http://127.0.0.1:8000/task/{task_id}/pause```

To resume a paused task, use: ```
curl -X POST http://127.0.0.1:8000/task/{task_id}/resume```

To check the status of a task, use: ```
curl -X GET http://127.0.0.1:8000/task/{task_id}/status```

To check the result of a task, use: ```
curl -X GET http://127.0.0.1:8000/task/{task_id}/result ```

To cancel a task, use: ```
curl -X DELETE http://127.0.0.1:8000/task/{task_id}```

## Testing
You can test the API using the provided scripts.

test_multi_task.sh script will create multiple tasks, check their status, results, and cancel one of them.

Run the script with: ```bash test_multi_task.sh```

test_single_task.sh script will create, pause, resume, and check the status and result of a task.

Run the script with: ```bash test_single_task.sh```

Make sure the API server is running before executing the script.

