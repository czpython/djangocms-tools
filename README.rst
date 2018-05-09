****************
django CMS Tools
****************

============
Installation
============

Requirements
============

django CMS Alias requires that you have a django CMS 3.4 (or higher) project already running and set up.


To install
==========

Run::

    pip install git+git://github.com/czpython/djangocms-tools#egg=djangocms-tools

Add ``djangocms_tools`` to your project's ``INSTALLED_APPS``.

Run::

    python manage.py migrate djangocms_tools

to perform the application's database migrations.


=====
Usage
=====

Example::

    ./manage.py create_page_tree --max-count 300 --max-count-children 3 --max-depth 2


Will create a page tree with a total of 300 root pages, 3 direct child pages for each new page
and up to 3 levels (first plus max-depth) in depth.

