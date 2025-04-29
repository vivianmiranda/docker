FROM ubuntu:24.10

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get install -yq --fix-missing software-properties-common apt-utils build-essential \
  && apt-get update \
  && apt-get update \
  && apt-get install -yq --fix-missing --no-install-recommends \
    git autoconf dpkg git-lfs xz-utils pkg-config libgflags-dev \
    libhdf5-dev libarpack2-dev nano make wget curl libleveldb-dev \
    sqlite3 libv4l-dev fonts-liberation tzdata unzip grep libsnappy-dev \
    sed libsqlite3-dev sudo locales fonts-dejavu libgoogle-glog-dev  \
    libx264-dev libtool automake zlib1g-dev libcurl4-gnutls-dev g++ gfortran \
    emacs sed vim man-db manpages-posix cmake cm-super ghostscript dvipng \
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

ARG NB_USER="whovian"
ARG NB_UID=1005
ARG NB_GID=1005

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
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
    GOSU_VERSION=1.16

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
# Create NB_USER wtih name jovyan user with UID=1005 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su \
    && sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers \
    && sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers \
    && useradd -m -s /bin/bash -N -u $NB_UID $NB_USER \
    && groupmod -g 1005 users \
    && chmod g+w /etc/passwd 

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
ENV OPENMPI_VERSION=4.1.5
RUN wget --no-check-certificate https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-${OPENMPI_VERSION}.tar.gz \
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
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN wget -q http://ftp.wayne.edu/gnu/gsl/gsl-2.8.tar.gz \
  && tar zxvf gsl-2.8.tar.gz \
  && rm -f gsl-2.8.tar.gz \
  && cd gsl-2.8 \
  && ./configure --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf gsl-2.8/

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN wget -q https://sourceforge.net/projects/arma/files/armadillo-14.2.2.tar.xz \
  && tar xvf armadillo-14.2.2.tar.xz\
  && rm -f armadillo-14.2.2.tar.xz \
  && cd armadillo-14.2.2/ \
  && cmake -DBUILD_SHARED_LIBS=TRUE --log-level=ERROR . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf armadillo-14.2.2/

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN wget https://archives.boost.io/release/1.87.0/source/boost_1_87_0.tar.gz \
  && tar zxvf boost_1_87_0.tar.gz \
  && rm boost_1_87_0.tar.gz \
  && cd boost_1_87_0 \
  && ./bootstrap.sh \
  && ./b2  --with-regex install \
  && cd ../ \
  && rm -rf boost_1_87_0 \
#--------------------------------------------------------------------
  && ldconfig
#--------------------------------------------------------------------

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# FMT formmating library C++20 (https://github.com/fmtlib/fmt)
RUN git clone https://github.com/fmtlib/fmt.git \ 
  && cd ./fmt \
  && git checkout 11.0.2 \
  && mkdir  build \
  && cd build \
  && cmake -DCMAKE_INSTALL_PREFIX=/usr/local .. \
  && make all \
  && make install \
  && cd ../../ \
  && rm -rf ./fmt

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN git clone https://github.com/vivianmiranda/spdlog.git \
  && cd spdlog \
  && cd ../ \
  && cd spdlog \
  && mkdir  build \
  && cd build \
  && cmake \ 
    -DSPDLOG_NO_EXCEPTIONS=yes \
    -DCMAKE_INSTALL_PREFIX=/usr/local .. \
  && make all \
  && make install \ 
  && cd ../../ \
  && rm -rf ./spdlog

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN git clone https://github.com/kokkos/mdspan \
    && cd ./mdspan \
    && mkdir  build \
    && cd build  \
    && cmake \
    -DMDSPAN_ENABLE_TESTS=OFF \
    -DMDSPAN_ENABLE_BENCHMARKS=OFF \
    -DCMAKE_CXX_FLAGS="-Werror -Wall -Wextra -pedantic" \
    -DCMAKE_CXX_STANDARD=20 -DMDSPAN_CXX_STANDARD=20 \
    -DCMAKE_CXX_COMPILER=g++ \
    -DCMAKE_CXX_EXTENSIONS=OFF \
    -DCMAKE_INSTALL_PREFIX=/usr/local .. \
    && cd ../../ 

RUN cp /mdspan/include/experimental/mdarray /usr/local/include/ \
    && cp /mdspan/include/experimental/mdspan /usr/local/include/ \
    && cp -r /mdspan/include/experimental/__p0009_bits /usr/local/include/ \
    && cp -r /mdspan/include/experimental/__p1684_bits /usr/local/include/ \
    && cp -r /mdspan/include/experimental/__p2630_bits /usr/local/include/ \
    && rm -rf /mdspan/

# ------------------------------------------------------------------
# DOWNLOAD EXPERIMENTAL GCC SNAPSHOT (GCC15)
RUN wget --content-disposition https://kayari.org/gcc-latest/gcc-latest.deb \
    && apt install ./gcc-latest_15.0.1-20250406gitb39d5fad621c.deb \ 
    &&  rm -rf gcc-latest_15.0.1-20250406gitb39d5fad621c.deb

# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------
ENV VCPKG_DIR /usr/local/

RUN apt-get install -yq --fix-missing --no-install-recommends unzip

RUN git clone https://github.com/Microsoft/vcpkg.git \
    && cd vcpkg \
    && ./bootstrap-vcpkg.sh \
    && ./vcpkg integrate install \
    && ./vcpkg install range-v3 \
    && cd ../
  
RUN rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

RUN git clone https://github.com/catchorg/Catch2 \
  && cd Catch2 \ 
  && mkdir build \
  && cd build \
  && cmake .. \
  && make \
  && make install \
  && cd ../../ \
  && rm -rf Catch2

RUN git clone https://github.com/contour-terminal/libunicode/ \
    && cd libunicode \
    && cmake -B build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build \
    && cmake --install build \
    && cd .. \
    && rm -rf libunicode

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

RUN mkdir -p $HOME/.jupyter 

RUN /usr/local/bin/fix-permissions $HOME 
RUN /usr/local/bin/fix-permissions $HOME/.jupyter

RUN chown -R $NB_USER:$NB_GID $HOME
RUN chown -R $NB_USER:$NB_GID $HOME/.jupyter 

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

RUN apt-get update \
  && apt-get install -yq --fix-missing libtbb-dev \
  && apt-get clean \
  && apt-get autoremove --yes \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /usr/share/doc/ \
  && rm -rf /usr/share/man/

EXPOSE 8888

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/bin/bash", "-c", "source $HOME/bash.bashrc; /bin/bash"]

USER $NB_UID
WORKDIR $HOME
VOLUME ["$HOME/host/"]

# REMIND HOW TO BUILD THIS FILE
# docker build . -f Dockerfile
# docker image ls
# docker tag 143f15f6f0e6 vivianmiranda/whovian-phy504lite
# docker push vivianmiranda/whovian-phy504lite
# How to run?
# docker run --platform linux/amd64 --hostname whovianphy504 --name phy504_2025_v2 -it -p 8888:8888 -v $(pwd):/home/whovian/host/ -v ~/.ssh:/home/whovian/.ssh:ro vivianmiranda/whovian-phy504lite
