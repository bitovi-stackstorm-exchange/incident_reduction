from st2reactor.sensor.base import PollingSensor
import json
import os
import time

class ProcessDebounceAlerts(PollingSensor):
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
        super(ProcessDebounceAlerts, self).__init__(
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



        debounce_alerts_root_file_path = self._config.get('debounce_alerts_root_file_path')
        trigger_name = "incident_reduction.processed_debounced_alerts"
        # get a list of files in debounce_alerts_root_file_path
        #  - that aren't named catchall
        #  - that don't have a suffix of ".processing" or ".failed"
        #  - that are older than 5 minutes
        # for each of the files in debounce_alerts_root_file_path
        #  first, "claim" the file by renaming it with a suffix of ".processing"
        #  then, read the file contents
        #  each line is a json object that needs to be read into a python object
        #  send a trigger which contains a list of the python objects
        #  finally, delete the file
        #  if any of the above steps fail, rename the file to ".failed" and log the error
        

        # read the directory debounce_alerts_root_file_path
        #  - that aren't named catchall
        #  - that don't have a suffix of ".processing" or ".failed"
        #  - that are older than 5 minutes
        debounce_alerts_files = os.listdir(debounce_alerts_root_file_path)
        self.logger.debug('debounce_alerts_files: ' + json.dumps(debounce_alerts_files))
        for debounce_alerts_file in debounce_alerts_files:
            entries = []
            full_debounce_alerts_file = f"{debounce_alerts_root_file_path}/{debounce_alerts_file}"
            self.logger.info(f"process_debounce_alerts.py - processing file: {debounce_alerts_file}")
            
            # if debounce_alerts_file is named catchall, skip it
            if(debounce_alerts_file == "catchall"):
                continue

            # if debounce_alerts_file has a suffix of ".processing" or ".failed", skip it
            if(debounce_alerts_file.endswith(".processing") or debounce_alerts_file.endswith(".failed")):
                continue

            # if debounce_alerts_file is older than 5 minutes, skip it
            file_last_modified = os.path.getmtime(full_debounce_alerts_file)
            file_age_in_seconds = time.time() - file_last_modified
            if(file_age_in_seconds > 300):
                continue
        
        
            # "claim" the file by renaming it with a suffix of ".processing"
            full_debounce_alerts_file_processing = f"{full_debounce_alerts_file}.processing"
            os.rename(full_debounce_alerts_file, full_debounce_alerts_file_processing)

            # read the file contents
            with open(full_debounce_alerts_file_processing) as f:
                debounce_alerts_file_contents = f.readlines()
                self.logger.debug('debounce_alerts_file_contents: ' + json.dumps(debounce_alerts_file_contents))
                for line in debounce_alerts_file_contents:
                    entries.append(json.loads(line))

            # send a trigger which contains a list of the python objects
            self._sensor_service.dispatch(trigger=trigger_name, payload={
                "metadata": {
                    "unique_code": debounce_alerts_file,
                    "processed_file": debounce_alerts_file,
                    "processed_file_full_path": full_debounce_alerts_file
                },
                "entries": entries
            })

            # finally, delete the file
            # os.remove(full_debounce_alerts_file_processing)

            






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
