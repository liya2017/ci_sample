#!/bin/bash
set +e
echo $PR_COMMONS_BODY
echo "$PR_COMMONS_BODY" | grep -q "Need to cherry-pick to the release branch"
          curl -X "POST" "https://api.github.com/repos/${{ github.repository }}/issues" \
              -H "Authorization: token ${{ secrets.REPO_ACCESS_TOKEN }}" \
              -H "Content-Type: text/plain; charset=utf-8" \
              -d $'{
            "title": '$title',
            "body": "TBD",
            "assignees": [
              "liya2017"
            ],
            "labels": [
              "s:backport-needed"
            ]
          }'







