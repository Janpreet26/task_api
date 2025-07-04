#!/bin/bash

echo "Submitting a task..."
RESPONSE=$(curl -s -X POST http://localhost:8000/run/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 20}')

echo "Response: $RESPONSE"

# Extract the task ID
TASK_ID=$(echo $RESPONSE | sed -n 's/.*"task_id": *"\([^"]*\)".*/\1/p')

echo "Waiting 3 seconds..."
sleep 3

echo "Checking status..."
curl http://localhost:8000/task/$TASK_ID/status
echo ""

echo "Pausing task..."
curl -X POST http://localhost:8000/task/$TASK_ID/pause
echo ""

echo "Checking status..."
curl http://localhost:8000/task/$TASK_ID/status
echo ""

echo "Waiting 15 seconds while paused..."
sleep 15

echo "Checking no result..."
curl http://localhost:8000/task/$TASK_ID/result
echo ""

echo "Resuming task..."
curl -X POST http://localhost:8000/task/$TASK_ID/resume
echo ""

echo "Checking status..."
curl http://localhost:8000/task/$TASK_ID/status
echo ""

echo "Waiting 15 seconds for task to finish..."
sleep 15

echo "Getting result..."
curl http://localhost:8000/task/$TASK_ID/result
echo ""
