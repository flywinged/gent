from distutils.core import setup

import setuptools

setup(
    name = 'TGE',
    packages = setuptools.find_packages(),
    version = '0.0.1a1',
    license = 'MIT',
    description = 'TGE (Terminal Game Engine), is a library to allow game like interactions in user terminals',
    author = 'Clayton Brown',
    author_email = 'clayton.john.brown@gmail.com',
    url = "https://github.com/flywinged/TGE",
    # download_url = 'https://github.com/flywinged/pyGEfT/archive/v_01.tar.gz',
    keywords = ['Terminal', 'Graphics', 'Game', 'Engine'],
    install_requires = [            # I get to this in a second
        'numpy',
        'colorama',
        'sty',
        'dataclasses'
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
)