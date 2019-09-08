#!/bin/bash
echo $(grep $(uname -n) /etc/hosts | cut -f1 -d$'\t')  "vhcalnplci" >> /etc/hosts
export HOSTNAME="vhcalnplci"
echo $HOSTNAME > /etc/hostname 
echo "export HOSTNAME=$HOSTNAME" >> /etc/profile
test $(hostname) == $HOSTNAME || exit 1
export SAP_LOG_FILE="/var/tmp/abap_trial_install.log"; \
export PATH=/usr/local/bin/mock:$PATH
(/usr/local/bin/install.expect --password "S3cr3tP@ssw0rd" --accept-SAP-developer-license || exit 1; \
 (export LD_LIBRARY_PATH=/sapmnt/NPL/exe/uc/linuxx86_64; \
  python /usr/local/bin/sap_add_trusted_server_cert -v /etc/pki/ca-trust/source/SAP/*.cer); \
  su - npladm -c "stopsap ALL")