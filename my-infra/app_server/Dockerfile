# MASTER image - used to create the master container to manage hosts

# use builded ansible_base (defined in ../base/Dockerfile) as a starting point
FROM ubuntu:latest


# install required packages
RUN apt-get update \
    && apt-get install --no-install-recommends --no-install-suggests -y \
        aptitude iputils-ping net-tools man vim openssh-server python3  python3-paramiko mysql-client python3-pymysql \
    && rm -rf /var/lib/apt/lists/*

# ensure that required directories are created
RUN mkdir /var/run/sshd
RUN mkdir /root/.ssh

# copy content of ansible directory from local disk to file system inside Docker image
COPY my-app /var/ans/

# change working directory
WORKDIR /var/ans

# generate RSA key pair to allow master to communicate with managed nodes
# default private key passphrase is '12345' (not a good idea for production environment ;)
RUN ssh-keygen -t rsa -N 12345 -C "master key" -f master_key
