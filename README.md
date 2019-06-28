# Sample pack to demonstrate concepts

## Example API Calls
```
# 4xx
curl 'https://stackstorm-instance.com/api/v1/webhooks/handle-alerts' \
-k \
 -H 'Content-Type: application/json' \
 -H 'St2-Api-Key: <api-key>' \
 --data-binary '{"type":"4xx","id":"1111111"}'


# AAA
 curl 'https://stackstorm-instance.com/api/v1/webhooks/handle-alerts' \
-k \
 -H 'Content-Type: application/json' \
 -H 'St2-Api-Key: <api-key>' \
 --data-binary '{"type":"AAA","id":"1111111","dc":"foo","app_id":"abc","app_env":"bar"}'


# low_disk_space
 curl 'https://stackstorm-instance.com/api/v1/webhooks/handle-alerts' \
-k \
 -H 'Content-Type: application/json' \
 -H 'St2-Api-Key: <api-key>' \
 --data-binary '{"type":"low_disk_space","id":"1111111","low_disk_entries":[{"hostname":"a","mount":"/var/log"},{"hostname":"b","mount":"/var/log"}]}'


# responding an inquiry
curl 'https://stackstorm-instance.com/api/v1/inquiries/5d1449fb93addb50bf8e5a5f' \
-k \
-X PUT \
 -H 'Content-Type: application/json' \
 -H 'St2-Api-Key: <api-key>' \
 --data-binary '{"id":"5d1449fb93addb50bf8e5a5f","response":{"approved":true,"message":"hello from api"}}'

# responding to an inquiry with a query string api key
 curl 'https://stackstorm-instance.com/api/v1/inquiries/5d1449fb93addb50bf8e5a5f?st2-api-key=<api-key>' \
-k \
-X PUT \
 -H 'Content-Type: application/json' \
 --data-binary '{"id":"5d1449fb93addb50bf8e5a5f","response":{"approved":true,"message":"hello from api"}}'

```