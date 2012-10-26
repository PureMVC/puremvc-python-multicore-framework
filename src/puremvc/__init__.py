# -*- coding: utf-8 -*-
"""
 PureMVC Python Port by Toby de Havilland <toby.de.havilland@puremvc.org>
 PureMVC Python Port by Daniele Esposti <expo@expobrain.net>
 PureMVC - Copyright(c) 2006-08 Futurescale, Inc., Some rights reserved.
 Your reuse is governed by the Creative Commons Attribution 3.0 License
"""


class MultitonError(Exception):
    """
    Exception raised by multiton classes
    """

    def __init__(self, message):
        super(Exception, self).__init__(message)
