# setup.py
#
# Author: Fabian Meyer
# Created On: 31 Jan 2019

from setuptools import setup

setup(name='bombgame2',
    version='0.1',
    description='',
    license='MIT',
    author=['Fabian Meyer', 'Jens Gansloser'],
    author_email='',
    packages=['bombgame'],
    package_data={'bombgame': ['assets/*.png']},
    ext_modules=[],
    entry_points={
        'console_scripts': ['bombgame2=bombgame:run'],
    },
    install_requires=['numpy', 'pygame']
)
