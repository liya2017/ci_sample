#!/bin/bash
set -e
set -u
[ -n "${DEBUG:-}" ] && set -x || true

set +e
echo ${COMMIT_MESSAGE}
if [[ ${COMMIT_MESSAGE} =~ "skip ci" ]];then
 echo "skip ci"
else
 echo "no sikp ci"
fi

EXIT_STATUS="$?"

set -e
if [ "$EXIT_STATUS" = 0 ]; then
    echo "Check whether the ci succeeds"
else
    echo "Fail the ci"
fi
exit $EXIT_STATUS
