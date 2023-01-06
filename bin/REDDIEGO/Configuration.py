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

import os
import json
import sys
from jsonschema import validate

class Configuration:
    
    def __init__(self, configurationDirectory):
        self.configurationDirectory = os.path.abspath(configurationDirectory)
        os.environ['REDDIEGO_ConfigurationDirectory'] = self.configurationDirectory

    def loadJsonFile(self, fileName, schema = None):
    
        try:
            jsonFile = open(os.path.join(self.configurationDirectory, fileName),"r")
        
        except:
            sys.exit("ERROR: File '" + os.path.join(self.configurationDirectory, fileName) + "' does not exist.")
        
        dictionary = json.load(jsonFile)
        
        if schema != None:
            validate(dictionary, schema)
            
        jsonFile.close()
        return dictionary
