#!/usr/bin/python3
import requests
import json
import time
import datetime
import os
import sys
from dotenv import load_dotenv
from github import Github
load_dotenv()
job_runs_info=str(os.getenv('workspace'))+"/job_runs_info.txt"
job_info=str(os.getenv('workspace'))+"/job_info.txt"
headers = {"Authorization": "token "+str(os.getenv('TOKEN'))}
def run_query(url): # A  function to use requests.get to make the API call. Note the json= section.
    request = requests.get(url,headers=headers)
    link = request.headers.get('link', None)
    if link is not None:
        print(link)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failure to run by returning code of {}. {}".format(request.status_code))
#function to call commit check suit
def get_check_suite(commit_sha):
    url="https://api.github.com/repos/liya2017/ci_sample/commits/"+commit_sha+"/check-suites"
    check_suite_result=run_query(url)
    data = {}
    data['job_run_info']=[]
    for num in range(len(check_suite_result["check_suites"])):
        if (check_suite_result["check_suites"][num]["app"]["slug"] == "github-actions"):
            data["job_run_info"].append({
           'job_run_url':check_suite_result["check_suites"][num]["check_runs_url"]
           })  
    with open(job_runs_info, 'w') as outfile:
            json.dump(data, outfile)

# function to get each job info from each checkruns     
def get_check_runs(commit_sha):
    get_check_suite(commit_sha)
    f = open(job_runs_info,"r") 
    data = json.load(f)
    job_data={}
    job_data["job_details"]=[]
    for i in range(len(data['job_run_info'])):
        job_run_url=data['job_run_info'][i]["job_run_url"]
        job_info_res=run_query(job_run_url)
        for j in range(len(job_info_res["check_runs"])):
            print(job_info_res["check_runs"][j]["name"])
            job_data["job_details"].append({
            'job_name':job_info_res["check_runs"][j]['name'],
            'job_status':job_info_res["check_runs"][j]['status'],
            'job_conclusion':job_info_res["check_runs"][j]['conclusion'],
            'job_started_at':job_info_res["check_runs"][j]['started_at'],
            'job_completed_at':job_info_res["check_runs"][j]['completed_at']
            })
    with open(job_info, 'w') as outfile:
            json.dump(job_data, outfile)
#function to check job's conculusions
def check_runs_conculusions(commit_sha):
    print("check_runs_conculusions"+str(commit_sha))
    get_check_runs(commit_sha)
    f = open(job_info,"r") 
    jobs_data= json.load(f)
    print("jobs_data")
    print(jobs_data)
    print("jobs_data done")
    CI_conclusion=""
    required_jobs_count=0
    failure_reson=""

    UnitTest_macOS_conclusion=""
    UnitTest_Linux_conclusion=""
    UnitTest_Windows_conclusion=""
    Liners_macOS_conclusion=""
    Liners_Linux_conclusion=""

    UnitTest_conclusion=""
    Liners_conclusion=""


    for i in range(len(jobs_data["job_details"])):
        #Unit test conclusion
        if (jobs_data["job_details"][i]["job_name"]).find("ci_unit_tests (ubuntu") != -1:
            UnitTest_Linux_conclusion=jobs_data["job_details"][i]["job_conclusion"]
        if (jobs_data["job_details"][i]["job_name"]).find("ci_unit_tests (macos") != -1:
            UnitTest_macOS_conclusion=jobs_data["job_details"][i]["job_conclusion"]
        if (jobs_data["job_details"][i]["job_name"]).find("ci_unit_tests (windows") != -1:
            UnitTest_Windows_conclusion=jobs_data["job_details"][i]["job_conclusion"]
        #liners test conclusion
        if (jobs_data["job_details"][i]["job_name"]).find("ci_liners (ubuntu") != -1:
            Liners_Linux_conclusion=jobs_data["job_details"][i]["job_conclusion"]
        if (jobs_data["job_details"][i]["job_name"]).find("ci_liners (macos") != -1:
            Liners_macOS_conclusion=jobs_data["job_details"][i]["job_conclusion"]

    if (UnitTest_macOS_conclusion == "success" ) | (UnitTest_Linux_conclusion == "success" ) | (UnitTest_Windows_conclusion == "success" ):
        UnitTest_conclusion="success"
        required_jobs_count +=1
    elif (UnitTest_macOS_conclusion == "failure" ) | (UnitTest_Linux_conclusion == "failure" ) | (UnitTest_Windows_conclusion == "failure" ):
        UnitTest_conclusion="failure"
        required_jobs_count +=1

    if (Liners_macOS_conclusion == "success" ) | (Liners_Linux_conclusion == "success" ):
        Liners_conclusion="success"
        required_jobs_count +=1
    elif (Liners_macOS_conclusion == "failure" ) | (Liners_Linux_conclusion == "failure" ):
        Liners_conclusion="failure"
        required_jobs_count +=1
    jobs_conclusion=[UnitTest_conclusion,Liners_conclusion]
    # check child jobs conclusions if all required jobs completed in one os
    if ( required_jobs_count == 2 ):
        #set ci conclusion
        if  "failure" in jobs_conclusion:
            CI_conclusion="failure"
        else:
            CI_conclusion="success"
    if (CI_conclusion !=""):
       print("call update_commit_state")
       update_commit_state(CI_conclusion,COMMIT_SHA)
def update_commit_state(CI_conclusion,COMMIT_SHA):
    g = Github(os.getenv('TOKEN'))
    repo = g.get_repo(os.getenv('REPOSITPRY'))
    print("COMMIT_SHA"+str(COMMIT_SHA))
    print("CI_conclusion:"+str(CI_conclusion))
    repo.get_commit(sha=COMMIT_SHA).create_status(
        state=str(CI_conclusion),
        # target_url="https://github.com/liya2017/ci_sample/actions/runs/1149902863",
        description="ci",
        context="ci"
    )
    print("update_commit_state done")

if __name__ == '__main__':

   COMMIT_SHA=''
   if str(os.getenv('EVENT_NAME')) == "push":
      COMMIT_SHA=str(os.getenv('COMMIT_SHA'))

   if str(os.getenv('EVENT_NAME')) == "pull_request":
      COMMIT_SHA=str(os.getenv('PR_COMMIT_SHA'))
   check_runs_conculusions(COMMIT_SHA)


