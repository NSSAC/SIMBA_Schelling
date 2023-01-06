#!/usr/bin/env bash

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

while :; do
    case $1 in
        --mode)
            shift;
            mode=$1
            ;;
        --startTick)
            shift;
            startTick=$1
            ;;
        --startTime)
            shift;
            startTime=$1
            ;;
        --lastRunTick)
            shift;
            lastRunTick=$1
            ;;
        --lastRunTime)
            shift;
            lastRunTime=$1
            ;;
        --currentTick)
            shift;
            currentTick=$1
            ;;
        --currentTime)
            shift;
            currentTime=$1
            ;;
        --targetTick)
            shift;
            targetTick=$1
            ;;
        --targetTime)
            shift;
            targetTime=$1
            ;;
        --endTick)
            shift;
            endTick=$1
            ;;
        --endTime)
            shift;
            endTime=$1
            ;;
        --status)
            shift
            status=$1
            ;;
        ?*)
            args="$args $1"
            ;;
         *)               # Default case: No more options, so break out of the loop.
            break
     esac
  
    shift
done

case $mode in
    start)
        case $processMode in
            pre) 
                ln -s ${REDDIEGO_ConfigurationDirectory}/base base
                mkdir tick_$startTick
                cp base/dynamic/* tick_$startTick
                ;;
            post)
                ;;
        esac
        ;;
    step)
        case $processMode in
            pre) 
                chmod -R a-w tick_$currentTick
                mkdir tick_$targetTick
                cp base/dynamic/* tick_$targetTick
                ;;
            post)
                ;;
        esac
        ;;
    end)
        case $processMode in
            pre) 
                ;;
            post)
                chmod -R a-w tick_$endTick
                ;;
        esac
        ;;
    *)
        echo Invalid mode: $mode
        exit 1
        ;;
esac

echo success > $status
exit 0