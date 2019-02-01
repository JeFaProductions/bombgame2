# setup.py
#
# Author: Fabian Meyer
# Created On: 31 Jan 2019

from distutils.core import setup

setup(name='bombgame2',
    version='0.1',
    description='',
    license='MIT',
    author=['Fabian Meyer', 'Jens Gansloser'],
    author_email='',
    packages=['bombgame'],
    package_data={'bombgame': ['assets']},
    ext_modules=[],
    scripts=['bombgame2.py'])
