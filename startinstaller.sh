#!/bin/bash

docker run -d --privileged -v /hdd/D/local/NW752:/var/tmp/ABAP_Trial/ \
  -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v sapdata:/sapdata \
  --name installer  -h vhcalnplci \
  --dns-search=abap.local abapinstaller:752  bash
