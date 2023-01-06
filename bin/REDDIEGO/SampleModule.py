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

from REDDIEGO.AbstractModule import AbstractModule
from REDDIEGO.REDDIEGO import REDDIEGO
 

class SampleModule(AbstractModule):
    
    def _init(self):
        self.schema = {}
        
        self.data = self.REDDIEGO.getConfiguration().loadJsonFile("SampleModule/config.json", self.schema)
        return
        
    def _start(self, startTick, startTime):
        # Implement startup procedure, this is the first call to the module
        return True
        
    def _step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
        # Implement simulation step, this is called for every tick
        return True
        
    def _end(self, lastRunTick, lastRunTime, endTick, endTime):
        # Implement shutdown procedure, this is the last call to the module
        return True
        