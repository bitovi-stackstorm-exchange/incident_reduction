from st2reactor.sensor.base import PollingSensor
import json

class HostSensor(PollingSensor):
    """
    * self.sensor_service
        - provides utilities like
            - get_logger() - returns logger instance specific to this sensor.
            - dispatch() for dispatching triggers into the system.
    * self._config
        - contains parsed configuration that was specified as
          config.yaml in the pack.
    """

    def __init__(self, sensor_service, config, poll_interval=20):
        super(HostSensor, self).__init__(
            sensor_service = sensor_service,
            config = config,
            poll_interval = poll_interval
        )
        self.logger = None

    def setup(self):
        # Setup stuff goes here. For example, you might establish connections
        # to external system once and reuse it. This is called only once by the system.
        self.logger = self.sensor_service.get_logger(name=self.__class__.__name__)

    def poll(self):
        # This is where the crux of the sensor work goes.
        # This is called once by the system.
        # (If you want to sleep for regular intervals and keep
        # interacting with your external system, you'd inherit from PollingSensor.)
        # For example, let's consider a simple flask app. You'd run the flask app here.
        # You can dispatch triggers using sensor_service like so:
        # self.sensor_service(trigger, payload, trace_tag)
        #   # You can refer to the trigger as dict
        #   # { "name": ${trigger_name}, "pack": ${trigger_pack} }
        #   # or just simply by reference as string.
        #   # i.e. dispatch(${trigger_pack}.${trigger_name}, payload)
        #   # E.g.: dispatch('examples.foo_sensor', {'k1': 'stuff', 'k2': 'foo'})
        #   # trace_tag is a tag you would like to associate with the dispatched TriggerInstance
        #   # Typically the trace_tag is unique and a reference to an external event.
        payload_in = self._config.get('payload', { "entries": []})
        self.logger.debug('hosts: ' + json.dumps(payload_in))
        hosts = payload_in["entries"]

        if(len(hosts)):
            trigger = "incident_reduction.low_disk_space_sensor_event"
            self._sensor_service.dispatch(trigger=trigger, payload={
                "type":"low_disk_space",
                "id":"1111111",
                "low_disk_entries": hosts
            })
        else:
            self.logger.debug('No host entries found.')
        pass

    def cleanup(self):
        # This is called when the st2 system goes down. You can perform cleanup operations like
        # closing the connections to external system here.
        pass

    def add_trigger(self, trigger):
        # This method is called when trigger is created
        pass

    def update_trigger(self, trigger):
        # This method is called when trigger is updated
        pass

    def remove_trigger(self, trigger):
        # This method is called when trigger is deleted
        pass
