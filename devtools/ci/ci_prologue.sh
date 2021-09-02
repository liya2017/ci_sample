#!/bin/bash

set +e

if [ $EVENT_NAME == "push" ];then
   COMMIT_SHA=$COMMIT_SHA
   MESSAGE="$COMMIT_MESSAGE"
   echo $MESSAGE | grep -q "ci-runs-on: "
   if [ $? -eq 0 ]; then
     runs_on=` echo "${MESSAGE}"| grep "runs_on" | awk -F 'runs-on' '{print $1}' | awk -F ':' '{print $2}'`
   else
     runs_on=' [ "ubuntu-20.04","macos-10.15","windows-2019" ] '
   fi
fi
if [ $EVENT_NAME == "pull_request" ];then
    COMMIT_SHA=$PR_COMMIT_SHA
    MESSAGE="$PR_COMMONS_BODY"
fi

echo $MESSAGE | grep -q "runs_on:"

if [ $? -eq 0 ]; then
    runs_on=` echo "${MESSAGE}"| grep "runs_on" | awk -F 'runs-on' '{print $1}' | awk -F ':' '{print $2}'`
elif [ ! -n ${CI_RUNS_ON} ]; then
    runs_on='${{secrets.CI_RUNS_ON}}'
elif [[ ${REPO_OWNER} != "nervosnetwork" ]] || [[ ${REPO_OWNER} == "nervosnetwork" && ${EVENT_NAME}} == 'pull_request' && $nervosnetwork_actor_list != *$REPO_ACTOR* ]]; then
    runs_on=' [ "ubuntu-20.04","macos-10.15","windows-2019" ] '
else
    runs_on=' [ "self-hosted-ci-ubuntu-20.04",macos-10.15","windows-2019" ] '
fi
echo  $runs_on
