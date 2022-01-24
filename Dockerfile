# Dockerfile for Maple
#
# Add commands that you want to run during the build process here. This file is 
# appended to an internal Dockerfile within Maple to build images using a docker backend.
#
# Do not include FROM statements in this file 
# FROM is used to define the base image for the build, which is 
# supplied through Maple CLI: ```maple image build <build-image-name> <base-image-name>```
#
# Do not include CMD statement in this file
# CMD is used to define commands to run inside the container which is done using
# Maple CLI: ```maple container run --image=<image-name> "<your-command>"```
#
# Similar functionality for a singularity definition file is currently not available
# but can be implemented if needed.
# ---------------------------------------------------------------------------------------------

# Build essential dependencies from ubuntu base
 ENV TZ=US/Michigan
 RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
 RUN apt-get update -y && apt-get install -y apt-utils && apt-get upgrade -y
 RUN apt-get install -y libhdf5-openmpi-dev openmpi-bin
 RUN apt-get install -y python python3 python3-dev python3-pip

# Install boost libraries
 RUN apt-get install -y libboost-all-dev

# Install vim and jupyter - do not install when building production images to reduce size
# RUN apt-get install -y vim git && pip3 install jupyter
