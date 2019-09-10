#!/bin/bash

if echo $1|grep -q '[0-9][0-9]'; then
  docker run -d --privileged -h vhcalnplci.abap.local --dns-search=abap.local \
    -v sapdata$1:/sapdata --name sap$1 -p 32$1:3200 -p 80$1:8000 -p 443$1:44300 \
    -v /sys/fs/cgroup:/sys/fs/cgroup:ro saptrialvol
else
  echo mandatory parameter missing
fi