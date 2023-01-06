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

import sys
from REDDIEGO import Configuration
# from REDDIEGO import Database
from REDDIEGO import Scheduler
from numpy import inf
import os, logging
from datetime import datetime

class REDDIEGO:
    def __init__(self, configurationDirectory):
        self.Configuration = Configuration.Configuration(configurationDirectory)
        # self.Database = Database.Database(self)
                
        self.schema = {
            "type" : "object",
            "properties" : {
                "runId" : {"type" : "string", "default" : "Uniquely generated Id"},
                "cellId" : {"type" : "string", "default" : "0"},
                "initialTick" : {"type" : "integer", "default" : 0},
                "initialTime" : {"type" : "number", "default" : 0.0},
                "endTime" : {"type" : "number"},
                "continueFromTick" : {"type" : "integer", "default" : "initialTick"}, 
                "scheduleIntervals" : {
                    "description" : 
                        "The intervals are executed in the listed order and must not overlap.",
                    "type" : "array",
                    "items" : {
                        "type" : "object",
                        "properties" : {
                            "startTick" : {
                                "type" : "integer", 
                                "default" : "Previous endTick + 1 or 0"
                                },
                            "endTick" : {
                                "anyOf" : [
                                    {"type" : "integer"},
                                    {"enum" : ["Infinity"]}
                                    ],
                                "default" : "Infinity"
                                },
                            "timePerTick" : {"type" : "number"}
                            },
                        "required" : [
                            "timePerTick"
                            ]
                        }
                    }
                },
            "required" : [
                "endTime",
                "scheduleIntervals"
                ]
            }
        
        self.data = self.Configuration.loadJsonFile("REDDIEGO.json", self.schema)
        
        if not "runId" in self.data:
            self.data["runId"] = datetime.now().strftime("%Y%m%d%H%M%S.") + str(os.getpid())

        os.mkdir(self.data["runId"])
        os.chdir(self.data["runId"])

        if not "cellId" in self.data:
            self.data["cellId"] = ''
        
        if self.data["cellId"] != '':
            os.mkdir(self.data["cellId"])
            os.chdir(self.data["cellId"])

        if not "initialTick" in self.data:
            self.data["initialTick"] = 0
            
        if not "initialTime" in self.data:
            self.data["initialTime"] = 0.0
            
        if not "continueFromTick" in self.data:
            self.data["continueFromTick"] = self.data["initialTick"]
        
        if self.data["continueFromTick"] < self.data["initialTick"]:
            sys.exit("ERROR: REDDIEGO invalid continueFromTick: '" + str(self.data["continueFromTick"]) + "'.")
            
        if self.data["endTime"] <= 0.0:
            sys.exit("ERROR: REDDIEGO invalid endTime: '" + str(self.data["endTime"]) + "'.")
        
        currentTime = self.data["initialTime"]
        currentTick = -1
        ToBeRemoved = list()
        
        for item in self.data["scheduleIntervals"]:
            if currentTime >= self.data["endTime"]:
                ToBeRemoved.append(item)
                continue
                
            if not "startTick" in item:
                item["startTick"] = currentTick + 1
                
            if  item["startTick"] <= currentTick:
                sys.exit("ERROR: REDDIEGO overlapping schedule interval with startTick:  '" + str(item["startTick"]) + "'.")
                
            if not "endTick" in item:
                item["endTick"] = float(inf)
            elif not isinstance(item["endTick"], int):
                item["endTick"] = float("inf")
                
            if item["endTick"] < item["startTick"]:
                sys.exit("ERROR: REDDIEGO invalid schedule interval: ['" + str(item["startTick"]) + "', '" + str(item["endTick"]) + "'].")
            
            if item["timePerTick"] <= 0.0:
                sys.exit("ERROR: REDDIEGO invalid schedule interval timePerTick: '" + str(item["timePerTick"]) + "'.")

            if currentTick < 0:
                maxTime = currentTime + (item["endTick"] - item["startTick"]) * item["timePerTick"]
            else: 
                maxTime = currentTime + (item["endTick"] - item["startTick"] + 1) * item["timePerTick"]
            
            if maxTime > self.data["endTime"]:
                item["endTick"] = item["startTick"] + (self.data["endTime"] - currentTime) / item["timePerTick"]
                
            currentTime = maxTime
            currentTick += item["endTick"] - item["startTick"] + 1
                 
        for item in ToBeRemoved:
            self.data["scheduleIntervals"].remove(item)
            
        if currentTime < self.data["endTime"]:
            sys.exit("ERROR: REDDIEGO endTime: '" + str(self.data["endTime"]) + "' will never be reached (max time: '" + str(currentTime) + "').")
            
        if currentTick < self.data["continueFromTick"]:
            sys.exit("ERROR: REDDIEGO continueFromTick: '" + str(self.data["continueFromTick"]) + "' will never be reached (max tick: '" + str(currentTick) + "').")

        self.Scheduler = Scheduler.Scheduler(self)


        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename = 'REDDIEGO.log')
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(10)
            
        return
    
    def run(self):
        self.Scheduler.start(self.data["initialTick"], self.data["initialTime"])
        
        for item in self.data["scheduleIntervals"]:
            self.Scheduler.step(max(item["startTick"], self.data["continueFromTick"]), item["endTick"], item["timePerTick"])
        
        self.Scheduler.end()
        return
    
    def getConfiguration(self):
        return self.Configuration
    
    # def getDatabase(self):
    #     return self.Database
    
    def getRunId(self):
        return self.data["runId"]
    
    def getCellId(self):
        return self.data["cellId"]
