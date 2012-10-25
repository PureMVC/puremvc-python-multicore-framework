#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fabric.operations import local


def install():
    """ Install package
    """
    local("python ./setup.py clean")
    local("python ./setup.py install")


def clean():
    """ Remove local .pyc files
    """
    local("find ./src/ -name '*.pyc' -exec rm -rf {} \;")
    local("find ./tests/ -name '*.pyc' -exec rm -rf {} \;")
    local("rm -rf docs/*")


def docs():
    """ Build docs
    """
    local("rm -rf ./docs/*")
    local("epydoc -v --html --name 'PureMVC Multicore Python' "
          "./src/puremvc -o ./docs/")


def test():
    """ Run unit tests
    """
    local("python ./tests/main.py")


def pep8():
    """ Run unit tests
    """
    local("pep8 -r .")
