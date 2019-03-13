[![Build Status](https://api.travis-ci.org/globocom/link-migration.png)](https://api.travis-ci.org/globocom/link-migration)

Link Migration
===========

A generic tool for migrate in python.

Link Migration brings migrations to Python applications. Its main objectives are to provide a simple, stable and database-independent migration layer to prevent all the hassle schema changes over time bring to your applications.

We try to make Link Migration both as easy-to-use and intuitive as possible, by making it automate most of your schema-changing tasks, while at the same time providing a powerful set of tools for large or complex projects.

Version
=======

0.0.7


Install
=======

If you have pip available on your system, just type::

    pip install link-migration

If you’ve already got an old version of link-migration, and want to upgrade, use:

    pip install --upgrade link-migration



Understanding how to use
========================

The first thing you’ll need is a migration file. There are some example 
migration files in the “link-migrations” directory. The migration files 
have the following format::

The folder link-migrations need be a module (\_\_init\_\_.py most be present in link-migrations folder).


    # -*- coding: utf-8 -*-

    """
        migrate all the world of test
        greetings world
    """

    version = "0.0.1"

    def up():
        """ HeLo World and migrate the world """
        print "HeLo World and migrate the world"

    def down():
        """roolback the world"""
        print "Bye World and roolback the world"


Link Migration uses the _version_ information to track the migrations schema and to 
decide the order of execution of the scripts. Link Migration will go through all .py 
files in your directory and execute all of them in their creation (date) order.

Second, you have to configure access to your current version so Link Migration can execute DDL. 
Just create a file named “conf.py”, with the following content 
(there is also an example in the “link-migration” directory):

    # -*- coding: utf-8 -*-
    import settings

    folder = "{PATH_LINKMIGRATION}/version.txt".format(**vars(settings))

It is possible to override the way Link Migration retrieve the current version. To do so,
you just need do implement the methods get_current_version and set_current_version:

    # -*- coding: utf-8 -*-

    folder = "/version_folder"

    def current_version():
        with open("{folder}/version.txt".format(folder=folder)) as f:
            version = f.read()
        return version

    def set_current_version(version):
        with open("{folder}/version.txt".format(folder=folder)) as f:
            f.write(version)



Migrating to a specific version
===============================

If you want, you can migrate your database schema to a specific version by 
informing the --to (or -t) parameter. The attribute _version_ of the migration
file will be used as unique identifier:

    $ link-migration --to=00.00.01

If you don’t specify any version, using --up or --down, Link Migration will migrate 
the schema to the latest version available in the migrations directories 
specified in the config file.



You can do anything!
====================

You can use this project to run migrations on MySQL, Oracle, MS-SQL, redis, filesystem, 
solr, elasticsearch or any database server.


Getting involved !
==================

Link Migration's development may be viewed and followed on github::

    http://github.com/globocom/link-migration

Retrieve the source code using 'git'::

    $ git clone git@github.com:globocom/link-migration.git


Install package in 'development mode' and run tests with _run_::

    $ git clone git@github.com:globocom/link-migration.git
    $ cd link-migration
    $ ./run unit



