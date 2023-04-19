FROM vivianmiranda/whovian-base:v4.0

#RUN  apt-get update \
#  && apt install -yq --fix-missing emacs sed vim man-db manpages-posix

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# PIP - HOME PYTHON
RUN pip install --upgrade --no-cache-dir pip setuptools wheel \
    pip install --no-cache-dir \
    'python-config' \
    'numpy==1.24.1' \
    'python-dateutil==2.8.1' \
    'six==1.15.0' \
    'cython==0.29.32' \
    'protobuf==3.13.0' \
    'nodejs' \
    'kiwisolver==1.2.0' \
    'pyparsing==2.4.7' \
    'pillow==9.4.0' \
    'fuzzywuzzy==0.17.0' \
    'pyyaml==6.0' \
    'virtualenv==20.17.1' \
    'imageio==2.23.0' \ 
    'notebook==6.5.2' \
    'scipy==1.10.0' \
    'pandas==1.5.2' \
    'h5py==3.5.0' \
    'astropy==5.2' \
    'pybind11==2.10.3' \
    'tokenizers==0.8.1' \
    'numba==0.50.1' \
    'GetDist==1.3.2' \
    'requests==2.24.0' \
    'seaborn==0.10.1' \
    'emcee==3.1.1' \
    'iminuit==2.8.2' \
    'py-bobyqa==1.3' \
    'wget==3.2' \
    'matplotlib==3.6.2' \
    'mpi4py==3.1.2' \
    'tensorflow-gpu==2.11.0' \
    'keras==2.11.0' \
    'keras-preprocessing' \
    'torch' \
    'torchvision' \
  && /usr/local/bin/fix-permissions $HOME


# FMT formmating library C++20 (https://github.com/fmtlib/fmt)
RUN git clone https://github.com/fmtlib/fmt.git \ 
  && cd ./fmt \
  && git checkout 9.1.0 \
  && mkdir  build \
  && cd build \
  && cmake -DCMAKE_INSTALL_PREFIX=/usr/local .. \
  && make all \
  && make install \
  && cd ../../ \
  && rm -rf ./fmt

# spdlog
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

# gcc 13 install
RUN wget --content-disposition https://kayari.org/gcc-latest/gcc-latest.deb \
  &&  apt install ./gcc-latest_13.0.1-20230402git8f989fe879dd.deb \ 
  &&  rm -rf gcc-latest_13.0.1-20230402git8f989fe879dd.deb

#
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

RUN    cp /mdspan/include/experimental/mdarray /usr/local/include/ \
    && cp /mdspan/include/experimental/mdspan /usr/local/include/ \
    && cp -r /mdspan/include/experimental/__p0009_bits /usr/local/include/ \
    && cp -r /mdspan/include/experimental/__p1684_bits /usr/local/include/ \
    && cp -r /mdspan/include/experimental/__p2630_bits /usr/local/include/ \
    && rm -rf /mdspan/
    
RUN rm -rf /var/lib/apt/lists/*

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
COPY jupyter_notebook_config.py $HOME/.jupyter/jupyter_notebook_config.py
COPY bashrc $HOME/bash.bashrc

RUN chmod +x /usr/bin/tini \
  && chmod a+rwx $HOME/bash.bashrc \
  && mkdir -p $HOME/host/ && chmod -R a+rwx $HOME/host/ \
  && rm -rf ~/.cache/pip \
  && /usr/local/bin/fix-permissions $HOME

EXPOSE 8888

ENTRYPOINT ["tini", "-g", "--"]
CMD ["/bin/bash", "-c", "source $HOME/bash.bashrc; /bin/bash"]

USER $NB_UID
WORKDIR $HOME
VOLUME ["$HOME/host/"]

RUN /usr/local/bin/fix-permissions $HOME
