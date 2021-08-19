#!/usr/bin/python3
from github import Github
token="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"
g = Github(token)
repo = g.get_repo("liya2017/ci_sample")
pr = repo.get_pulls()
print(pr.get_page(0))
repo.get_commit(sha='342b7070f8c76f266de94beaad0554ab13099ea0').create_status(
    state="success",
    # target_url="https://github.com/liya2017/ci_sample/actions/runs/1149902863",
    description="CI is building",
    context="ci"
)