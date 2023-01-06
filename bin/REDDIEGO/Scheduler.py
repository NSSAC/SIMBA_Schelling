# BEGIN: Copyright 
# Copyright (C) 2020 - 2021 Rector and Visitors of the University of Virginia 
# All rights reserved 
# END: Copyright 

# BEGIN: License 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#   http://www.apache.org/licenses/LICENSE-2.0 
# END: License 

# from REDDIEGO.REDDIEGO import REDDIEGO
from importlib import import_module
import sys, logging
import numbers
from functools import cmp_to_key

def scheduleCompare(A, B):
    if A["tick"] != B["tick"]:
        return A["tick"] - B["tick"]
    
    delta = A["priority"] - B["priority"]
    
    return -1 if delta < 0 else 1 if delta > 0 else 0

class Scheduler:
    
    def __init__(self, REDDIEGO):
        self.REDDIEGO = REDDIEGO
        
        self.schema = {
            "type" : "array",
            "items" : {
                "type" : "object",
                "properties" : {
                    "name" : {"type" : "string"},
                    "class" : {"type" : "string"},
                    "package" : {"type" : "string"},
                    "priority" : { 
                        "anyOf" : [
                            {"type" : "number"},
                            {"enum" : ["-Infinity", "Infinity"]}
                            ]
                        },
                    "startTick" : {"type" : "integer", "default" : 0},
                    "tickIncrement" : {"type" : "number", "minimum": 0, "default" : 0},
                    "endTick" : { 
                        "anyOf" : [
                            {"type" : "integer"},
                            {"enum" : ["Infinity"]}
                            ],
                        "default" : "startTick if tickIncrement is 0, Infinity otherwise"
                        },
                    "moduleData" : {"type" : "object"}
                    },
                "required" : [
                    "name",
                    "class",
                    "priority"
                    ]
                }
            }
        
        self.data = self.REDDIEGO.getConfiguration().loadJsonFile("schedule.json", self.schema)
        
        self.schedule = list()
        
        priorities = set()
        
        # Create a child logger, to the REDDIEGO logger (and writing to the same log file)
        self.logger = logging.getLogger(self.REDDIEGO.__class__.__name__ + '.' + __name__)

        for item in self.data:
            self.__addModule(item)
            
            """ Priorities must be unique """
            if item["priority"] in priorities:
                sys.exit("ERROR: Module '" + item["name"] + "' conflicting priority = '" + str(item["priority"]) + "'.")
                
            priorities.add(item["priority"])
            
        self.currentTick = None
        self.currentTime = None

        return
            
        
    def start(self, startTick, startTime):

        self.logger.debug('start called')

        self.currentTick = startTick
        self.currentTime = startTime
        
        success = True
        
        try:
            for item in self.data:
                success &= item["instance"].start(startTick, startTime)
                
                if not success:
                    break
                
        except:
            success = False
        
        if not success:
            sys.exit("ERROR: Module '" + item["name"] + "' failed to start.")
            
        for item in self.data:
            self.schedule.append({"tick" : item["startTick"], "priority" : item["priority"], "moduleData" : item})

        self.schedule.sort(key=cmp_to_key(scheduleCompare))
         
        return success
        
    def step(self, continueFromTick, endTick, deltaTime):
        self.logger.debug('step called')
        success = True
        startTime = self.currentTime
        startTick = self.currentTick
        
        while self.currentTick < endTick:
            success &= self.__internalStep(deltaTime, self.currentTick < continueFromTick)
            self.currentTick += 1
            self.currentTime = startTime + (self.currentTick - startTick) * deltaTime

        return success
    
    def __internalStep(self, deltaTime, skipExecution):
        self.logger.debug('__internalStep called')

        success = True
        toBeRemoved = list()
        
        for item in self.schedule:
            if item["tick"] != self.currentTick:
                break
            
            moduleData = item["moduleData"]
            
            success &= moduleData["instance"].step(self.currentTick, self.currentTime, 1, deltaTime, skipExecution)
            
            """ Reschedule the item if required otherwise prepare for removal """
            if self.currentTick + moduleData["tickIncrement"] <= moduleData["endTick"] and moduleData["tickIncrement"] > 0:
                item["tick"] += moduleData["tickIncrement"]
            else:
                toBeRemoved.append(item)
            
        """ Remove items which have not been rescheduled """
        for item in toBeRemoved:
            self.schedule.remove(item)
        
        self.schedule.sort(key=cmp_to_key(scheduleCompare))
        
        return success
        
    def end(self):
        self.logger.debug('end called')
        success = True
        
        for item in self.data:
            try:
                success &= item["instance"].end(self.currentTick, self.currentTime)
                
            except:
                success = False
                
            if not success:
                break
        
        if not success:
            sys.exit("ERROR: Module '" + item["name"] + "' failed to end.")
            
        self.schedule = list()
        self.currentTick = None
        self.currentTime = None
        
        return success

    def __addModule(self, module):
        self.logger.debug('__addModule called')
        if not "package" in module:
            module["package"] = None
        
        if not "moduleData" in module:
            module["moduleData"] = None

        if module["package"] == None:
            Imported = import_module(module["class"])
        else:
            Imported = import_module("." + module["class"], module["package"])
            
        Constructor = getattr(Imported, module["class"])
        module["instance"] = Constructor(self.REDDIEGO, module["moduleData"])
        
        if not isinstance(module["priority"], numbers.Real):
            if module["priority"] == "-Infinity":
                module["priority"] = -float("inf")
            elif module["priority"] == "Infinity":
                module["priority"] = float("inf")

        if not "startTick" in module:
            module ["startTick"] = 0

        if module["startTick"] < 0 :
            sys.exit("ERROR: Module '" + module["name"] + "' invalid startTick = '" + str(module["startTick"]) + "'.")
            
        if not "tickIncrement" in module:
            module ["tickIncrement"] = 0
            
        if module["tickIncrement"] < 0:
            sys.exit("ERROR: Module '" + module["name"] + "' invalid tickIncrement = '" + str(module["tickIncrement"]) + "'.")
            
        if not "endTick" in module:
            if module["tickIncrement"] == 0:
                module["endTick"] = module["startTick"]
            else:
                module["endTick"] = float("inf")
        elif not isinstance(module["endTick"], int):
            module["endTick"] = float("inf")
                
        if module["endTick"] < module["startTick"] or (not isinstance(module["endTick"], int) and module["endTick"] != float("inf")):
            sys.exit("ERROR: Module '" + module["name"] + "' invalid endTick = '" + str(module["endTick"]) + "'.")
            
        return True
