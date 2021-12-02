#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
[[ ${DEBUG:-} == true ]] && set -o xtrace
readonly __dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sh "${__dir}/../../download-data.sh" https://www.hackerrank.com/rest/contests/master/challenges/30-hello-world/download_testcases
