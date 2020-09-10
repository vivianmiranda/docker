FROM vivianmiranda/whovian-base-base

RUN git clone git://github.com/opencv/opencv.git /opencv \
  && git clone git://github.com/opencv/opencv_contrib.git \
  && cd /opencv \
  && git checkout 4.4.0 \
  && mkdir ./build \
  && cd ./build \
  && cmake -DCMAKE_BUILD_TYPE=RELEASE \
     -DOPENCV_EXTRA_MODULES_PATH=/opencv_contrib/modules \
     -DPYTHON_EXECUTABLE=/usr/bin/python3.7/ \
     -DOPENCV_ENABLE_NONFREE=ON \
     -DBUILD_TIFF=OFF \
     -DBUILD_TESTS=ON  \
     -DOPENCV_GENERATE_PKGCONFIG=YES \
     -DWITH_CUDA=ON \
     -DWITH_CUDNN=ON \
     -DENABLE_FAST_MATH=ON \
     -DCUDA_FAST_MATH=ON \
     -DFORCE_VTK=ON \
     -DWITH_EIGEN=ON \
     -DWITH_FFMPEG=ON \
     -DWITH_GTK=OFF \
     -DWITH_JPEG=ON \
     -DWITH_PNG=ON \
     -DWITH_TBB=ON \
     -DBUILD_EXAMPLES=ON \
     -DWITH_GDAL=OFF \
     -DWITH_JAVA=OFF \
     -DINSTALL_C_EXAMPLES=ON \
     -DINSTALL_PYTHON_EXAMPLES=ON \
     -DCMAKE_C_COMPILER=gcc-7 \
     -DCMAKE_CXX_COMPILER=g++-7 .. \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../../ \
  && rm -rf /opencv \
  && rm -rf /opencv_contrib \
  && ldconfig \
  && /usr/local/bin/fix-permissions $HOME \
#--------------------------------------------------------------------
# INSTALL GOSU
  && dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')" \
  && curl -sSL "https://github.com/tianon/gosu/releases/download/${GOSU_VERSION}/gosu-${dpkgArch}" > /usr/bin/gosu \
  && chmod 755 /usr/bin/gosu \
  && gosu nobody true \
#--------------------------------------------------------------------
# INSTALL wait-for-it.sh
  && curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh > /usr/bin/wait-for-it.sh \
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

RUN wget --quiet \
https://repo.continuum.io/miniconda/Miniconda3-py37_${CONDAV}-Linux-x86_64.sh \
  && /bin/bash Miniconda3-py37_${CONDAV}-Linux-x86_64.sh -f -b -p $CONDA_DIR \
  && rm Miniconda3-py37_${CONDAV}-Linux-x86_64.sh \
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