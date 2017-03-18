========================================
Generating documentation - In a nutshell
========================================

This page describes how to generate our documentation automatically.

This guidelines are also in a static page in the ``nordlys-v02`` documentation to be generated (``doc/build/html/generating_doc-in_a_nutshell.html``). But first you need to generate it to see it :) 


A quick tour for documenting Nordlys
------------------------------------

How to generate HTML documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's assume we already have (like currently in our repository in ``doc/source/``) the .rst source files for the documentation.

We run ::

	$ make html

from the documentation directory, e.g. ``[...]/nordlys-v02/doc``. That renders the HTML documents in ``build/html/`` with ``index.html`` being the main page (such .html files are not kept under version control). *And that's all.*


Modifying modules and re-documenting them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you modify the content of a module, just run ``make html``. You don't need to run any other command before, since the package hierarchy didn't change.


Adding/moving modules and documenting them
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Everytime we change the project package tree (for example, when we add a module, or we move a module from one place to another), we need to modify somehow the .rst files corresponding to those modifications *before* running ``make html``.

If you add packages or modules, you can create their respective .rst files by running  the command: ::

	$ make rstf
	
which is actually a wrapper for the command: ::

	$ sphinx-apidoc -f -T -e -M -o source/api/ ../nordlys

It will force (that's why the ``-f`` option) to create all the .rst files (and overwriting, i.e. "forcing", the existing ones to update the possible changes in the modules hierarchy).

As it overwrites the existing .rst files, **it should be used carefully** and it should be followed by a manual checking for not pushing any broken documentation.

Alternatively you could run: ::

	$ make rst

which is, as before, a wrapper for the ``sphinx-apidoc`` command with those same options excepting ``-f``. It will create only all the missing .rst files and skip the ones already existing, i.e. it will not reflect properly the changes in the package hierarchy.


Adding a static page
~~~~~~~~~~~~~~~~~~~~

Should you have something to explain with more details, beyond the syntax and the space of the docstrings, you can create a new "section" in the documentation, by adding a static page. The nutshell you are reading, or any other page from the left menu after the main ``nordlys``, is rendered as a static page.

Create a .rst file in ``source/``, e.g. ``a_static_page.rst``, and add its name ``a_static_page`` (starting with lowercase) in a new line in the "Contents" section of ``source/index.rst`` (the .rst header file). Then run only ``make html``.


Some words about Sphinx
-----------------------

``sphinx`` is a tool for automatically generate code documentation.

We use the ReadTheDocs HTML theme. Both ``sphinx`` and ``sphinx_rtd_theme`` should be part of ``anaconda``. Otherwise, if you need to install them: ::

	$ sudo pip install --upgrade pip
	$ pip install Sphinx
	$ pip install sphinx_rtd_theme

``sphinx`` contains several commands, among which the one we use for generating the docs is the ``sphinx-apidoc`` command, and a ``make`` we already created.


The rendering imports each module and accesses to its docstrings. But we only care about that it uses the .rst files we have in ``source/``. A special source header is ``index.rst``. For the rest of the .rst files, the first time we created them we ran: ::

	$ sphinx-apidoc -T -e -M -o source/api/ ../nordlys

which generates in ``source/api/`` one .rst file for every new module, with the appropriate syntax to document it according to the package hierarchy of the project.

**This command is also what we use to regenerate a .rst file, or add a new one.**

In general (as from ``$ sphinx-apidoc --help``), ::

	$ sphinx-apidoc [options] -o <output_path> <module_path>

The most useful options are: ::

	-f, --force			  Overwrite all existing files
	-e, --separate        Put documentation for each module on its own page
	-P, --private         Include "_private" modules
	-T, --no-toc          Don't create a table of contents file
	-E, --no-headings     Don't create headings for the module/package packages
	                      (e.g. when the docstrings already contain them)
	-M, --module-first    Put module documentation before submodule
	                      documentation


Useful links
------------

  - `reST syntax <http://www.sphinx-doc.org/en/stable/rest.html>`_
  - ``sphinx-apidoc`` `reference <http://www.sphinx-doc.org/en/stable/man/sphinx-apidoc.html>`_
