FROM nvidia/cuda:12.0.1-cudnn8-devel-ubuntu22.04

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
    git autoconf dpkg git-lfs xz-utils pkg-config python3-pip python3-pip \
  && apt-get install -yq --fix-missing --no-install-recommends libgflags-dev \
    libhdf5-dev libarpack2-dev nano make wget curl \
    libgtk2.0-dev libglib2.0-0 libfreetype6-dev libleveldb-dev \
    sqlite3 libv4l-dev fonts-liberation tzdata unzip grep libsnappy-dev \
    sed libsqlite3-dev sudo locales fonts-dejavu libgoogle-glog-dev  \
    texlive-xetex texlive-fonts-recommended texlive-plain-generic libx264-dev \
    libtool automake zlib1g-dev libcurl4-gnutls-dev ca-certificates libssl-dev \
    libtiff5-dev libpng-dev run-one ffmpeg gcc-10 gfortran-10 g++-10 gcc-9 gfortran-9 g++-9 \
    gcc-11 gfortran-11 g++-11 gcc-12 gfortran-12 g++-12 emacs sed vim \
    libjpeg-dev libtbb-dev dvipng libavcodec-dev libeigen3-dev \
    libjpeg8-dev libavformat-dev libswscale-dev ca-certificates-java \
    "openjdk-11-jre-headless" libatlas-base-dev libgtk-3-dev libxvidcore-dev \
# ------------------------------------------------------------------------
  && ln -s /bin/tar /bin/gtar \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen
# ------------------------------------------------------------------------
RUN  update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 12 \
  && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 12 \
  && update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-12 12 \
  && update-alternatives --set gcc /usr/bin/gcc-12 \
  && update-alternatives --set g++ /usr/bin/g++-12 \
  && update-alternatives --set gfortran /usr/bin/gfortran-12 
# ------------------------------------------------------------------------
RUN python3 -m pip install pip --upgrade --quiet --no-cache-dir \
  && pip3 install numpy==1.24.0 --quiet --no-cache-dir 
# ------------------------------------------------------------------------
RUN curl -L "https://github.com/krallin/tini/releases/download/v0.19.0/tini_0.19.0.deb" > tini.deb \
  && dpkg -i tini.deb \
  && rm tini.deb 
# --------------------------------------------------------------------------
# Install OpenSSH for MPI to communicate between containers
RUN apt-get update \
  && apt-get install -y --no-install-recommends openssh-client openssh-server \
  && mkdir -p /var/run/sshd 
# --------------------------------------------------------------------------
# Allow OpenSSH to talk to containers without asking for confirmation
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new \
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
    MAKE_NUM_THREADS=4

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
# INSTALL CORE RESEARCH LIBRARIES FROM SOURCE

RUN git clone  https://github.com/Kitware/CMake.git \
  && cd ./CMake \
  && git checkout v3.16.0 \
  && ./bootstrap \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf CMake 
#--------------------------------------------------------------------
RUN curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" \
  && unzip protoc-3.0.0-linux-x86_64.zip -d proto3 \
  && mv proto3/bin/* /usr/local/bin \
  && mv proto3/include/* /usr/local/include \
  && rm -rf proto3 protoc-3.0.0-linux-x86_64.zip 
#--------------------------------------------------------------------
ENV OPENMPI_VERSION=4.0.7

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
#--------------------------------------------------------------------
RUN git clone https://github.com/xianyi/OpenBLAS.git \
  && cd OpenBLAS \
  && git checkout v0.3.21 \
  && make -j $MAKE_NUM_THREADS USE_OPENMP=1 all \
  && make install PREFIX=/usr/local \
  && cd ../ \
  && rm -rf OpenBLAS/ 
#--------------------------------------------------------------------
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
#--------------------------------------------------------------------
RUN wget -q http://ftp.wayne.edu/gnu/gsl/gsl-2.7.tar.gz \
  && tar zxvf gsl-2.7.tar.gz \
  && rm -f gsl-2.7.tar.gz \
  && cd gsl-2.7 \
  && ./configure --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf gsl-2.7/ 
#--------------------------------------------------------------------
RUN wget -q http://www.fftw.org/fftw-3.3.10.tar.gz \
  && tar zxvf fftw-3.3.10.tar.gz \
  && rm -f fftw-3.3.10.tar.gz \
  && cd fftw-3.3.10/ \
  && ./configure --enable-openmp --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf fftw-3.3.10/ 
#--------------------------------------------------------------------
RUN wget -q http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-4.2.0.tar.gz \
  && tar zxvf cfitsio-4.2.0.tar.gz \
  && rm -f cfitsio-4.2.0.tar.gz \
  && cd cfitsio-4.2.0/ \
   && mkdir build \
  && cd build \
  && cmake -DBUILD_SHARED_LIBS=TRUE --log-level=ERROR .. \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf cfitsio-4.2.0/ 
#--------------------------------------------------------------------
RUN wget -q https://sourceforge.net/projects/arma/files/armadillo-12.0.1.tar.xz \
  && tar xvf armadillo-12.0.1.tar.xz\
  && rm -f armadillo-12.0.1.tar.xz \
  && cd armadillo-12.0.1/ \
  && cmake -DBUILD_SHARED_LIBS=TRUE --log-level=ERROR . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf armadillo-12.0.1/
#--------------------------------------------------------------------
RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.81.0/source/boost_1_81_0.tar.gz \
  && tar zxvf boost_1_81_0.tar.gz \
  && rm boost_1_81_0.tar.gz \
  && cd boost_1_81_0 \
  && ./bootstrap.sh \
  && ./b2  --with-regex install \
  && cd ../ \
  && rm -rf boost_1_81_0 \
#--------------------------------------------------------------------
  && ldconfig 
#--------------------------------------------------------------------
RUN git clone https://github.com/AcademySoftwareFoundation/openexr.git \
  && cd ./openexr \
  && git checkout v3.1.6 \
  && cmake . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf openexr/ 
#--------------------------------------------------------------------
RUN git clone https://github.com/apache/xerces-c.git \
  && cd ./xerces-c \
  && git checkout v3.2.4 \
  && cmake . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf ./xerces-c 
#--------------------------------------------------------------------
RUN git clone https://github.com/libigl/eigen.git \
  && mkdir eigein_build_dir \
  && cd eigein_build_dir \
  && cmake ../eigen \
  && make install \
  && cd ../ \
  && rm -rf eigein_build_dir \
  && rm -rf eigen \
#--------------------------------------------------------------------
  && ldconfig
#--------------------------------------------------------------------