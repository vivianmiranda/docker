FROM nvidia/cuda:13.0.1-cudnn-devel-ubuntu24.04

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update \
  && apt-get install -yq --fix-missing software-properties-common apt-utils build-essential \
  && add-apt-repository -y universe \
  && add-apt-repository -y multiverse \
  && apt-get update \
  && apt-get install -yq --fix-missing --no-install-recommends libstdc++-14-dev \
    git autoconf dpkg git-lfs xz-utils pkg-config libgflags-dev python3  \
    libhdf5-dev libarpack2-dev nano make wget curl libleveldb-dev python3-dev \
    sqlite3 libv4l-dev fonts-liberation tzdata unzip grep libsnappy-dev python3-pip \
    sed libsqlite3-dev sudo locales fonts-dejavu libgoogle-glog-dev manpages less  \
    libx264-dev libtool automake zlib1g-dev libcurl4-gnutls-dev g++ gfortran manpages-dev \
    emacs vim man-db manpages-posix unminimize cmake cm-super ghostscript dvipng zip tar libtbb-dev \
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
  && apt-get autoremove --yes

RUN set +o pipefail \
    && yes | unminimize \
    && set -o pipefail \
    && mandb -q \
    && apt-get clean \
    && apt-get autoremove --yes \
    && rm -rf /var/lib/apt/lists/*

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
RUN git clone --depth 1 --branch v0.3.33 https://github.com/xianyi/OpenBLAS.git \
  && cd OpenBLAS \
  && make -j $MAKE_NUM_THREADS USE_OPENMP=1 all \
  && make install PREFIX=/usr/local \
  && cd ../ \
  && rm -rf OpenBLAS/ 
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN wget -q http://www.fftw.org/fftw-3.3.11.tar.gz \
  && tar zxvf fftw-3.3.11.tar.gz \
  && rm -f fftw-3.3.11.tar.gz \
  && cd fftw-3.3.11/ \
  && ./configure --enable-openmp --enable-shared=yes --enable-static=yes \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf fftw-3.3.11/ 
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN wget -q -O armadillo-15.2.7.tar.xz 'https://sourceforge.net/projects/arma/files/armadillo-15.2.7.tar.xz/download' \
  && tar xvf armadillo-15.2.7.tar.xz \
  && rm -f armadillo-15.2.7.tar.xz \
  && cd armadillo-15.2.7/ \
  && cmake -DBUILD_SHARED_LIBS=TRUE --log-level=ERROR . \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf armadillo-15.2.7/ 
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN git clone --branch v0.6.1 https://github.com/RUrlus/carma.git \
  && cp -r carma/include/carma /usr/local/include/ \
  && rm -rf carma
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
# DOWNLOAD EXPERIMENTAL GCC SNAPSHOT (GCC16)

RUN apt-get update \
  && wget --content-disposition https://kayari.org/gcc-latest/gcc-latest.deb \
  && apt install -y ./gcc-latest*.deb \ 
  && rm -f gcc-latest*.deb \
  && rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN wget https://archives.boost.io/release/1.87.0/source/boost_1_87_0.tar.gz \
  && tar zxvf boost_1_87_0.tar.gz \
  && rm boost_1_87_0.tar.gz \
  && cd boost_1_87_0 \
  && ./bootstrap.sh --with-libraries=regex \
  && ./b2 link=shared --with-regex -j$MAKE_NUM_THREADS install \
  && cd ../ \
  && rm -rf boost_1_87_0 \
  && ldconfig

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# FMT formmating library C++20 (https://github.com/fmtlib/fmt)
RUN git clone --branch 12.1.0 https://github.com/fmtlib/fmt.git \ 
  && cd ./fmt \
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
RUN git clone --branch v1.17.0 https://github.com/gabime/spdlog.git \
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


# ------------------------------------------------------------------
# ------------------------------------------------------------------
# ------------------------------------------------------------------
ENV VCPKG_DIR /usr/local/
RUN git clone https://github.com/Microsoft/vcpkg.git \
    && cd vcpkg \
    && git checkout 2026.01.16 \
    && ./bootstrap-vcpkg.sh \
    && ./vcpkg integrate install \
    && ./vcpkg install range-v3 --clean-after-build \
    && rm -rf buildtrees packages downloads \
    && cd ../ \
    && rm -rf /usr/local/vcpkg/.git \
              /usr/local/vcpkg/downloads \
              /usr/local/vcpkg/buildtrees \
              /usr/local/vcpkg/packages 
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN git clone --branch v3.12.0 https://github.com/catchorg/Catch2 \
  && cd Catch2 \ 
  && mkdir build \
  && cd build \
  && cmake .. \
  && make \
  && make install \
  && cd ../../ \
  && rm -rf Catch2

RUN git clone --branch v0.7.0 https://github.com/contour-terminal/libunicode/ \
    && cd libunicode \
    && cmake -B build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build \
    && cmake --install build \
    && cd .. \
    && rm -rf libunicode
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
RUN git clone --branch v3.0.4 https://github.com/pybind/pybind11.git \
    && cd pybind11 \
    && cmake -B build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build \
    && cmake --install build \
    && cd .. \
    && rm -rf pybind11
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
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
    'tensorflow==2.21.0' \
    'tensorflow_probability==0.25.0' \
    'keras==3.12.1' \
    'keras-preprocessing==1.1.2' \
    'torch==2.11.0' \
    'torchvision==0.26.0' \
    'torchaudio==2.11.0' \
    'scikit-learn==1.7.2' \
    'jupyter>=1.1' \
    'typing-extensions==4.13.2' \
    'mkdocs_material==9.6.13' \
    'mkdocstrings==0.29.1' \
    'pytest==8.3.5' \
    'tf-keras==2.21.0' \
    'jax==0.4.30' \
    'jaxlib==0.4.30' \
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
    --extra-index-url "https://download.pytorch.org/whl/cu130" \
    -f https://storage.googleapis.com/jax-releases/jax_releases.html 

# Critical: let whovian modify the venv later
RUN chown -R $NB_UID:$NB_GID /opt/venv \
  && chmod -R u+rwX,g+rwX /opt/venv
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

EXPOSE 8888

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/bin/bash", "-c", "source $HOME/bash.bashrc; /bin/bash"]

USER $NB_UID
WORKDIR $HOME
VOLUME ["$HOME/host/"]

# REMIND HOW TO BUILD THIS FILE
# docker build . -f Dockerfile
# docker image ls
# docker tag 143f15f6f0e6 vivianmiranda/whovian-cosmo2026
# docker push vivianmiranda/whovian-cosmo2026
# How to run?
# docker run --platform linux/amd64 --hostname cosmo2026 --name cosmo2026 -it -p 8888:8888 -v "$(pwd)":/home/whovian/host/ -v ~/.ssh:/home/whovian/.ssh:ro vivianmiranda/whovian-cosmo2026
