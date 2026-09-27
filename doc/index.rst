..
    Zephyr Project documentation main file

.. _zephyr-home:

Zephyr Project Documentation
############################

.. raw:: html

   <script>
     function openVersionSelector() {
       // Open the mobile menu if visible
       var mobileMenu = document.querySelector('[data-toggle="wy-nav-top"]');
       if (mobileMenu && mobileMenu.offsetParent !== null) {
         mobileMenu.click();
       }
       // Open the version selector
       var versionSelector = document.querySelector('[data-toggle="rst-current-version"]');
       if (versionSelector) {
         versionSelector.click();
       }
     }
   </script>

.. only:: release

   .. admonition:: Welcome to Zephyr Project Documentation for version |version|.
      :class: welcome

      Use the `official documentation site <https://docs.zephyrproject.org/>`_
      for documentation of other Zephyr versions.

.. only:: development

   .. admonition:: Welcome to Zephyr Project Documentation for the ``main`` tree (|version|).
      :class: welcome

      Use the `official documentation site <https://docs.zephyrproject.org/>`_
      for documentation of previously released versions.

.. raw:: html
   :file: index.html

.. toctree::
   :maxdepth: 1
   :hidden:

   introduction/index.rst
   develop/index.rst
   kernel/index.rst
   services/index.rst
   Build and Configuration Systems <build/index.rst>
   hardware/index.rst
   contribute/index.rst
   project/index.rst
   security/index.rst
   safety/index.rst
   Samples and Demos <samples/index.rst>
   Supported Boards and Shields <boards/index.rst>
   releases/index.rst
