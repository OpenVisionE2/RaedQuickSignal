#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup

pkg = 'Extensions.RaedQuickSignal'
setup (name = 'enigma2-plugin-extensions-raedquicksignal',
       version = '4.8',
       description = 'Plugin to show useful information in enigma2.',
       packages = [pkg],
       package_dir = {pkg: 'usr'},
       package_data = {pkg: ['plugin.png', '*/*.png']},
      )
