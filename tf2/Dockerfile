FROM vivianmiranda/whovian-base

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# SET CONDA ENV TF2

ENV OLDPATH=$PATH \
    PATH=/opt/conda/envs/tf2/bin:$PATH \
    OLD_LD_LIB_PATH=$LD_LIBRARY_PATH \
    LD_LIBRARY_PATH=/opt/conda/envs/tf2/libs:$LD_LIBRARY_PATH

RUN conda create --name tf2 python=3.7 --quiet --yes \
  && conda install -n tf2 --quiet --yes \
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
    'conda-forge::giflib=5.2.1' \
    'conda-forge::openjpeg=2.3.1'\
    'conda-forge::jpeg=9d'\
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
#--------------------------------------------------------------------
  && /opt/conda/envs/tf2/bin/pip install --quiet --no-cache-dir \
    'tensorflow-gpu==2.2.0' \
    'keras==2.4.3' \
    'keras-preprocessing==1.1.0' \
    'pyfits==3.5' \
    'seaborn==0.10.1'  \
    'mpi4py==3.0.3' \
#--------------------------------------------------------------------
  && conda clean --all -f -y \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR

#--------------------------------------------------------------------
# INSTALL DARKNET

ENV PKG-CFG=/usr/bin/pkg-config

RUN git clone git://github.com/pjreddie/darknet.git \
  && mv ./darknet/ /opt/conda/envs/tf2/ \
  && cd /opt/conda/envs/tf2/darknet \
  && git checkout 4a03d405982aa1e1e911eac42b0ffce29cc8c8ef
COPY darknet/Makefile ./
RUN cd /opt/conda/envs/tf2/darknet \
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