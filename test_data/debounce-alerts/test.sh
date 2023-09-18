#!/bin/bash

STACKSTORM_URL="https://vm-single.stackstorm.bitovidevops.com"
WEBHOOK_NAME="handle-alerts-debounce"
FULL_WEBHOOK_PATH="${STACKSTORM_URL}/api/v1/webhooks/${WEBHOOK_NAME}"

# read data from test_data/debounce-alerts/1.json
test_data_path="test_data/debounce-alerts/1.json"
test_data=$(cat ${test_data_path})

# the json file has newlines, so we need to remove them
test_data=$(echo ${test_data} | tr -d '\n')


# number of times to make the request
num_requests=10

# make the request num_requests times
while [ $num_requests -gt 0 ]; do
  echo "making request ${num_requests}"
  curl "${FULL_WEBHOOK_PATH}" \
  -k \
   -H 'Content-Type: application/json' \
   -H "St2-Api-Key: ${ST2_API_KEY}" \
   --data-binary "${test_data}"
  num_requests=$((num_requests-1))
done