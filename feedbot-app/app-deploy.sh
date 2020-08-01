#!/bin/bash
GREEN_COLOR='\033[1;32m'
NO_COLOR='\033[0m'

#Prevent executing in wrong directory
CURRENT_DIR=$(pwd)
if [[ ! "$CURRENT_DIR" =~ "-app" ]]; then 
     echo "Current directory is wrong"; exit 1
fi

# Append enviromnent variables to file
echo '' >> app.yaml;
cat ../env.yaml >> app.yaml;

# Deploy at Google App Engine
gcloud -q app deploy
echo -e "${GREEN_COLOR}Deploy Executed${NO_COLOR}"

# Return file to previous state
FILE_ORIGINAL_STATE=$(grep -v -x -f ../env.yaml app.yaml)
echo "$FILE_ORIGINAL_STATE" | tee app.yaml