#!/bin/bash

#Prevent executing in wrong directory
CURRENT_DIR=$(pwd)
if [[ ! "$CURRENT_DIR" =~ "feedbot" ]]; then 
     echo "Current directory is wrong"; exit 1
fi

cd feedbot-app/ || exit 1
/bin/bash app-deploy.sh &

cd feedsender-app/ || exit 1
/bin/bash app-deploy.sh &

cd feedparser-app/ || exit 1
/bin/bash app-deploy.sh &

jobs

