FROM nvidia/cuda:10.2-devel-ubuntu18.04

ARG NB_USER="whovian"
ARG NB_UID=1000
ARG NB_GID=1000

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get install -yq --fix-missing software-properties-common  \
    apt-utils build-essential \
  && add-apt-repository ppa:ubuntu-toolchain-r/test \
  && apt-get update \
  && apt-get install -yq --fix-missing --no-install-recommends gcc-7 \
    gfortran-7 g++-7 git autoconf dpkg git-lfs xz-utils pkg-config \
    python3.7-dev python3-pip python-pip python3.7-venv \
  && apt-get install -yq --fix-missing --no-install-recommends libgflags-dev \
    libhdf5-dev libarpack2-dev nano make wget curl \
    libgtk2.0-dev libglib2.0-0 libfreetype6-dev libleveldb-dev \
    sqlite3 libv4l-dev fonts-liberation tzdata unzip grep libsnappy-dev \
    sed libsqlite3-dev sudo locales fonts-dejavu libgoogle-glog-dev  \
    texlive-xetex texlive-fonts-recommended texlive-plain-generic libx264-dev \
    libtool automake zlib1g-dev libcurl4-gnutls-dev ca-certificates libssl-dev \
    libtiff5-dev libpng-dev run-one ffmpeg gcc-9 gfortran-9 g++-9 \
    #libprotobuf-dev protobuf-compiler libopenexr-dev \
    libjpeg-dev libtbb-dev dvipng libavcodec-dev libeigen3-dev \
    libjpeg8-dev libavformat-dev libswscale-dev ca-certificates-java \
    "openjdk-11-jre-headless" libatlas-base-dev libgtk-3-dev libxvidcore-dev \
# ------------------------------------------------------------------------
  && ln -s /bin/tar /bin/gtar \
  && echo "en_US.UTF-8 UTF-8" > /etc/locale.gen \
  && locale-gen \
# ------------------------------------------------------------------------
  && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.7 \
  && update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 9 \
  && update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 9 \
  && update-alternatives --install /usr/bin/gfortran gfortran /usr/bin/gfortran-9 9 \
  && update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 \
  && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 \
  && update-alternatives --set gcc /usr/bin/gcc-9 \
  && update-alternatives --set g++ /usr/bin/g++-9 \
  && update-alternatives --set gfortran /usr/bin/gfortran-9 \
  && update-alternatives --set python /usr/bin/python3.7 \
  && update-alternatives --set python3 /usr/bin/python3.7 \
# ------------------------------------------------------------------------
  && python -m pip install pip --upgrade --quiet --no-cache-dir \
  && pip install numpy==1.19.1 --quiet --no-cache-dir \
# ------------------------------------------------------------------------
  && TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` \
  && curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb \
  && dpkg -i tini.deb \
  && rm tini.deb \
# --------------------------------------------------------------------------
#  && curl -SL https://github.com/llvm/llvm-project/releases/download/llvmorg-10.0.0/clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04.tar.xz | tar -xJC . \
#  && mv clang+llvm-10.0.0-x86_64-linux-gnu-ubuntu-18.04 clang_10.0.0 \
#  && echo 'export PATH=/clang_10.0.0/bin:$PATH' >> ~/.bashrc \
#  && echo 'export LD_LIBRARY_PATH=/clang_10.0.0/lib:$LD_LIBRARY_PATH' >> ~/.bashrc \
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
    CONDAV=4.8.3 \
    GOSU_VERSION=1.12 \
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

ENV OPENMPI_VERSION=4.0.5

RUN git clone  https://github.com/Kitware/CMake.git \
  && cd ./CMake \
  && git checkout v3.16.0 \
  && ./bootstrap \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf CMake \
#--------------------------------------------------------------------
  && curl -OL "https://github.com/google/protobuf/releases/download/v3.0.0/protoc-3.0.0-linux-x86_64.zip" \
  && unzip protoc-3.0.0-linux-x86_64.zip -d proto3 \
  && mv proto3/bin/* /usr/local/bin \
  && mv proto3/include/* /usr/local/include \
  && rm -rf proto3 protoc-3.0.0-linux-x86_64.zip \
#--------------------------------------------------------------------
  && wget --no-check-certificate https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-${OPENMPI_VERSION}.tar.gz \
  && tar xvzf openmpi-${OPENMPI_VERSION}.tar.gz \
  && rm -rf openmpi-${OPENMPI_VERSION}.tar.gz \
  && cd openmpi-${OPENMPI_VERSION} \
  && CFLAGS=-O3 CXXFLAGS=-O3 ./configure --prefix=/usr \
    --enable-orterun-prefix-by-default --enable-wrapper-rpath \
  && make -j $MAKE_NUM_THREADS all \
  && make install \
  && cd ../ \
  && rm -rf openmpi-${OPENMPI_VERSION} \
#--------------------------------------------------------------------
  && git clone https://github.com/xianyi/OpenBLAS.git \
  && cd OpenBLAS \
  && make -j $MAKE_NUM_THREADS USE_OPENMP=1 all \
  && make install PREFIX=/usr/local \
  && cd ../ \
  && rm -rf OpenBLAS/ \
#--------------------------------------------------------------------
  && wget http://www.netlib.org/lapack/lapack-3.9.0.tgz \
  && tar xvzf lapack-3.9.0.tgz \
  && rm lapack-3.9.0.tgz \
  && cd lapack-3.9.0 \
  && mkdir build \
  && cd build \
  && cmake -DBUILD_SHARED_LIBS=TRUE --prefix=/usr/local --log-level=ERROR .. \
  && make -j $MAKE_NUM_THREADS all \
  && make install \
  && cd ../../ \
  && rm -rf lapack-3.9.0/ \
#--------------------------------------------------------------------
  && wget -q http://ftp.wayne.edu/gnu/gsl/gsl-2.6.tar.gz \
  && tar zxvf gsl-2.6.tar.gz \
  && rm -f gsl-2.6.tar.gz \
  && cd gsl-2.6 \
  && ./configure --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf gsl-2.6/ \
#--------------------------------------------------------------------
  && wget -q http://www.fftw.org/fftw-3.3.8.tar.gz \
  && tar zxvf fftw-3.3.8.tar.gz \
  && rm -f fftw-3.3.8.tar.gz \
  && cd fftw-3.3.8/ \
  && ./configure --enable-openmp --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf fftw-3.3.8/ \
#--------------------------------------------------------------------
  && wget -q http://heasarc.gsfc.nasa.gov/FTP/software/fitsio/c/cfitsio-3.49.tar.gz \
  && tar zxvf cfitsio-3.49.tar.gz \
  && rm -f cfitsio-3.49.tar.gz \
  && cd cfitsio-3.49/ \
  && cmake -DBUILD_SHARED_LIBS=TRUE --log-level=ERROR . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf cfitsio-3.49/ \
#--------------------------------------------------------------------
  && wget -q https://sourceforge.net/projects/arma/files/armadillo-9.200.7.tar.xz \
  && tar xvf armadillo-9.200.7.tar.xz \
  && rm -f armadillo-9.200.7.tar.xz \
  && cd armadillo-9.200.7/ \
  && cmake -DBUILD_SHARED_LIBS=TRUE --log-level=ERROR . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf armadillo-9.200.7/
#--------------------------------------------------------------------

RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.74.0/source/boost_1_74_0.tar.gz \
  && tar zxvf boost_1_74_0.tar.gz \
  && rm boost_1_74_0.tar.gz \
  && cd boost_1_74_0 \
  && ./bootstrap.sh \
  && ./b2  --with-regex install \
  && cd ../ \
  && rm -rf boost_1_74_0 \
#--------------------------------------------------------------------
  && ldconfig \
#--------------------------------------------------------------------
  && git clone git://github.com/AcademySoftwareFoundation/openexr.git \
  && cd ./openexr \
  && git checkout v2.5.2 \
  && cmake . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf openexr/ \
#--------------------------------------------------------------------
  && git clone git://github.com/apache/xerces-c.git \
  && cd ./xerces-c \
  && git checkout v3.2.3 \
  && cmake . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf ./xerces-c \
#--------------------------------------------------------------------
  && git clone git://github.com/libigl/eigen.git \
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
