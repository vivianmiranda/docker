FROM vivianmiranda/whovian-base

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# SET CONDA ENV TF2

ENV OLDPATH=$PATH \
    PATH=/opt/conda/envs/tf2/bin:$PATH \
    OLD_LD_LIB_PATH=$LD_LIBRARY_PATH \
    LD_LIBRARY_PATH=/opt/conda/envs/tf2/libs:$LD_LIBRARY_PATH

RUN conda create --name tf2 python=3.8 --quiet --yes \
  && conda install -n tf2 --quiet --yes \
    'conda-forge::numpy=1.21.4' \
    'conda-forge::cython=0.29.24' \
    'conda-forge::matplotlib=3.3.1' \
    'conda-forge::imutils=0.5.3' \
    'conda-forge::numba=0.50.1' \
    'conda-forge::scipy=1.8.0' \
    'conda-forge::pandas=1.4.1' \
    'conda-forge::hdf5=1.10.6' \
    'conda-forge::h5py=2.10.0' \
    'conda-forge::scikit-image=0.19.2' \
    'conda-forge::scikit-learn=1.0.2' \
  && /opt/conda/envs/tf2/bin/pip install --quiet --no-cache-dir --upgrade importlib-metadata \
#--------------------------------------------------------------------
  && /opt/conda/envs/tf2/bin/pip install --quiet --no-cache-dir \
    'tensorflow-gpu==2.11.0' \
    'keras==2.11.0' \
    'keras-preprocessing' \
    'astropy==5.2' \
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

RUN git clone https://github.com/pjreddie/darknet.git \
  && mv ./darknet/ /opt/conda/envs/tf2/ \
  && cd /opt/conda/envs/tf2/darknet \
  && git checkout f6afaabcdf85f77e7aff2ec55c020c0e297c77f9
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
