#!/bin/bash

set -o nounset
set -o errexit
set -o pipefail

[[ $# -ne 1 ]] && {
    echo "Usage: $0 INSTALL_FILES_DIR"
    exit 1
}

declare -r test_drive_sources="$( realpath $1 )"
declare -r test_drive_ld_preload="$( realpath $PWD/mock_hostname/ld.so.preload )"
declare -r test_drive_mock_hostname_lib="$( realpath $PWD/mock_hostname/libmock_hostname.so )"

[[ ! -d "$test_drive_sources" ]] && {
    echo "$test_drive_sources: not a directory"
    exit 1
}

[[ ! -f "$test_drive_ld_preload" ]] && {
    echo "$test_drive_ld_preload: not a file"
    exit 1
}

[[ ! -f "$test_drive_mock_hostname_lib" ]] && {
    echo "$test_drive_mock_hostname_lib: not a file"
    exit 1
}

docker build \
   -v $test_drive_sources:/var/tmp/ABAP_Trial \
   -v $test_drive_ld_preload:/etc/ld.so.preload \
   -v $test_drive_mock_hostname_lib:/usr/local/lib64/libmock_hostname.so \
   -t abaptrial:752 .
