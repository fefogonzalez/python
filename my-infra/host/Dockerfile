# HOST image - used to create containers to be managed by master

# use builded ansible_base (defined in ../base/Dockerfile) as a starting point
#FROM ansible_base:latest
FROM ubuntu:latest

# install required packages
RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        aptitude iputils-ping net-tools man vim openssh-server python \
    && rm -rf /var/lib/apt/lists/*

# ensure that required directories are created
RUN mkdir /var/run/sshd
RUN mkdir /root/.ssh





# copy script from local disk to file system inside Docker image
COPY run.sh /var/

# adjust file permissions to make run.sh executable
RUN chmod 755 /var/run.sh