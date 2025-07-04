#!/bin/bash

BASE_URL="http://localhost:8000"

declare -a TASK_IDS=()

# Submit 5 tasks (e.g., 'add' tasks)
for i in {1..5}
do
  echo "Submitting task #$i..."
  RESPONSE=$(curl -s -X POST "$BASE_URL/run/add" \
    -H "Content-Type: application/json" \
    -d "{\"a\": $i, \"b\": $((i*2))}")
  
  TASK_ID=$(echo $RESPONSE | sed -n 's/.*"task_id": *"\([^"]*\)".*/\1/p')
  echo "Task ID: $TASK_ID"
  TASK_IDS+=("$TASK_ID")
done

echo ""

echo "All tasks submitted."

echo ""

echo "Cancel the first task..."
curl -X DELETE "$BASE_URL/task/${TASK_IDS[0]}"

echo ""

echo "Waiting 5 seconds before checking status..."
sleep 5

# Check status of all tasks every 5 seconds until all complete
while true; do
  ALL_DONE=true
  echo "Checking task statuses..."

  for TASK_ID in "${TASK_IDS[@]}"
  do
    STATUS=$(curl -s "$BASE_URL/task/$TASK_ID/status" | sed -n 's/.*"status": *"\([^"]*\)".*/\1/p')
    echo "Task $TASK_ID status: $STATUS"

    if [[ "$STATUS" != "completed" && "$STATUS" != "cancelled" && "$STATUS" != "error" ]]; then
      ALL_DONE=false
    fi
  done

  if $ALL_DONE ; then
    echo "All tasks finished!"
    break
  fi

  echo "Waiting 5 seconds to check again..."
  sleep 5
done

echo ""
echo "Fetching results..."

for TASK_ID in "${TASK_IDS[@]}"
do
  RESULT=$(curl -s "$BASE_URL/task/$TASK_ID/result")
  echo "Result for task $TASK_ID: $RESULT"
done
