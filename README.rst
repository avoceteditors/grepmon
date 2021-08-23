
GrepMon
########

Grep utilities, (such as ``grep``, ``egrep``, and ``rgrep``), are great tools for inspecting the contents of a text file or files. 

GrepMon enables the execution of grep commands with the addition of a watchdog system that monitors the given files for updates.  Upon changes it reruns the grep command and updates the list of watch files and prints the results to stdout.  This provides a running burndown list for file changes.

Note that this is currently an alpha build under active development and may not run reliably or on all systems.

Installation
*************

.. code-block:: console

   $ python3 setup.py install --user

Usage
******

.. code-block:: console

   $ grepmon grep "example_pattern" source -R


