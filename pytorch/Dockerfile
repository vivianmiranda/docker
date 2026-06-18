FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get install -yq --fix-missing software-properties-common apt-utils build-essential \
  && add-apt-repository -y universe \
  && add-apt-repository -y multiverse \
  && apt-get update \
  && apt-get install -yq --fix-missing --no-install-recommends \
    git autoconf dpkg git-lfs xz-utils pkg-config libgflags-dev python3  \
    libhdf5-dev nano make wget curl libleveldb-dev python3-dev \
    sqlite3 fonts-liberation tzdata unzip grep libsnappy-dev python3-pip \
    sed libsqlite3-dev sudo locales fonts-dejavu libgoogle-glog-dev less  \
    libtool automake zlib1g-dev libcurl4-gnutls-dev \
    vim man-db cmake cm-super ghostscript dvipng zip tar \
# ------------------------------------------------------------------------
  && ln -s /bin/tar /bin/gtar \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen \
# --------------------------------------------------------------------------
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
  && rm -rf /var/lib/apt/lists/*

ARG NB_USER="whovian"
ARG NB_UID=1005
ARG NB_GID=1005
# --------------------------------------------------------------------------
# GLOBAL ENV VARIABLES
ENV SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    HOME=/home/$NB_USER \
    MAKE_NUM_THREADS=4 \
    GOSU_VERSION=1.16 \
    CONDA_DIR=/opt/conda
# --------------------------------------------------------------------------
# Copy a script that we will use to correct permissions
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions \
# --------------------------------------------------------------------------
# Enable prompt color in the skeleton .bashrc before creating the NB_USER
  && sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc
# --------------------------------------------------------------------------
# protoc (Protocol Buffers compiler)
ENV PROTOC_VERSION=34.1
RUN curl -sSL -o protoc.zip \
    "https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}-linux-x86_64.zip" \
  && unzip -q protoc.zip -d /tmp/proto \
  && mv /tmp/proto/bin/* /usr/local/bin/ \
  && mv /tmp/proto/include/* /usr/local/include/ \
  && chmod 755 /usr/local/bin/protoc \
  && rm -rf /tmp/proto protoc.zip
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
# Create NB_USER and make sure dirs are writable by 'users' group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su \
    && sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers \
    && sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers \
    && useradd -m -s /bin/bash -N -u $NB_UID $NB_USER \
    && groupmod -g 1005 users \
    && chmod g+w /etc/passwd 
# --------------------------------------------------------------------------
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
       python3-venv \
       python3-pip \
  && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install \
    'numpy' \
    'tensorflow==2.18.0' \
    'tensorflow_probability==0.25.0' \
    'keras==3.6.0' \
    'torch==2.5.1' \
    'torchvision==0.20.1' \
    'torchaudio==2.5.1' \
    'scikit-learn==1.7.2' \
    'jupyter>=1.1' \
    'typing-extensions==4.13.2' \
    'pytest==8.3.5' \
    'jax[cuda12]==0.4.30' \
    'astropy' \
    'getdist==1.7.7' \
    'matplotlib==3.10.9' \
    'numba' \
    'iminuit' \
    'scipy' \
    'pandas' \
    'sympy' \
    'multiprocess' \
    'virtualenv' \
    'imageio' \
    --no-cache-dir \
    --prefer-binary \
    --extra-index-url "https://download.pytorch.org/whl/cu121"
# --------------------------------------------------------------------------
# Critical: let whovian modify the venv later
RUN chown -R $NB_UID:$NB_GID /opt/venv \
  && chmod -R u+rwX,g+rwX /opt/venv
# --------------------------------------------------------------------------
USER root

# 1) System fonts + fontconfig
RUN apt-get update && apt-get install -y --no-install-recommends \
      fontconfig \
      fonts-dejavu-core \
      fonts-liberation \
    && rm -rf /var/lib/apt/lists/*
RUN fc-cache -fv

# 2) matplotlib cache outside /home so bind-mounted homes can't shadow it
ENV MPLCONFIGDIR=/opt/matplotlib-cache
RUN mkdir -p $MPLCONFIGDIR \
 && chown -R $NB_UID:$NB_GID $MPLCONFIGDIR \
 && chmod -R a+rwX $MPLCONFIGDIR

# 3) Warm the cache as the notebook user
USER $NB_UID
RUN python -c "import matplotlib; matplotlib.use('Agg'); \
import matplotlib.pyplot as plt; \
fig, ax = plt.subplots(); ax.plot([1,2,3]); \
fig.savefig('/tmp/_warmup.png'); \
print('cache dir:', matplotlib.get_cachedir())" \
 && rm -f /tmp/_warmup.png

USER root
# --------------------------------------------------------------------------
RUN mkdir -p $HOME/.jupyter 

RUN /usr/local/bin/fix-permissions $HOME 
RUN /usr/local/bin/fix-permissions $HOME/.jupyter

RUN chown -R $NB_USER:$NB_GID $HOME
RUN chown -R $NB_USER:$NB_GID $HOME/.jupyter 
# --------------------------------------------------------------------------
# VM: solves an important use: ls -l `which sh` -> bash not dash
RUN echo "dash dash/sh boolean false" | debconf-set-selections

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

# REMIND HOW TO BUILD THIS FILE
# docker build . -f Dockerfile
# docker image ls
# docker tag 6ce9968b6d0a vivianmiranda/whovian-pytorch-amypond
# docker push vivianmiranda/whovian-pytorch-amypond
# How to run?
# docker run --gpus all --platform linux/amd64 --hostname pytorch \
#  --name pytorch -it -p 8888:8888 -v "$(pwd)":/home/whovian/host/ \
#   -v ~/.ssh:/home/whovian/.ssh:ro vivianmiranda/whovian-pytorch-amypond