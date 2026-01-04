#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
[[ ${DEBUG:-} == true ]] && set -o xtrace

day="${1:-}"
filter=()

if [[ -n "${day}" ]]; then
  filter=(--filter "FullyQualifiedName~y2025.unit.day_${day}")
fi

dotnet test dotnet/y2025.unit --nologo --logger "console;verbosity=detailed" "${filter[@]}"
