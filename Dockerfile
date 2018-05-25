FROM opensuse:latest

# Make sure we do not spend time preparing the OS
# while the installation sources are not mounted.
RUN test -f /tmp/NW751/install.sh

# General information
LABEL de.itsfullofstars.sapnwdocker.version="1.0.0-filak-sap-1"
LABEL de.itsfullofstars.sapnwdocker.vendor="Tobias Hofmann"
LABEL de.itsfullofstars.sapnwdocker.name="Docker for SAP NetWeaver 7.5x Developer Edition"

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
# And we have to try really hard so don't forget to start docker build with:
# -v $PWD/mock_hostname/ld.so.preload -v $PWD/mock_hostname/libmockhostname.so:/usr/local/lib64/libmockhostname.so
RUN  export HOSTNAME="vhcalnplci"; \
     echo $HOSTNAME > /etc/hostname; \
     echo "export HOSTNAME=$HOSTNAME" >> /etc/profile; \
     echo 127.0.0.1   $HOSTNAME >> /etc/hosts; \
     test $(hostname) == $HOSTNAME || exit 1; \
     ./run.sh

# Command sequence to use this Dockerfile

# Before you start, please, configured docker to use devicemapper and set dm.basesize to 60G.

# To avoid the need to copy the installation files (10s of GBs), mount the directory with
# installation files to /tmp/NW751.

# And don't forget to patch install.sh to not create file in the source directory!
# BTW: you can ignore the chmod command - as we use the trick with '/bin/bash /tmp/NW751/install.sh'.

# $ docker build -v $PWD/NW751:/tmp/NW751 -t nwabap .

# Here is the patch:
# --- NW751/install.sh.bck        2018-03-23 14:17:01.833180534 +0100
# +++ NW751/install.sh    2018-03-23 14:20:22.346916898 +0100
# @@ -306,9 +306,10 @@
#          echo "Now we begin with the installation."
#          echo "Be patient, this will take a while ... "
#          echo " " 
# -        cp ${dvd_drive}/${dvd_dist_dir}/sapinst.txt ${dvd_drive}/${dvd_dist_dir}/sapinstmod.txt
# -       sed -i  "s/<INST_HOST>/${virt_hostname}/g" ${dvd_drive}/${dvd_dist_dir}/sapinstmod.txt 
# -       sed -i  "s/<Appl1ance>/${masterpwd}/g" ${dvd_drive}/${dvd_dist_dir}/sapinstmod.txt 
# +       local sapinstmod=$(mktemp -d)/sapinstmod.txt
# +        cp ${dvd_drive}/${dvd_dist_dir}/sapinst.txt $sapinstmod
# +       sed -i  "s/<INST_HOST>/${virt_hostname}/g" $sapinstmod
# +       sed -i  "s/<Appl1ance>/${masterpwd}/g" $sapinstmod
#           # now install the software 
#         if [ x"${skip_kernel_parameters}" = "xy" ]; then
#                 echo "Kernel parameters not set!"
# @@ -325,9 +326,9 @@
#          /usr/sap/hostctrl/exe/SAPCAR -xf ${dvd_drive}/${dvd_dist_dir}/SWPM10*.SAR -R /tmp/swpm
#         cd /tmp/swpm/
#         if [ x"${guimode}" = "xy" ]; then
# -               ./sapinst product.catalog SAPINST_EXECUTE_PRODUCT_ID=NW_StorageBasedCopy SAPINST_INPUT_PARAMETERS_URL=${dvd_drive}/${dvd_dist_dir}/sapinstmod.txt
# +               ./sapinst product.catalog SAPINST_EXECUTE_PRODUCT_ID=NW_StorageBasedCopy SAPINST_INPUT_PARAMETERS_URL=$sapinstmod
#         else
# -               ./sapinst product.catalog SAPINST_EXECUTE_PRODUCT_ID=NW_StorageBasedCopy SAPINST_INPUT_PARAMETERS_URL=${dvd_drive}/${dvd_dist_dir}/sapinstmod.txt -nogui -noguiserver SAPINST_SKIP_DIALOGS=true
# +               ./sapinst product.catalog SAPINST_EXECUTE_PRODUCT_ID=NW_StorageBasedCopy SAPINST_INPUT_PARAMETERS_URL=$sapinstmod -nogui -noguiserver SAPINST_SKIP_DIALOGS=true
#         fi
#         if [ $? -eq 0 ]; then
#                 rm -rf /tmp/sapinst_instdir
