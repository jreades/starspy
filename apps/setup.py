#!/usr/bin/env python
"""
setup.py - script for building a stars App

Usage:
    Mac:
    % python setup.py py2app
    Windows:
    c:\> python setup.py py2exe --bundle=1
        Notes for Windows: Do not try to build on a shared or otherwise network drive.
                           Make sure the the build location is on a local drive.
"""
import sys,os
if __name__=='__main__':
    if len(sys.argv) == 1:
        print "Going to Build Now!"
        if sys.platform == 'darwin':
            sys.argv.extend(['py2app', '--iconfile', 'NIJ_Demo/icons/oGeoDa.icns'])
        elif sys.platform == 'win32':
            sys.argv.extend(['py2exe', '--bundle=1'])

from distutils.core import setup
pkgs = []
if sys.platform == 'darwin':
    import py2app
    setup( app=['NIJ_Demo/NIJ_Stars_Demo.py'], 
           packages=pkgs
         )
elif sys.platform == 'win32':
    import py2exe
    origIsSystemDLL = py2exe.build_exe.isSystemDLL
    def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ('msvcp71.dll'):
            return 0
        return origIsSystemDLL(pathname)
    py2exe.build_exe.isSystemDLL = isSystemDLL
    setup( zipfile=None,
           windows=[ {"script": "NIJ_Stars_Demo.py", 
                      "icon_resources": [(1, "NIJ_Stars_Demo/icons/oGeoDa.ico")]}],
           packages=pkgs
         )

