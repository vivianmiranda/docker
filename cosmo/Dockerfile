FROM vivianmiranda/whoviancosmobase

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# --------------------------------------------------------------------------
# PIP
RUN pip install --upgrade --no-cache-dir pip setuptools wheel \
    pip install --no-cache-dir \
    'python-config' \
    'numpy==1.19.1' \
    'python-dateutil==2.8.1' \
    'six==1.15.0' \
    'cython==0.29.21' \
    'protobuf==3.13.0' \
    'nodejs' \
    'kiwisolver==1.2.0' \
    'pyparsing==2.4.7' \
    'pillow==7.2.0' \
    'fuzzywuzzy==0.17.0' \
    'pyyaml==5.3.1' \
    'virtualenv==20.0.20' \
    'imageio==2.9.0' \
    'notebook==6.1.1' \
    'scipy==1.5.2' \
    'pandas==1.1.1' \
    'h5py==2.10.0' \
    'astropy==4.0.1.post1' \
    'pybind11==2.5.0' \
    'tokenizers==0.8.1' \
    'numba==0.50.1' \
    'GetDist==1.1.2' \
    'requests==2.24.0' \
  && pip install --no-cache-dir \
    'pyfits==3.5' \
    'seaborn==0.10.1' \
    'emcee==3.0.2' \
    'iminuit==1.4.9' \
    'py-bobyqa==1.2' \
    'wget==3.2' \
    'matplotlib==3.3.1' \
    'mpi4py==3.0.3' \
  && /usr/local/bin/fix-permissions $HOME

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
