import os

from setuptools import setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

VERSION = '0.1.0'

setup(
    name='pygpio',
    version=VERSION,
    packages=['pygpio'],
    license='GNU GPL Version 3',
    author='Omer Akram',
    author_email='om26er@gmail.com',
    description='GPIO over WAMP',
    keywords=['linux', 'raspberrypi']
)
