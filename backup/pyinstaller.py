#coding:utf-8
'''
Created on 2015年8月8日 下午2:35:42

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132
'''
#! /usr/bin/env python
#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
"""
Main command-line interface to PyInstaller.
"""
# from  PyInstaller import  *
import  os

if __name__ == '__main__':
    from PyInstaller.main import run
    opts=['showUI.py','-D','-w']
    run(opts)