# Sample pack to demonstrate concepts

## Config

### config: payload
Type: object

Example:
```
{"entries":[{"hostname":"foo", "mount":"/var/log"}]}
```

- entries
A list of entries for the sensor.  Each entry should be of the following format:
```
{"hostname":"foo", "mount":"/var/log"}
```

## Actions

### Actions: handle-alerts
This acts as a router to decide which sub-workflow to execute based on an alert type.

![Alert Router](/img/use-cases-alert-router.jpg)

### Actions: handle-alert-4xx
Look up information about the alert in a log store (Splunk, Elasticsearch, Scalyr, etc), and perform an action based on the result.

### Actions: handle-alert-aaa
AAA is designated here as a highly destructive action (such as removing a server, clearing a database, etc), and it should be approved prior to executing the `remediate-aaa` action.

![AAA](/img/use-cases-aaa.jpg)

#### Actions: handle-alert-aaa inquiry: Example API Calls
```
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

### Actions: remediate-aaa
This would perform the actual destructive action.

This workflow demonstrates the use of a Higher-Order Workflow pattern (see `wrap-incident` below).

### Actions: handle-alert-low-disk-space
Follows the naming pattern of `handle-*` and calls a remediate action.

### Actions: remediate-low-disk-space
For a list of given hosts, run a Chef cookbook (or similar integration) to clean the excessive disk data.

![Clear Log Files](/img/use-cases-clear-log-files.jpg)

### Actions: wrap-incident
Example Implementation of a Higher-Order Workflow pattern.  It takes an action and an action's inputs as its own inputs and allows wrapping arbitrary actions with customized logic.

#### Actions: wrap-incident: Problem

Sometimes it is necessary to standardize logic before and/or after a set of actions.

For example, maybe when an action is taken, it needs to be logged as a ticket, and when the action completes, the ticket needs to then be updated with information and status.

One approach with StackStorm is to provide a pack for the incident/ticket system and a couple of actions: one to create a ticket and one to update with information and status. These actions could then be used before and after each action that needs an associated ticket.

![Process Incidents](/img/use-cases-process-incidents.jpg)

> **NOTE:** The ‘remediate’ action calls `create-ticket`, `restart_components`, and `modify-ticket`

There are caveats to this approach.

**Caveat: Developer Oversight**

It becomes possible for pack developers to forget to include pieces such as the following update task.  This is also a good reason for enforcing Code Reviews, but even then, it’s possible things could be missed.

**Caveat: High Maintenance Overhead**

There are currently only two additional actions - one before to create a ticket and one following to update the ticket.  However, it’s possible that there could be additional complexity and steps that need to happen prior to an action, after an action, or both, in which case the ‘convention’ that pack developers would need to follow could require excessive overhead.


#### Actions: wrap-incident: Solution

To remedy these challenges, a Higher-Order Workflow pattern can be used wherein the action and action inputs are parameterized, and the necessary incident creation logic can be abstracted from the actual calling of the action.

This way, pack developers need only know to ‘wrap’ their action within the ‘wrap-incident’ action and can rest assured that the incident creation and update logic is accounted for.

![Process Incidents HOW](/img/use-cases-process-incidents-higher-order-workflow.jpg)

> **NOTE:** The ‘remediate’ action calls only `restart_components` within then `wrap-incident` action

## Rules

### Rules: handle-alerts

Sets up a webhook to send alerts to.  All alerts will be routed into the `handle-alerts` action (the Alert Router workflow described above).

#### Rules: handle-alerts: Example API Calls
```
# 4xx
curl 'https://stackstorm-instance.com/api/v1/webhooks/handle-alerts' \
-k \
 -H 'Content-Type: application/json' \
 -H 'St2-Api-Key: <api-key>' \
 --data-binary '{"type":"4xx","id":"1111111"}'

# 4xx (with mock data - force close)
curl 'https://stackstorm-instance.com/api/v1/webhooks/handle-alerts' \
-k \
 -H 'Content-Type: application/json' \
 -H 'St2-Api-Key: <api-key>' \
 --data-binary '{"type":"4xx","id":"1111111", "mock_splunk_data": "your device is ..."}'

# 4xx (with mock data - set visible)
curl 'https://stackstorm-instance.com/api/v1/webhooks/handle-alerts' \
-k \
 -H 'Content-Type: application/json' \
 -H 'St2-Api-Key: <api-key>' \
 --data-binary '{"type":"4xx","id":"1111111", "mock_splunk_data": "foo"}'


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
```

### Rules: handle-post-sensor-alerts

Receives alerts from a trigger (instead of a webhook) and routes them into the `handle-alerts` action.

## Sensors

### Sensors: host_sensor
Emits a `low_disk_space_sensor_event` trigger containing the `entries` from the config.

> **Note:** This is turned off by default because it creates a lot of noise.  Turn it on only when needed for demonstrating or lower the `poll_interval`.

## Aliases

### Aliases: low-disk-space
Demonstrates connecting ChatOps to an existing action.

```
@bot remediate-low-disk-space
```

> **Note:** This uses the hard-coded default values for hosts. In practice, this would likely be passed as variables.


## File sharing between the debounce alerts sensor and workflows
need to add stanley and root to the same group so they can both mess with files in /packdata
```
sudo mkdir /packdata
sudo groupadd packdata_rw
sudo chgrp -R packdata_rw /packdata
sudo chmod -R 2775 /packdata
sudo usermod -a -G packdata_rw root
sudo usermod -a -G packdata_rw stanley
```