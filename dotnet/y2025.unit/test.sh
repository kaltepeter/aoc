#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
[[ ${DEBUG:-} == true ]] && set -o xtrace


# Simple test runner with minimal output
dotnet test dotnet/y2025.unit --nologo --verbosity minimal "$@"

