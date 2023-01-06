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

from abc import ABCMeta, abstractmethod
import logging

class AbstractModule():
    __metaclass__ = ABCMeta
    
    def __init__(self, REDDIEGO, data):
        self.REDDIEGO = REDDIEGO
        self.data = data
        self.__lastRunTick = None
        self.__lastRunTime = None

        # Create a child logger, to the REDDIEGO logger (writing to the same log file)
        self.logger = logging.getLogger(self.REDDIEGO.__class__.__name__ + '.' + __name__)
        
        self._init()
    
    @abstractmethod   
    def _init(self):
        self.logger.debug(__name__ + '._init called')
        return False

    def start(self, startTick, startTime):
        self.logger.debug(__name__ + '.start called')

        self.__lastRunTick = startTick
        self.__lastRunTime = startTime
        
        return self._start(startTick, startTime)
        
    @abstractmethod   
    def _start(self, startTick, startTime):
        self.logger.debug(__name__ + '._start called')
        return False
        
    def step(self, currentTick, currentTime, deltaTick, deltaTime, skipExecution):
        self.logger.debug(__name__ + '.step called')
        success = True
        
        if not skipExecution:
            success = self._step(self.__lastRunTick, self.__lastRunTime, currentTick, currentTime, currentTick + deltaTick, currentTime + deltaTime)
        
        self.__lastRunTick = currentTick
        self.__lastRunTime = currentTime
        
        return success 

    @abstractmethod   
    def _step(self, lastRunTick, lastRunTime, currentTick, currentTime, targetTick, targetTime):
        self.logger.debug(__name__ + '._step called')
        return False
        
    def end(self, endTick, endTime):
        self.logger.debug(__name__ + '.end called')
        
        success = self._end(self.__lastRunTick, self.__lastRunTime, endTick, endTime)
        
        self.__lastRunTick = None
        self.__lastRunTime = None
        
        return success 

    @abstractmethod   
    def _end(self, lastRunTick, lastRunTime, endTick, endTime):
        self.logger.debug(__name__ + '._end called')
        return False
