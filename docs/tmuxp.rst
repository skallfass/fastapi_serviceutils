tmuxp
^^^^^

.. include:: sources.rst

For a predefined development environment the ``.tmuxp.yml`` configuration can
be used to create a Tmux_-session (using Tmuxp_) with a window including three
panels:

* one panel for **editing files**
* one panel **running the service**
* one panel **running the tests**

Run the following command to create the tmux-session:

.. code-block:: bash

    tmuxp load .
