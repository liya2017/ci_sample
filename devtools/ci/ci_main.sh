#!/bin/bash
set -e
set -u
is_self_runner=`echo $RUNNER_LABEL | awk -F '-' '{print $1}'`
if [[ $is_self_runner == "self" ]];then
    CARGO_TARGET_DIR=$GITHUB_WORKSPACE/../target
fi
CARGO_TARGET_DIR=${CARGO_TARGET_DIR:-"$GITHUB_WORKSPACE/target"}
case $GITHUB_WORKFLOW in
	ci_linters*)
		echo "Hellow ci_linters!"
		echo "CARGO_TARGET_DIR is  "$CARGO_TARGET_DIR
		;;
	ci_unit_test*)
		echo "See you unit_test!"
		echo "CARGO_TARGET_DIR is  "$CARGO_TARGET_DIR
		;;
	*)
		echo -n "unknown"
		;;
esac
EXIT_STATUS="$?"
exit $EXIT_STATUS
