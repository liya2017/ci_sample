#!/bin/bash
set -e
set -u
case $GITHUB_WORKFLOW in
	ci_linters*)
		echo "Hellow ci_linters!"
		;;
	ci_unit_test*)
		echo "See you unit_test!"
		;;
	*)
		echo -n "unknown"
		;;
esac
EXIT_STATUS="$?"
exit $EXIT_STATUS
