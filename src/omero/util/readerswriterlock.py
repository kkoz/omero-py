#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# OMERO ReadersWriterLock class
# Copyright 2021 Glencoe Software, Inc.  All Rights Reserved.
# Use is subject to license terms supplied in LICENSE.txt

import threading

class ReadersWriterLock(object):
    def __init__(self):
        self._rwlock = threading.Condition(threading.RLock())
        self._readers_count = 0

    def acquire_read_lock(self):
        self._rwlock.acquire()
        self._readers_count += 1
        self._rwlock.release()
        
    def release_read_lock(self):
        self._rwlock.acquire()
        self._readers_count -= 1
        if self._readers_count == 0:
            self._rwlock.notifyAll()
        self._rwlock.release()

    def acquire_write_lock(self):
        self._rwlock.acquire()
        while self._readers_count > 0:
            self._rwlock.wait()

    def release_write_lock(self):
        self._rwlock.release()

