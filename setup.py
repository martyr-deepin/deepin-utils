#! /usr/bin/env python

from setuptools import setup, Extension
import commands

def pkg_config_cflags(pkgs):
    '''List all include paths that output by `pkg-config --cflags pkgs`'''
    return map(lambda path: path[2::], commands.getoutput('pkg-config --cflags-only-I %s' % (' '.join(pkgs))).split())

def pkg_config_libs(pkgs):                                                    
    '''List all include paths that output by `pkg-config --libs pkgs`'''         
    return map(lambda path: path[2::], commands.getoutput('pkg-config --libs-only-l %s' % (' '.join(pkgs))).split())

cairo_mod = Extension('dtk_cairo_blur',
                include_dirs = pkg_config_cflags(['cairo', 'pygobject-2.0']),
                libraries = ['cairo', 'pthread', 'glib-2.0'],
                sources = ['./deepin_utils/cairo_blur.c'])
webkit_mod = Extension('dtk_webkit_cookie',
                include_dirs = pkg_config_cflags(['gtk+-2.0', 'webkit-1.0', 'pygobject-2.0']),
                libraries = ['webkitgtk-1.0', 'soup-2.4', 'pthread', 'glib-2.0'],
                sources = ['./deepin_utils/webkit_cookie.c'])
deepin_font_icon_mod = Extension('deepin_font_icon',
                include_dirs = pkg_config_cflags(['glib-2.0', 'cairo', 'pycairo']),
                libraries = pkg_config_libs(['glib-2.0', 'cairo', 'pycairo']),
                sources = ['./deepin_utils/deepin_font_icon.c'])

setup(name='deepin_utils',
      version='1.0',
      ext_modules = [cairo_mod, webkit_mod, deepin_font_icon_mod],
      description='Basic utils for all projects in Linux Deepin.',
      long_description ="""Python download library for Linux DeepinBasic utils for all projects in Linux Deepin.""",
      author='Wang Yong',
      author_email='wangyong@linuxdeepin.com',
      license='GPL-3',
      url="https://github.com/linuxdeepin/deepin-utils",
      download_url="git://github.com/linuxdeepin/deepin-utils.git",
      platforms = ['Linux'],
      packages = ['deepin_utils'],
      )

