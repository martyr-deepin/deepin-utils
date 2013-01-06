#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from .path import touch_file_dir
        
def write_file(filepath, content, mkdir=False):
    '''
    Write file with given content.

    @param filepath: Target filepath to write.
    @param content: File content to write.
    '''
    if mkdir:
        touch_file_dir(filepath)
    
    f = open(filepath, "w")
    f.write(content)
    f.close()

def read_file(filepath, check_exists=False):
    '''
    Read file content.
    
    @param filepath: Target filepath.
    @param check_exists: Whether check file is exist, default is False.
    
    @return: Return \"\" if check_exists is True and filepath not exist.
    
    Otherwise return file's content.
    '''
    if check_exists and not os.path.exists(filepath):
        return ""
    else:
        r_file = open(filepath, "r")
        content = r_file.read()
        r_file.close()
        
        return content
