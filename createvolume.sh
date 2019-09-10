#!/bin/bash
if echo $1|grep -q '[0-9][0-9]'; then
  lz4 -dc /hdd/D/local/docker_backups/sapdata.tar.lz4 |docker run -i --rm -v sapdata$1:/sapdata alpine tar xvf - -C /sapdata
else
  echo mandatory parameter missing
fi