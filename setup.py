#!/usr/bin/env python3
# -*- coding: utf-8 -*-
try:
    import distribute_setup
    distribute_setup.use_setuptools()
except:
    pass

from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

import os
import re


with open(os.path.join(os.path.dirname(__file__), 'ume', '__init__.py')) as f:
    version = re.search("__version__ = '([^']+)'", f.read()).group(1)

with open('requirements.txt', 'r') as f:
    requires = [x.strip() for x in f if x.strip()]

with open('test-requirements.txt', 'r') as f:
    test_requires = [x.strip() for x in f if x.strip()]

xgboost_files = [
    "ume/externals/_xgboost_wrapper.pyx",
    "ume/externals/_xgboost/wrapper/xgboost_wrapper.cpp",
    "ume/externals/_xgboost/subtree/rabit/src/allreduce_base.cc",
    "ume/externals/_xgboost/subtree/rabit/src/allreduce_robust.cc",
    "ume/externals/_xgboost/subtree/rabit/src/engine.cc",
    "ume/externals/_xgboost/src/tree/updater.cpp",
    "ume/externals/_xgboost/src/io/io.cpp",
    "ume/externals/_xgboost/src/gbm/gbm.cpp",
]

extensions = [
    Extension("ume.externals._xgboost_wrapper", xgboost_files,
        include_dirs=['ume/externals/_xgboost'],
        library_dirs=[],
        libraries=['pthread', 'm', 'gomp'],
        extra_compile_args=[
            '-O3', '-msse2', '-Wall',
            '-Wno-unknown-pragmas',
            '-std=c++11',
            '-fPIC',
            '-fopenmp',
            '-DRABIT_USE_HDFS=0'],
        define_macros=[],
        depends=[],
        language='c++'),
]

setup(
    name='ume',
    version=version,
    description="Personal datamining framework for kaggle",
    ext_modules=cythonize(extensions),
    #packages=find_packages(exclude=['doc', 'tests']),
    #package_dir=['ume/externals'],
    #packages=["ume/externals"],
    #entry_points={'console_scripts': ['ume = ume.cmd:main']},
    #test_suite='tests',
    #tests_require=test_requires,
    #install_requires=requires,
    #extras_require={'tests': test_requires}
)
