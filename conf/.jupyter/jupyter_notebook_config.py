c = get_config()  # get the config object
c.IPKernelApp.pylab = 'inline'  # in-line figure when using Matplotlib
c.NotebookApp.ip = '*'
c.NotebookApp.allow_remote_access = True
c.NotebookApp.open_browser = False # do not open a browser window by default when using notebooks
c.NotebookApp.notebook_dir = '/model'
c.NotebookApp.allow_root = True # Allow to run Jupyter from root user inside Docker container
c.NotebookApp.allow_origin = '*'
c.NotebookApp.tornado_settings = {
    'headers': {
        'Content-Security-Policy': "frame-ancestors 'self' *"
    }
}
c.NotebookApp.max_buffer_size = 70000000000
NotebookApp.iopub_data_rate_limit=10000000000
c.NotebookApp.shutdown_no_activity_timeout = 0
c.NotebookApp.webbrowser_open_new = 2