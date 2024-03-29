FROM vivianmiranda/whovian-base

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# SET CONDA ENV pytorch

ENV OLDPATH=$PATH \
    PATH=/opt/conda/envs/pytorch/bin:$PATH \
    OLD_LD_LIB_PATH=$LD_LIBRARY_PATH \
    LD_LIBRARY_PATH=/opt/conda/envs/pytorch/libs:$LD_LIBRARY_PATH

# SET CONDA ENV PYMC

RUN conda create --name pytorch python=3.7 -c conda-forge/label/cf202003 \
  --no-default-packages --strict-channel-priority --override-channels \
  --quiet --yes

RUN conda install -n pytorch --quiet --yes \
    freeimage \
    libtiff \
    'conda-forge/label/cf202003::boost=1.70.0' \
    'python-dateutil=2.8.1' \
    'readline=8.0' \
    'six=1.15.0' \
    'numpy=1.19.1' \
    'cython=0.29.21' \
    'tini=0.18.0' \
    'protobuf=3.13.0' \
    'nodejs' \
    'libpng=1.6.37' \
    'kiwisolver=1.2.0' \
    'pyparsing=2.4.7' \
    'pillow=7.2.0' \
    'conda-forge/label/cf201901::fuzzywuzzy' \
    'pyyaml=5.3.1' \
    'virtualenv=16.7.5' \
    'imageio=2.9.0' \
    'widgetsnbextension=3.5.1' \
    'notebook=6.1.1' \
#--------------------------------------------------------------------
# NUMERICAL WORK
    'numba=0.48.0' \
    'scipy=1.5.2' \
    'pandas=1.1.1' \
    'mpi4py=3.0.3' \
    'hdf5=1.10.6' \
    'h5py=2.10.0' \
#--------------------------------------------------------------------
# MachineLearning
    'scikit-image=0.16.2'\
#--------------------------------------------------------------------
  && /opt/conda/envs/pytorch/bin/pip install --quiet --no-cache-dir \
    imutils  \
    pyfits \
    seaborn  \
    emcee  \
    iminuit \
    matplotlib \
#--------------------------------------------------------------------
# Jupyter Lab
    jupyterlab \
#--------------------------------------------------------------------
    torch \
    torchvision \
#--------------------------------------------------------------------
  && conda clean --all -f -y \
  && find $CONDA_DIR -follow -type f -name '*.pyc' -delete \
  && /usr/local/bin/fix-permissions $HOME \
  && /usr/local/bin/fix-permissions $CONDA_DIR

#--------------------------------------------------------------------
# INSTALL DARKNET

ENV PKG-CFG=/usr/bin/pkg-config

RUN git clone git://github.com/pjreddie/darknet.git \
  && mv ./darknet/ /opt/conda/envs/pytorch/ \
  && cd /opt/conda/envs/pytorch/darknet \
  && git checkout f6afaabcdf85f77e7aff2ec55c020c0e297c77f9
COPY darknet/Makefile ./
RUN cd /opt/conda/envs/pytorch/darknet \
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