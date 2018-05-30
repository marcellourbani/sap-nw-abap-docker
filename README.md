# sap-nw-abap-docker
SAP NetWeaver ABAP Developer Edition in Docker

# Installation

A detailed blog on how to get this image and container up and running can be found on my blog: [DOCKERFILE FOR SAP NETWEAVER ABAP 7.5X DEVELOPER EDITION](https://www.itsfullofstars.de/2017/09/dockerfile-for-sap-netweaver-abap-7-5x-developer-edition/)

To be able to setup the Docker container with just one command, make sure to read my blog [ADJUST IMAGE SIZE OF DOCKER QCOW2 FILE
](https://www.itsfullofstars.de/2017/12/adjust-the-image-size-of-docker/). SAP NetWeaver is somewhat too large for Docker, and you can get a no space left on device error when installing it on a default Docker installation. The blog expains how to increase the Docker image file size by 100G, allowing to setup SAP NetWeaver ABAP by just running docker build -t abap .

## Short version

0. Download your version of [SAP NetWeaver ABAP 7.5x Developer Edition from SAP](https://tools.hana.ondemand.com/#abap). The files are compressed (RAR). Un-compress them into a folder named NW751. The folder must be at the same location where your Dockerfile is.

1. Set up docker on your instance

```sh
docker daemon --storage-opt dm.basesize=60G
```

2. Patch the install.sh

```sh
patch NW751/install.sh 0001-Create-temp-inst-file-in-temp-dir.patch
```

2. Build the Docker image

```sh
docker build -v $PWD/NW751:/tmp/NW751 -v $PWD/mock_hostname/ld.so.preload:/etc/ld.so.preload -v $PWD/mock_hostname/libmockhostname.so:/usr/local/lib64/libmockhostname.so -t nwabap .
```

3. Start the Docker container

```sh
docker run -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 3200:3200 -p 3300:3300 -p 8000:8000 -p 44300:44300 -h vhcalnplci --name myabap nwabap
```

or alternatively, use docker-compose

```sh
docker-compose up -d
```

4. Done. NetWeaver ABAP is installed and ready to be used. Users, credentials, etc can be found in the fie readme.html shipped with the NetWeaver ABAP RAR files.

5. Now, you should register the system and commit the container myabap as a new image
