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
  && add-apt-repository ppa:ubuntu-toolchain-r/test \
  && apt-get update \
  && apt-get install -yq --fix-missing --no-install-recommends \
    git autoconf dpkg git-lfs xz-utils pkg-config python3-pip \
  && apt-get install -yq --fix-missing --no-install-recommends libgflags-dev \
    libhdf5-dev libarpack2-dev nano make wget curl \
    libgtk2.0-dev libglib2.0-0 libfreetype6-dev libleveldb-dev \
    sqlite3 libv4l-dev tzdata unzip grep libsnappy-dev \
    sed libsqlite3-dev sudo locales fonts-dejavu libgoogle-glog-dev  libx264-dev \
    libtool automake zlib1g-dev libcurl4-gnutls-dev libssl-dev \
    libtiff5-dev run-one emacs vim gfortran gcc g++ libtbb-dev libeigen3-dev libswscale-dev \
    "openjdk-11-jre-headless" libatlas-base-dev libgtk-3-dev libxvidcore-dev \
# ------------------------------------------------------------------------
  && ln -s /bin/tar /bin/gtar \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen \
# ------------------------------------------------------------------------
  && python3 -m pip install pip --upgrade --quiet --no-cache-dir \
  && pip3 install numpy==1.24.0 --quiet --no-cache-dir \
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
    OPENMPI_VERSION=4.0.7 \
    GOSU_VERSION=1.16 \
    CONDAV=4.12.0

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Copy a script that we will use to correct permissions
# after running certain commands
COPY fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions \
# --------------------------------------------------------------------------
# https://github.com/jupyter/docker-stacks/pull/826
# Enable prompt color in the skeleton .bashrc before creating the NB_USER
  && sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# INSTALL CORE RESEARCH LIBRARIES FROM SOURCE (For native Cosmolike)

# --------------------------------------------------------------------------
RUN git clone  https://github.com/Kitware/CMake.git \
  && cd ./CMake \
  && git checkout v3.16.0 \
  && ./bootstrap \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf CMake 
# --------------------------------------------------------------------------
RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" \
  && unzip protoc-3.0.0-linux-x86_64.zip -d proto3 \
  && mv proto3/bin/* /usr/local/bin \
  && mv proto3/include/* /usr/local/include \
  && rm -rf proto3 protoc-3.0.0-linux-x86_64.zip 
# --------------------------------------------------------------------------
RUN wget --no-check-certificate https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-${OPENMPI_VERSION}.tar.gz \
  && tar xvzf openmpi-${OPENMPI_VERSION}.tar.gz \
  && rm -rf openmpi-${OPENMPI_VERSION}.tar.gz \
  && cd openmpi-${OPENMPI_VERSION} \
  && CFLAGS=-O3 CXXFLAGS=-O3 ./configure --prefix=/usr \
    --enable-orterun-prefix-by-default --enable-wrapper-rpath \
  && make -j $MAKE_NUM_THREADS all \
  && make install \
  && cd ../ \
  && rm -rf openmpi-${OPENMPI_VERSION} 
# --------------------------------------------------------------------------
RUN git clone https://github.com/xianyi/OpenBLAS.git \
  && cd OpenBLAS \
  && git checkout v0.3.21 \
  && make -j $MAKE_NUM_THREADS USE_OPENMP=1 all \
  && make install PREFIX=/usr/local \
  && cd ../ \
  && rm -rf OpenBLAS/ 
# --------------------------------------------------------------------------
RUN git clone https://github.com/Reference-LAPACK/lapack lapack \
  && cd lapack \
  && git checkout v3.11.0 \
  && mkdir build \
  && cd build \
  && cmake -DBUILD_SHARED_LIBS=TRUE --prefix=/usr/local --log-level=ERROR .. \
  && make -j $MAKE_NUM_THREADS all \
  && make install \
  && cd ../../ \
  && rm -rf lapack-3.11.0/ 
# --------------------------------------------------------------------------
RUN wget -q http://ftp.wayne.edu/gnu/gsl/gsl-2.7.tar.gz \
  && tar zxvf gsl-2.7.tar.gz \
  && rm -f gsl-2.7.tar.gz \
  && cd gsl-2.7 \
  && ./configure --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf gsl-2.7/ 
# --------------------------------------------------------------------------
RUN wget -q http://www.fftw.org/fftw-3.3.10.tar.gz \
  && tar zxvf fftw-3.3.10.tar.gz \
  && rm -f fftw-3.3.10.tar.gz \
  && cd fftw-3.3.10/ \
  && ./configure --enable-openmp --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf fftw-3.3.10/ 
# --------------------------------------------------------------------------
RUN wget -q http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-4.2.0.tar.gz \
  && tar zxvf cfitsio-4.2.0.tar.gz \
  && rm -f cfitsio-4.2.0.tar.gz \
  && cd cfitsio-4.2.0/ \
   && mkdir build \
  && cd build \
  && cmake -DBUILD_SHARED_LIBS=TRUE --log-level=ERROR .. \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../../ \
  && rm -rf cfitsio-4.2.0/ \
  && ldconfig 
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
    && chown $NB_USER:$NB_GID $CONDA_DIR \
    && chmod g+w /etc/passwd \
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# INSTALL CONDA
  && wget --quiet \
https://repo.continuum.io/miniconda/Miniconda3-py38_${CONDAV}-Linux-x86_64.sh \
  && /bin/bash Miniconda3-py38_${CONDAV}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
  && rm Miniconda3-py38_${CONDAV}-Linux-x86_64.sh \
  && $CONDA_DIR/bin/conda config --system --set auto_update_conda false \
  && $CONDA_DIR/bin/conda config --system --set show_channel_urls true \
  && $CONDA_DIR/bin/conda config --system --set auto_activate_base false \
  && $CONDA_DIR/bin/conda config --system --prepend channels conda-forge \
  && $CONDA_DIR/bin/conda config --system --set channel_priority strict \
  && $CONDA_DIR/bin/conda clean --all -f -y \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR
ENV PATH=$CONDA_DIR/bin:$PATH

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN conda create --name cocoa python=3.7 --quiet --yes \
  && conda install -n cocoa --quiet --yes  \
  'conda-forge::libgcc-ng=10.3.0' \
  'conda-forge::libstdcxx-ng=10.3.0' \
  'conda-forge::libgfortran-ng=10.3.0' \
  'conda-forge::gxx_linux-64=10.3.0' \
  'conda-forge::gcc_linux-64=10.3.0' \
  'conda-forge::gfortran_linux-64=10.3.0' \
  'conda-forge::openmpi=4.1.1' \
  'conda-forge::sysroot_linux-64=2.17' \
  'conda-forge::git=2.33.1' \
  'conda-forge::git-lfs=3.0.2' \
  'conda-forge::hdf5=1.10.6' \
  'conda-forge::git-lfs=3.0.2' \
  'conda-forge::cmake=3.21.3' \
  'conda-forge::boost=1.76.0' \
  'conda-forge::gsl=2.7' \
  'conda-forge::fftw=3.3.10' \
  'conda-forge::cfitsio=4.0.0' \
  'conda-forge::openblas=0.3.18' \
  'conda-forge::lapack=3.9.0' \
  'conda-forge::armadillo=10.7.3'\
  'conda-forge::expat=2.4.1' \
  'conda-forge::cython=0.29.24' \
  'conda-forge::numpy=1.21.4' \
  'conda-forge::scipy=1.7.2' \
  'conda-forge::pandas=1.3.4' \
  'conda-forge::mpi4py=3.1.2' \
  'conda-forge::matplotlib=3.5.0' \
  'conda-forge::astropy=4.3.1' \
  && conda run -n cocoa /opt/conda/envs/cocoa/bin/pip install --no-cache-dir --root-user-action=ignore \
    'tensorflow-cpu==2.8.0' \
    'keras==2.8.0' \
    'keras-preprocessing==1.1.2' \
    'torch==1.11.0+cpu' \ 
    'torchvision==0.12.0+cpu' -f https://download.pytorch.org/whl/torch_stable.html \
  && conda clean --all -f -y \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && rm -rf /opt/conda/share/man/* \
  && rm -rf /opt/conda/envs/cocoa/man/* \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# cocoa
RUN cd ~/ \
    && conda run -n cocoa --no-capture-output $CONDA_PREFIX/bin/git-lfs install \
    && conda run -n cocoa --no-capture-output $CONDA_PREFIX/bin/git-lfs clone https://github.com/CosmoLike/cocoa.git \
    && /usr/local/bin/fix-permissions $HOME/cocoa 

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# Native Cosmolike
RUN mkdir ~/cosmolike \
    && cd ~/cosmolike \
    && git clone https://github.com/CosmoLike/cosmolike_core.git \
    && /usr/local/bin/fix-permissions $HOME/cosmolike 
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
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