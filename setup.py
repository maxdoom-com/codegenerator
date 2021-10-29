from setuptools import setup

setup(
    name='codegenerator',
    version='0.0.1',
    author='Nico Hoffmann',
    author_email='n-py-codegenerator@maxdoom.com',
    packages=['codegenerator',],
    url='https://github.com/maxdoom-com/codegenerator/',
    license='LICENSE.md',
    description='A simple codegenerator connecting yaml files (data) and jinja2 templates.',
    long_description=open('README.md').read(),
    install_requires=[
        "pyyaml",
        "jinja2",
    ],
)