#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
[[ ${DEBUG:-} == true ]] && set -o xtrace
readonly __dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

[[ -z "${1:-}" ]] && sh -c 'echo "First argument must be a download link for a zip."; exit 1;'

solution_dir="${__dir}/tmp/solution"

if [[ -d "${solution_dir}" ]]; then
  rm -rf "${solution_dir}"
fi

solution_zip="${__dir}/tmp/solution.zip"
curl "${1}" -o "${solution_zip}"
unzip -d "${__dir}/tmp/solution" -o "${solution_zip}"
rm "${solution_zip}"

if [[ -d "${solution_dir}" ]]; then
  echo "Example downloaded"
else
  echo "Failed to download solution"
  exit 1
fi
