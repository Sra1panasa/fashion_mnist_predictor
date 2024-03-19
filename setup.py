from setuptools import find_packages, setup

setup(
    name='kognitive_src',
    packages=find_packages(), package_data={
    '': ['*.ini','*.json','*.xml']
    },
    version='0.1.0',
    description='Fashion Mnist Prediciton',
    author='kognitive',
    license='',
)
