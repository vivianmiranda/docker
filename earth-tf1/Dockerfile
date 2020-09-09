FROM vivianmiranda/whovian-base

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# SET CONDA ENV EARTH-TF1

ENV TIFF_CFLAGS="-I/opt/conda/envs/earth-tf1/include" \
    TIFF_LIBS="-L/opt/conda/envs/earth-tf1/lib -ltiff" \
    GDAL_DATA=/opt/conda/envs/earth-tf1/share/gdal \
    GDAL_CONFIG=/opt/conda/envs/earth-tf1/bin/gdal-config \
    OLDPATH=$PATH \
    PATH=/opt/conda/envs/earth-tf1/bin:$PATH \
    OLD_LD_LIB_PATH=$LD_LIBRARY_PATH \
    LD_LIBRARY_PATH=/opt/conda/envs/earth-tf1/libs:$LD_LIBRARY_PATH

RUN conda create --name earth-tf1 python=3.7 --quiet --yes \
  && conda install -n earth-tf1 --quiet --yes \
    'conda-forge::libgcc-ng=9.3.0' \
    'conda-forge::libstdcxx-ng=9.3.0' \
    'conda-forge::gcc_linux-64=9.3.0' \
    'conda-forge::gxx_linux-64=9.3.0' \
    'conda-forge::freeimage=3.18.0' \
    'conda-forge::libtiff=4.1.0' \
    'conda-forge::python-dateutil=2.8.1' \
    'conda-forge::readline=8.0' \
    'conda-forge::six=1.15.0' \
    'conda-forge::numpy=1.19.1' \
    'conda-forge::cython=0.29.21' \
    'conda-forge::tini=0.18.0' \
    'conda-forge::protobuf=3.13.0' \
    'conda-forge::nodejs' \
    'conda-forge::libpng=1.6.37' \
    'conda-forge::kiwisolver=1.2.0' \
    'conda-forge::pyparsing=2.4.7' \
    'conda-forge::pillow=7.2.0' \
    'conda-forge::fuzzywuzzy=0.17.0' \
    'conda-forge::pyyaml=5.3.1' \
    'conda-forge::virtualenv=20.0.20' \
    'conda-forge::imageio=2.9.0' \
    'conda-forge::notebook=6.1.1' \
    'conda-forge::jpeg=9d'\
    'conda-forge::openjpeg=2.3.1'\
    'conda-forge::giflib=5.2.1' \
    'conda-forge::matplotlib=3.3.1' \
    'conda-forge::imutils=0.5.3' \
#--------------------------------------------------------------------
# NUMERICAL WORK
    'conda-forge::numba=0.50.1' \
    'conda-forge::scipy=1.4.1' \
    'conda-forge::pandas=1.1.1' \
    'conda-forge::hdf5=1.10.6' \
    'conda-forge::h5py=2.10.0' \
#--------------------------------------------------------------------
# MachineLearning
    'conda-forge::scikit-image=0.16.2' \
    'conda-forge::scikit-learn=0.23.2' \
  && conda clean --all -f -y \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR

#--------------------------------------------------------------------
# EARTH
RUN conda install -n earth-tf1 --quiet --yes \
    'conda-forge::geojson=2.5.0' \
    'conda-forge::muparser=2.3.2' \
    'conda-forge::gmp=6.2.0' \
    'conda-forge::mpfr=4.0.2' \
    'conda-forge::cgal=4.14' \
    'conda-forge::openexr=2.5.2' \
    'conda-forge::xerces-c=3.2.3' \
    'conda-forge::expat=2.2.9' \
    'conda-forge::libwebp=1.1.0' \
    'conda-forge::libkml=1.3.0' \
    'conda-forge::geotiff=1.6.0' \
  && conda clean --all -f -y \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR

#--------------------------------------------------------------------
# PIP
RUN /opt/conda/envs/earth-tf1/bin/pip install --quiet --no-cache-dir \
    'tensorflow-gpu==1.15.0' \
    'keras==2.3.1' \
    'keras-preprocessing' \
    'pyfits==3.5' \
    'seaborn==0.10.1' \
    'mpi4py==3.0.3' \
    'pyarrow==1.0.1' \
#--------------------------------------------------------------------
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR

#--------------------------------------------------------------------
# EARTH
RUN wget https://download.osgeo.org/proj/proj-7.1.0.tar.gz \
  && tar -xzf proj-7.1.0.tar.gz \
  && rm -f proj-7.1.0.tar.gz \
  && cd ./proj-7.1.0 \
  && ./configure --prefix=/opt/conda/envs/earth-tf1 \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf proj-7.1.0/ \
#--------------------------------------------------------------------
  && git clone git://github.com/libgeos/geos.git \
  && cd ./geos \
  && git checkout 3.7.2 \
  && ./autogen.sh \
  && mkdir obj \
  && cd obj \
  && ../configure --prefix=/opt/conda/envs/earth-tf1 \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../../ \
  && rm -rf geos/ \
#--------------------------------------------------------------------
  && wget http://download.osgeo.org/gdal/3.1.2/gdal-3.1.2.tar.gz \
  && tar -xvzf gdal-3.1.2.tar.gz \
  && rm -f gdal-3.1.2.tar.gz \
  && cd gdal-3.1.2 \
  && ./configure --prefix=/opt/conda/envs/earth-tf1 --quiet \
    --with-cpp14 \
    --with-curl=/usr \
    --with-local=/opt/conda/envs/earth-tf1 \
    --with-cfitsio=/usr/local \
    --with-armadillo=/usr/local \
    --with-hdf5=/opt/conda/envs/earth-tf1 \
    --with-xerces=/opt/conda/envs/earth-tf1 \
    --with-png=/opt/conda/envs/earth-tf1 \
    --with-jpeg=/opt/conda/envs/earth-tf1 \
    --with-libtiff=/opt/conda/envs/earth-tf1 \
    --with-geotiff=/opt/conda/envs/earth-tf1 \
    --with-geos=/opt/conda/envs/earth-tf1 \
    --with-expat=/opt/conda/envs/earth-tf1 \
    --with-libkml=/opt/conda/envs/earth-tf1 \
    --with-gif=/opt/conda/envs/earth-tf1 \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf gdal-3.1.2/ \
#--------------------------------------------------------------------
  && wget https://github.com/libspatialindex/libspatialindex/releases/download/1.9.3/spatialindex-src-1.9.3.tar.gz \
  && tar zxvf spatialindex-src-1.9.3.tar.gz \
  && rm -f spatialindex-src-1.9.3.tar.gz \
  && cd ./spatialindex-src-1.9.3 \
  && cmake . -DCMAKE_INSTALL_PREFIX=/opt/conda/envs/earth-tf1/ \
  && make -j $MAKE_NUM_THREADS  \
  && make install \
  && cd ../ \
  && rm -rf ./spatialindex-src-1.9.3 \
#--------------------------------------------------------------------
  && git clone git://github.com/ubarsc/kealib.git \
  && cd ./kealib \
  && git checkout kealib-1.4.13 \
  && cmake . -DCMAKE_INSTALL_PREFIX=/opt/conda/envs/earth-tf1 \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf ./kealib \
#--------------------------------------------------------------------
  && ldconfig \
#--------------------------------------------------------------------
  && git clone git://github.com/pyproj4/pyproj.git \
  && cd ./pyproj \
  && git checkout v2.6.1rel \
  && PROJ_DIR=/opt/conda/envs/earth-tf1 /opt/conda/envs/earth-tf1/bin/python setup.py install \
  && cd ../ \
  && rm -rf pyproj \
#--------------------------------------------------------------------
  && git clone git://github.com/Toblerity/Fiona.git \
  && cd Fiona \
  && git checkout 1.8.13.post1 \
  && /opt/conda/envs/earth-tf1/bin/python setup.py build_ext \
    -I/opt/conda/envs/earth-tf1/include \
    -L/opt/conda/envs/earth-tf1/lib -lgdal \
  && /opt/conda/envs/earth-tf1/bin/python setup.py install \
  && cd ../ \
  && rm -rf ./Fiona \
#--------------------------------------------------------------------
  && GEOS_CONFIG=/opt/conda/envs/earth-tf1 \
    /opt/conda/envs/earth-tf1/bin/pip install \
    --quiet --no-cache-dir --no-binary :all: \
    dask \
    shapely \
    geopandas \
    rasterio \
  && /opt/conda/envs/earth-tf1/bin/pip install --quiet --no-cache-dir descartes \
#--------------------------------------------------------------------
  && /opt/conda/envs/earth-tf1/bin/pip install --global-option=build_ext \
    --global-option=build_ext --prefix=/opt/conda/envs/earth-tf1 \
    --global-option="-L /opt/conda/envs/earth-tf1/libs -I/opt/conda/envs/earth-tf1/include" \
    pygdal=="3.1.2.6" --no-binary :all: --quiet --no-cache-dir \
#--------------------------------------------------------------------
  && git clone git://github.com/remotesensinginfo/arcsi.git \
  && cd ./arcsi \
  && git checkout v3.8.1 \
  && /opt/conda/envs/earth-tf1/bin/python setup.py install \
  && cd ../ \
  && rm -rf arcsi \
#--------------------------------------------------------------------
  && git clone git://github.com/perrygeo/python-rasterstats.git \
  && cd python-rasterstats \
  && git checkout 0.15.0  \
  && /opt/conda/envs/earth-tf1/bin/python setup.py install \
  && cd ../ \
  && rm -rf python-rasterstats \
#--------------------------------------------------------------------
  && git clone git://github.com/GeospatialPython/pyshp.git \
  && cd pyshp \
  && git checkout 2.1.0   \
  && /opt/conda/envs/earth-tf1/bin/python setup.py install \
  && cd ../ \
  && rm -rf pyshp \
#--------------------------------------------------------------------
  && git clone git://github.com/scisco/area.git \
  && cd area \
  && git checkout v1.1.1    \
  && /opt/conda/envs/earth-tf1/bin/python setup.py install \
  && cd ../ \
  && rm -rf area \
#--------------------------------------------------------------------
  && git clone git://github.com/remotesensinginfo/rsgislib.git \
  && cd rsgislib \
  && cmake . -DCMAKE_INSTALL_PREFIX=/opt/conda/envs/earth-tf1/ \
    -DBOOST_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DBOOST_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DHDF5_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DHDF5_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DXERCESC_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DXERCESC_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DGEOS_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DGEOS_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DGDAL_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DGDAL_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DCGAL_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DCGAL_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DKEA_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DKEA_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DMPFR_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DMPFR_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
    -DMUPARSER_INCLUDE_DIR=/opt/conda/envs/earth-tf1/include \
    -DMUPARSER_LIB_PATH=/opt/conda/envs/earth-tf1/lib \
  && make -j $MAKE_NUM_THREADS \
  && make install \
  && cd ../ \
  && rm -rf ./rsgislib \
#--------------------------------------------------------------------
  && git clone git://github.com/descarteslabs/descarteslabs-python.git \
  && cd descarteslabs-python \
  && git checkout v1.4.0 \
  && /opt/conda/envs/earth-tf1/bin/python setup.py install \
  && cd ../ \
  && rm -rf descarteslabs-python \
#--------------------------------------------------------------------
  && conda clean --all -f -y \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR

#--------------------------------------------------------------------
# INSTALL DARKNET

ENV PKG-CFG=/usr/bin/pkg-config

RUN git clone git://github.com/pjreddie/darknet.git \
  && mv ./darknet/ /opt/conda/envs/earth-tf1/ \
  && cd /opt/conda/envs/earth-tf1/darknet \
  && git checkout 4a03d405982aa1e1e911eac42b0ffce29cc8c8ef
COPY darknet/Makefile ./
RUN cd /opt/conda/envs/earth-tf1/darknet \
  && make -j $MAKE_NUM_THREADS \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR

ENV PATH=$OLDPATH \
  LD_LIBRARY_PATH=$OLD_LD_LIB_PATH

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

COPY jupyter_notebook_config.py $HOME/.jupyter/jupyter_notebook_config.py
COPY bashrc $HOME/bash.bashrc

RUN chmod +x /usr/bin/tini \
  && chmod a+rwx $HOME/bash.bashrc \
  && mkdir -p $HOME/host/ && chmod -R a+rwx $HOME/host/ \
  && /usr/local/bin/fix-permissions $HOME \
  && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
  && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
  && rm -rf ~/.cache/pip \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR \
  && chown $NB_USER:$NB_GID $CONDA_DIR

EXPOSE 8888 6006
# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["/bin/bash", "-c", "source $HOME/bash.bashrc; /bin/bash"]

USER $NB_UID
WORKDIR $HOME
VOLUME ["$HOME/host/"]

RUN /usr/local/bin/fix-permissions $CONDA_DIR \
  && /usr/local/bin/fix-permissions $HOME