# BEGIN: Copyright 
# Copyright (C) 2021 Rector and Visitors of the University of Virginia 
# All rights reserved 
# END: Copyright 

# BEGIN: License 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#   http://www.apache.org/licenses/LICENSE-2.0 
# END: License 

import tempfile
import os
import time
import subprocess
from pathlib import Path

from REDDIEGO.AbstractModule import AbstractModule
from REDDIEGO.REDDIEGO import REDDIEGO
 

class CommandlineModule(AbstractModule):
    
    def _init(self):
        self.schema = {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "Schema for commandline modules.",
            "description": "This schema contains all attributes supported by the commandline module.",
            "type": "object",
            "required": [
                "executable"
            ],
            "properties": {
                "executable": {
                    "type": "string"
                },
                "arguments": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                },
                "environment": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": [
                            "name",
                            "value"
                        ],
                        "properties": {
                            "name": {"type": "string"},
                            "value": {"type": "string"}
                        }
                    }
                }
            }
        }

        self.data = self.REDDIEGO.getConfiguration().loadJsonFile(self.data['config'], self.schema)

        if 'arguments' not in self.data:
            self.data['arguments'] = []

        if 'environment' not in self.data:
            self.data['environment'] = {}

        self.command = []
        self.command.append(self.data['executable'])
        
        for argument in self.data['arguments']:
            self.command.append(argument)

        # Create environment
        self.env = os.environ.copy()

        for item in self.data['environment']:
            self.env[item['name']] = item['value']

        return
        
    def _start(self, startTick, startTime):
        return self._run([
            "--mode", "start",
            "--startTick", str(startTick),
            "--startTime", str(startTime)])

    def _step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
        return self._run([
            "--mode", "step",
            "--lastRunTick", str(lastRunTick),
            "--lastRunTime", str(lastRunTime),
            "--currentTick", str(currentTick),
            "--currentTime", str(currentTime),
            "--targetTick", str(targetTick),
            "--targetTime", str(targetTime)])

    def _end(self, lastRunTick, lastRunTime, endTick, endTime):
        return self._run([
            "--mode", "end",
            "--lastRunTick", str(lastRunTick),
            "--lastRunTime", str(lastRunTime),
            "--endTick", str(endTick),
            "--endTime", str(endTime)])
        
    def _run(self, arguments):
        (fd, statusFile) = tempfile.mkstemp(prefix="status.", dir=os.getcwd(), text=True)
        os.close(fd)
        stamp = os.stat(statusFile).st_mtime

        arguments.append("--status")
        arguments.append(statusFile)

        if not self._execute(arguments):
            success = False
        else:
            success = self._monitor(statusFile, stamp)

        os.remove(statusFile)

        return success
        
    def _execute(self, arguments):
        cmd = self.command + arguments
        """Open a pipe that executes this instances command in.
        """
        self.logger.info('Executing (' + str(cmd) +') in ' + os.getcwd())

        try:
            p = subprocess.Popen(cmd, shell=False, env=self.env,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (self.output, self.errput) = p.communicate(input=None)

        except Exception as e:
            print(e)
            return False

        if p.returncode:
            self.logger.error('Command stdout = ' + self.output.decode())
            self.logger.error('Command sterr = ' + self.errput.decode())
            return False

        self.logger.debug('Command stdout = ' + self.output.decode())
        
        return True


    def _monitor(self, statusFile, stamp):
        while stamp == os.stat(statusFile).st_mtime:
            time.sleep(15)

        # Assure that the writing has completed
        time.sleep(1)
        Status = Path(statusFile).open().read().strip().lower()

        return Status == "success"

        
