# BEGIN: Copyright 
# Copyright (C) 2020 Rector and Visitors of the University of Virginia 
# All rights reserved 
# END: Copyright 

# BEGIN: License 
# Licensed under the Apache License, Version 2.0 (the "License"); 
# you may not use this file except in compliance with the License. 
# You may obtain a copy of the License at 
#   http://www.apache.org/licenses/LICENSE-2.0 
# END: License 

import psycopg2

class Database:

    def __init__(self, REDDIEGO):
        self.REDDIEGO = REDDIEGO
        
        self.schema = {
            "type" : "object",
            "properties" : {
                "host" : {"type" : "string"},
                "port" : {"type" : "number"},
                "database" : {"type" : "string"},
                "user" : {"type" : "string"},
                "password" : {"type" : "string"}
                },
            "required" : [
                "host",
                "port",
                "database",
                "user",
                "password"
                ]
            }
        
        self.data = self.REDDIEGO.getConfiguration().loadJsonFile("database.json", self.schema)
        
        try:
            conn = psycopg2.connect(
                host=self.data["host"],
                port = self.data["port"],
                database=self.data["database"],
                user=self.data["user"],
                password=self.data["password"])
            
        except:
            pass
        
        return
            
        
    def getConnectionInfo(self):
        return self.data
    
    def getHost(self):
        return self.data["host"]
        
    def getPort(self):
        return self.data["port"]
        
    def getDatabase(self):
        return self.data["database"]
        
    def getUser(self):
        return self.data["user"]
        
    def getPassword(self):
        return self.data["password"]
