FROM ubuntu:22.04

ARG NB_USER="whovian"
ARG NB_UID=1000
ARG NB_GID=1000

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get install -yq --fix-missing software-properties-common  \
    apt-utils build-essential \
  && apt-get update \
  && apt-get install -yq --fix-missing --no-install-recommends \
    git autoconf dpkg xz-utils pkg-config \
  && apt-get install -yq --fix-missing --no-install-recommends libgflags-dev \
    nano make wget curl libgtk2.0-dev libglib2.0-0 libfreetype6-dev libleveldb-dev \
    tzdata unzip grep libsnappy-dev sed sudo locales fonts-dejavu \
    libtool automake zlib1g-dev libcurl4-gnutls-dev libssl-dev run-one emacs vim \
# ------------------------------------------------------------------------
  && ln -s /bin/tar /bin/gtar \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen \
# ------------------------------------------------------------------------
  && curl -L "https://github.com/krallin/tini/releases/download/v0.19.0/tini_0.19.0.deb" > tini.deb \
  && dpkg -i tini.deb \
  && rm tini.deb \
# --------------------------------------------------------------------------
# Install OpenSSH for MPI to communicate between containers
  && apt-get update \
  && apt-get install -y --no-install-recommends openssh-client openssh-server \
  && mkdir -p /var/run/sshd \
# --------------------------------------------------------------------------
# Allow OpenSSH to talk to containers without asking for confirmation
  && cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new \
  && echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new \
  && mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config \
# --------------------------------------------------------------------------
  && apt-get clean \
  && apt-get autoremove --yes \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/doc/ \
  && rm -rf /usr/share/man/

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# GLOBAL ENV VARIABLES

ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    HOME=/home/$NB_USER \
    MAKE_NUM_THREADS=4 \
    OMP_PROC_BIND=close \
    OMP_NUM_THREADS=3 \
    OPENMPI_VERSION=4.1.6 \
    GOSU_VERSION=1.16 \
    CONDAV=24.5.0-0

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Copy a script that we will use to correct permissions
# after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions \
  && sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc
# --------------------------------------------------------------------------
# https://github.com/jupyter/docker-stacks/pull/826
# Enable prompt color in the skeleton .bashrc before creating the NB_USER

# --------------------------------------------------------------------------
RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" \
  && unzip protoc-3.0.0-linux-x86_64.zip -d proto3 \
  && mv proto3/bin/* /usr/local/bin \
  && mv proto3/include/* /usr/local/include \
  && rm -rf proto3 protoc-3.0.0-linux-x86_64.zip 
# --------------------------------------------------------------------------
# INSTALL GOSU
RUN dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
  && curl -sSL "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-${dpkgArch}" > /usr/bin/gosu \
  && chmod 755 /usr/bin/gosu \
  && gosu nobody true \
# --------------------------------------------------------------------------
# INSTALL wait-for-it.sh
  && curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh > /usr/bin/wait-for-it.sh \
  && chmod 755 /usr/bin/wait-for-it.sh \
# --------------------------------------------------------------------------
  && ldconfig

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Create NB_USER wtih name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su \
    && sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers \
    && sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers \
    && useradd -m -s /bin/bash -N -u $NB_UID $NB_USER \
    && groupmod -g 1000 users \
    && mkdir -p $CONDA_DIR \
    && chown $NB_USER:$NB_GID $CONDA_DIR  \
    && chmod g+w /etc/passwd \
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# INSTALL CONDA
  && wget --quiet  \
https://repo.continuum.io/miniconda/Miniconda3-py39_${CONDAV}-Linux-x86_64.sh \
  && /bin/bash Miniconda3-py39_${CONDAV}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
  && rm Miniconda3-py39_${CONDAV}-Linux-x86_64.sh \
  && $CONDA_DIR/bin/conda config --system --set auto_update_conda false \
  && $CONDA_DIR/bin/conda config --system --set show_channel_urls true \
  && $CONDA_DIR/bin/conda config --system --set auto_activate_base false \
  && $CONDA_DIR/bin/conda config --system --prepend channels conda-forge \
  && $CONDA_DIR/bin/conda config --system --set channel_priority strict \
  && $CONDA_DIR/bin/conda clean --all -f -y   \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME  \
  && /usr/local/bin/fix-permissions $CONDA_DIR   
ENV PATH=$CONDA_DIR/bin:$PATH

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

COPY cocoapy39.yml $HOME/cocoapy39.yml
COPY init_cocoa39.sh $HOME/init_cocoa39.sh

RUN conda env create --name cocoa --file=$HOME/cocoapy39.yml --quiet --yes \
  && conda clean --all -f -y  \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && rm -rf $CONDA_DIR/share/man/* \
  && rm -rf $CONDA_DIR/envs/cocoa/man/* \
  && conda run --no-capture-output -n cocoa /bin/bash $HOME/init_cocoa39.sh \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR 

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# VM: solves an important use: ls -l `which sh` -> bash not dash
RUN echo "dash dash/sh boolean false" | debconf-set-selections
#RUN DEBIAN_FRONTEND=noninteractive dpkg-reconfigure dash

COPY jupyter_notebook_config.py $HOME/.jupyter/jupyter_notebook_config.py
COPY bashrc $HOME/bash.bashrc 

RUN chmod +x /usr/bin/tini \
  && chmod a+rwx $HOME/bash.bashrc \
  && mkdir -p $HOME/host/ && chmod -R a+rwx $HOME/host/ \
  && rm -rf ~/.cache/pip

EXPOSE 8888

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/bin/bash", "-c", "source $HOME/bash.bashrc; /bin/bash"]

USER $NB_UID
WORKDIR $HOME
VOLUME ["$HOME/host/"]

RUN /usr/local/bin/fix-permissions $HOME 


# REMIND HOW TO BUILD THIS FILE
# docker build . -f Dockerfile
# docker image ls
# docker tag XXX vivianmiranda/whovian-cocoa
# docker push vivianmiranda/whovian-cocoa