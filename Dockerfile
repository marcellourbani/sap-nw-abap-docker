FROM opensuse:latest

# Make sure we do not spend time preparing the OS
# while the installation sources are not mounted.
RUN test -f /tmp/NW751/install.sh

# General information
LABEL de.itsfullofstars.sapnwdocker.version="1.0.0-filak-sap-1"
LABEL de.itsfullofstars.sapnwdocker.vendor="Tobias Hofmann"
LABEL de.itsfullofstars.sapnwdocker.name="Docker for SAP NetWeaver 7.5x Developer Edition"
LABEL modified_by="Jakub Filak <jakub.filak@sap.com>"

# Install dependencies
RUN zypper --non-interactive install --replacefiles  uuidd expect tcsh which iputils vim hostname tar net-tools iproute2

# Run uuidd
# !!! And we must start uuidd even in containers - we need to employ init!
RUN mkdir /run/uuidd && chown uuidd /var/run/uuidd && /usr/sbin/uuidd

# Prepare the shell script to install NW ABAP without asking for user input (using expect)
# Note: Password being used is s@pABAP751
RUN echo $'#!/usr/bin/expect -f \n\
spawn /bin/bash /tmp/NW751/install.sh -s -k -h vhcalnplci \n\
set PASSWORD "s@pABAP751"\n\
set timeout -1\n\
expect "Hit enter to continue!" \n\
send "\\rq" \n\
expect "Do you agree to the above license terms? yes/no:"\n\
send "yes\\r"\n\
expect "Please enter a password:"\n\
send "$PASSWORD\\r"\n\
expect "Please re-enter password for verification:"\n\
send  "$PASSWORD\\r"\n\
expect eof' >> ./run.sh; chmod +x ./run.sh


# Expose the ports to work with NW ABAP
EXPOSE 8000
EXPOSE 44300
EXPOSE 3300
EXPOSE 3200

# HOSTNAME is imbued into SAP stuff - so we must convince the installer
# to use the well known HOSTNAME.
# And we have to try really hard, so don't forget to start docker build with:
#
# -v $PWD/mock_hostname/ld.so.preload -v $PWD/mock_hostname/libmockhostname.so:/usr/local/lib64/libmockhostname.so
#
# In case you want to know what the library does:
#   https://github.com/jfilak/snippets/tree/master/mock_hostname
#
RUN  export HOSTNAME="vhcalnplci"; \
     echo $HOSTNAME > /etc/hostname; \
     echo "export HOSTNAME=$HOSTNAME" >> /etc/profile; \
     echo 127.0.0.1   $HOSTNAME >> /etc/hosts; \
     test $(hostname) == $HOSTNAME || exit 1; \
     ./run.sh

# Avoid the need to start uuidd manually.
RUN systemctl enable uuidd

# Wrap the comman startsap in a systemd service, so we do not need to log in to
# the container and start it manually.
COPY nwabap.service /etc/systemd/system
RUN systemctl enable nwabap

# Here it comes, start your containers without the need to attach/exec and
# start SAP processes manually.
#
# Do not forget to bind mount cgroups:
# -v /sys/fs/cgroup:/sys/fs/cgroup:ro
#
ENTRYPOINT ["/usr/lib/systemd/systemd", "--system"]

# Command sequence to use this Dockerfile

# Before you start, please, configured docker to use devicemapper and set dm.basesize to 60G.
#
# $ docker daemon --storage-opt dm.basesize=60G

# To avoid the need to copy the installation files (10s of GBs), mount the directory with
# installation files to /tmp/NW751.

# And don't forget to patch install.sh to not create file in the source directory!
# Otherwise, the script will try to create a new temporary file in the your NW751 directory.
#
# $ patch NW751/install.sh 0001-Create-temp-inst-file-in-temp-dir.patch

# Finally, run the build command.
#
# $ docker build \
#    -v $PWD/NW751:/tmp/NW751 \
#    -v $PWD/mock_hostname/ld.so.preload:/etc/ld.so.preload \
#    -v $PWD/mock_hostname/libmockhostname.so:/usr/local/lib64/libmockhostname.so \
#    -t nwabap .
