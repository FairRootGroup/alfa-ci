import os
from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='alfa-ci',
    version='0.0.1',
    license='GPLv3+',
    author='Dennis Klein',
    author_email='d.klein@gsi.de',
    description='alfa-ci environment manager',
    long_description=(read('README.md') + '\n\n'),
    long_description_content_type='text/markdown',
    url='https://github.com/FairRootGroup/alfa-ci',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    python_requires='>=3.7',
    setup_requires=['wheel'],
    install_requires=['argcomplete'],
    entry_points={
        'console_scripts': [
            'alfa-ci = alfaci.cli:main',
        ],
    })