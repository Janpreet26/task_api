Usage
To create a task, send a POST request to /run with a JSON body containing the task details. The response will include a task_id that you can use to pause, resume, check the status, check the result, or cancel the task.

To create a task, you can use the following curl command:

curl -X POST http://localhost:5000/run/add -H "Content-Type: application/json" -d '{"a": 2, "b": 3}'
curl -X POST http://localhost:5000/run/fib -H "Content-Type: application/json" -d '{"n": 10}'
To pause a running task, use:

curl -X POST http://localhost:5000/task/{task_id}/pause
To resume a paused task, use:

curl -X POST http://localhost:5000/task/{task_id}/resume
To check the status of a task, use:

curl -X GET http://localhost:5000/task/{task_id}/status
To check the result of a task, use:

curl -X GET http://localhost:5000/task/{task_id}/result
To cancel a task, use:

