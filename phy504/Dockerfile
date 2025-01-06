FROM vivianmiranda/whovian-base-base

#--------------------------------------------------------------------
# INSTALL GOSU
ENV GOSU_VERSION=1.16 

RUN dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
  && curl -sSL "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-${dpkgArch}" > /usr/bin/gosu \
  && chmod 755 /usr/bin/gosu \
  && gosu nobody true 

#--------------------------------------------------------------------
# INSTALL wait-for-it.sh
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh > /usr/bin/wait-for-it.sh \
  && chmod 755 /usr/bin/wait-for-it.sh \
#--------------------------------------------------------------------
  && ldconfig

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
    && /usr/local/bin/fix-permissions $HOME \
    && /usr/local/bin/fix-permissions $CONDA_DIR

#--------------------------------------------------------------------
# INSTALL CONDA

ENV CONDAV=4.12.0

RUN wget --quiet \
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
# PIP 'HOME PYTHON
RUN pip install --upgrade --no-cache-dir pip setuptools wheel \
    pip install --no-cache-dir \
    'python-config' \
    'six==1.15.0' \
    'nodejs' \
    'notebook==6.5.2' \
    'seaborn==0.10.1' \
    'emcee==3.1.1' \
    'wget==3.2' \
    'mpi4py==3.1.4' \
    'notebook==7.1.1' \
    'ipyparallel==8.8.0' \
    'tensorflow-gpu==2.12.0' \
    'keras==2.12.0' \
    'keras-preprocessing==1.1.2' \
    'torch==1.13.1+cu116' \
    'torchvision' \
    'torchaudio==0.13.1' \
    'tensiometer==0.1.2' \
    'alabaster==0.7.13' \
    'anytree==2.8.0' \
    'appdirs==1.4.4' \
    'astropy==5.2.2' \
    'babel==2.12.1' \
    'cachetools==5.3.1' \
    'certifi==2023.5.7' \
    'charset-normalizer==3.1.0' \
    'configparser==5.3.0' \
    'contourpy==1.1.0' \
    'corner==2.2.1' \
    'coverage==7.5.4' \
    'cycler==0.11.0' \
    'cython==3.0.10' \
    'deprecated==1.2.14' \
    'dill==0.3.6' \
    'distlib==0.3.8' \
    'docutils==0.20.1' \
    'filelock==3.13.4' \
    'fonttools==4.40.0' \
    'fuzzywuzzy==0.18.0' \
    'getdist==1.4.8' \
    'gpy==1.10.0' \
    'h5py==3.8.0' \
    'idna==3.4' \
    'imageio==2.31.1' \
    'imagesize==1.4.1' \
    'iminuit==2.25.2' \
    'importlib-metadata==6.6.0' \
    'importlib-resources==5.12.0' \
    'jax==0.4.12' \
    'jinja2==3.1.2' \
    'joblib==1.4.0' \
    'johnnydep==1.20.2' \
    'kiwisolver==1.4.4' \
    'lazy-loader==0.2' \
    'lenstronomy==1.11.2' \
    'llvmlite==0.41.1' \
    'markupsafe==2.1.3' \
    'matplotlib==3.7.5' \
    'ml-dtypes==0.2.0' \
    'mpmath==1.3.0' \
    'multiprocess==0.70.14' \
    'networkx==3.1' \
    'numba==0.58.1' \
    'numpy==1.24.1' \
    'numpydoc==1.5.0' \
    'oauthlib==3.2.2' \
    'opt-einsum==3.3.0' \
    'oyaml==1.0' \
    'packaging==23.1' \
    'pandas==2.0.3' \
    'paramz==0.9.5' \
    'pgen==0.2.1' \
    'pillow==9.5.0' \
    'platformdirs==3.9.1' \
    'portalocker==2.7.0' \
    'protobuf==4.23.2' \
    'py-bobyqa==1.4' \
    'pybind11==2.12.0' \
    'pydoe2==1.3.0' \
    'pyerfa==2.0.0.3' \
    'pyfftw==0.13.1' \
    'pygments==2.17.2' \
    'pyparsing==3.0.9' \
    'python-dateutil==2.8.2' \
    'pytz==2023.3' \
    'pywavelets==1.4.1' \
    'pyxdg==0.28' \
    'pyyaml==6.0' \
    'qp-prob==0.8.3' \
    'requests==2.31.0' \
    'sacc==0.8.1' \
    'schwimmbad==0.3.2' \
    'scikit-image==0.21.0' \
    'scikit-learn==1.2.2' \
    'scipy==1.10.1' \
    'setuptools==67.7.2' \
    'setuptools-scm==7.1.0' \
    'snowballstemmer==2.2.0' \
    'sphinx==7.1.2' \
    'sphinxcontrib-applehelp==1.0.4' \
    'sphinxcontrib-devhelp==1.0.2' \
    'sphinxcontrib-htmlhelp==2.0.1' \
    'sphinxcontrib-jsmath==1.0.1' \
    'sphinxcontrib-qthelp==1.0.3' \
    'sphinxcontrib-serializinghtml==1.1.5' \
    'structlog==23.1.0' \
    'sympy==1.12' \
    'tables-io==0.8.1' \
    'tabulate==0.9.0' \
    'threadpoolctl==3.1.0' \
    'tifffile==2023.4.12' \
    'tokenizers==0.13.3' \
    'toml==0.10.2' \
    'tqdm==4.65.0' \
    'typing-extensions==4.6.3' \
    'tzdata==2023.3' \
    'urllib3==1.26.16' \
    'virtualenv==20.26.0' \
    'wheel==0.40.0' \
    'wimpy==0.6' \
    'wrapt==1.14.1' \
    'zipfile38==0.0.3' \
    'zipp==3.15.0
  && /usr/local/bin/fix-permissions $HOME

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# gcc 15 install
#RUN wget --content-disposition https://kayari.org/gcc-latest/gcc-latest_15.0.0-20250105gitf5351b38a8af.deb \
#  &&  apt install ./gcc-latest_15.0.0-20250105gitf5351b38a8af.deb \ 
#  &&  rm -rf gcc-latest_15.0.0-20250105gitf5351b38a8af.deb

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

# FMT formmating library C++20 (https://github.com/fmtlib/fmt)
RUN git clone https://github.com/fmtlib/fmt.git \ 
  && cd ./fmt \
  && git checkout 11.1.1 \
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
