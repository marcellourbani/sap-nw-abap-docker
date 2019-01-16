# sap-nw-abap-docker

SAP NetWeaver ABAP Developer Edition in Docker

## What's in?

This Dockerfile creates a docker image using "docker build".

The installation command uses a pair of hacks to make sure the installation
process runs with hostname `vhcalnplci`. The hacks are necessary because it is
not possible to specify hostname on docker build command line.

One of the hack is changing the C functions returning hostname using
the library [libmock_hostname](https://github.com/jfilak/snippets/tree/master/mock_hostname).

## Extra content

The Dockerfile installs [PyRFC](https://github.com/SAP/PyRFC). If you want to use it, you need to
start python like this:

```bash
LD_LIBRARY_PATH=/sapmnt/NPL/exe/uc/linuxx86_64 python
```

I didn't put that path into the file /etc/ld.so.conf to avoid unintended side
effects in other SAP tools.

I install PyRFC to be able to call the function module SSFR**PUT**CRETIFICATE
to make SSL communication with GitHub trusted after the installation.

You can see the installed certificates in the directory [files/certs](files/certs/).

The only thing you need to do to enable abapGit is to install it.

## Installation

0. Download your version of [SAP NetWeaver ABAP 7.5x Developer Edition from SAP](https://tools.hana.ondemand.com/#abap). The files are compressed (RAR). Un-compress them into a folder named NW752. The folder must be at the same location where your Dockerfile is.

1. Set up docker on your instance

```sh
docker daemon --storage-opt dm.basesize=60G
```

2. Build the Docker image

```sh
docker build -v $PWD/NW752:/var/tmp/ABAP_Trial/NW752 -v $PWD/mock_hostname/ld.so.preload:/etc/ld.so.preload -v $PWD/mock_hostname/libmock_hostname.so:/usr/local/lib64/libmock_hostname.so -t abaptrial:752 .
```

3. Start the Docker container

```sh
docker run -d -v /sys/fs/cgroup:/sys/fs/cgroup:ro -p 3200:3200 -p 3300:3300 -p 8000:8000 -p 44300:44300 -h vhcalnplci --name testdrive abaptrial:752
```

or alternatively, use docker-compose (only to start the container, build is not
possible because of missing bind mounts).

```sh
docker-compose up -d
```

4. Done. NetWeaver ABAP is installed and ready to be used. Users, credentials, etc can be found in the fie readme.html shipped with the NetWeaver ABAP RAR files.

5. Now, you should register the system and commit the container myabap as a new image
