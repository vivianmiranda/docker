FROM vivianmiranda/whovian-base-base:v3.0

#--------------------------------------------------------------------
# Install OpenCV 
#--------------------------------------------------------------------

RUN git clone https://github.com/opencv/opencv.git \
  && cd ./opencv \
  && git checkout 4.7.0 \
  && mkdir ./build \
  && cd ./build \
  && git clone https://github.com/opencv/opencv_contrib.git \
  && cmake -DCMAKE_BUILD_TYPE=RELEASE \
     -DOPENCV_EXTRA_MODULES_PATH=./opencv_contrib/modules \
     -DPYTHON_EXECUTABLE=/usr/bin/python3.8/ \
     -DBUILD_TIFF=OFF \
     -DBUILD_TESTS=OFF \
     -DBUILD_opencv_python2=OFF \ 
     -DBUILD_opencv_python3=ON \
     -DBUILD_EXAMPLES=OFF \
     -DOPENCV_ENABLE_NONFREE=ON \
     -DOPENCV_GENERATE_PKGCONFIG=YES \
     -DENABLE_FAST_MATH=ON \
     -DCUDA_FAST_MATH=ON \
     -DOPENCV_DNN_CUDA=OFF \
     -DWITH_CUBLAS=OFF \
     -DFORCE_VTK=ON \
     -DWITH_CUDA=ON \
     -DWITH_CUDNN=ON \
     -DWITH_EIGEN=ON \
     -DWITH_FFMPEG=ON \
     -DWITH_GTK=OFF \
     -DWITH_JPEG=ON \
     -DWITH_PNG=ON \
     -DWITH_TBB=OFF \
     -DWITH_GDAL=OFF \
     -DWITH_JAVA=OFF \
     -DINSTALL_C_EXAMPLES=OFF \
     -DINSTALL_PYTHON_EXAMPLES=OFF \
     -DCMAKE_C_COMPILER=gcc-9 \
     -DCMAKE_CXX_COMPILER=g++-9 .. \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../../ \
  && rm -rf /opencv \
  && ldconfig \
  && /usr/local/bin/fix-permissions $HOME 

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

ENV CONDAV=4.11.0

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
