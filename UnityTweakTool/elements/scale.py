#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Team:
#   J Phani Mahesh <phanimahesh@gmail.com>
#   Barneedhar (jokerdino) <barneedhar@ubuntu.com>
#   Amith KK <amithkumaran@gmail.com>
#   Georgi Karavasilev <motorslav@gmail.com>
#   Sam Tran <samvtran@gmail.com>
#   Sam Hewitt <hewittsamuel@gmail.com>
#   Angel Araya <al.arayaq@gmail.com>
#
# Description:
#   A One-stop configuration tool for Unity.
#
# Legal Stuff:
#
# This file is a part of Unity Tweak Tool
#
# Unity Tweak Tool is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# Unity Tweak Tool is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, see <https://www.gnu.org/licenses/gpl-3.0.txt>

''' Definitions for Scale element. '''
from UnityTweakTool.backends import gsettings

import logging
logger=logging.getLogger('UnityTweakTool.elements.scale')

class Scale:
    def __init__(self,controlObj):
        ''' Initialise a scale from a controlObj dictionary '''
        self.id         = controlObj['id']
        self.ui         = controlObj['builder'].get_object(controlObj['id'])
        self.schema     = controlObj['schema']
        self.path       = controlObj['path']
        self.key        = controlObj['key']
        self.type       = controlObj['type']
        self.min        = controlObj['min']
        self.max        = controlObj['max']
        self.disabled   = False
        try:
            assert gsettings.is_valid(
                schema  = self.schema,
                path    = self.path,
                key     = self.key
                )
        except AssertionError as e:
            self.disabled=True
# TODO : Set range using min, max
        logger.debug('Initialised a scale with id {self.id} to control key {self.key} of type {self.type} in schema {self.schema} with path {self.path}'.format(self=self))


    def register(self,handler):
        ''' Register handler on a handler object '''
        handler['on_%s_value_changed'% self.id]=self.handler
        logger.debug('Handler for {self.id} registered'.format(self=self))

    def refresh(self):
        ''' Refresh the UI querying the backend '''
        logger.debug('Refreshing UI display for {self.id}'.format(self=self))
        if self.disabled:
            self.ui.set_sensitive(False)
            return
        self.ui.set_value(
            gsettings.get(
                schema=self.schema,
                path  =self.path,
                key   =self.key,
                type  =self.type
                )
            )

    def handler(self,*args,**kwargs):
        ''' Handle value_changed signals '''
        if self.disabled:
            return
        gsettings.set(
            schema=self.schema,
            path=self.path,
            key=self.key,
            type=self.type,
            value=self.ui.get_active()
            )
        logger.info('Handler for {self.id} executed'.format(self=self))

    def reset(self):
        ''' Reset the controlled key '''
        if self.disabled:
            return
        gsettings.reset(schema=self.schema,path=self.path,key=self.key)
        logger.debug('Key {self.key} in schema {self.schema} and path {self.path} reset.'.format(self=self))
