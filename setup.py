# coding:utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='douban-book',
    version='1.0.0',
    description='Douban book api',
    author='hxgz',
    author_email='jwzhou0905@gmail.com',
    url='',
    packages=['douban_book'],
)
