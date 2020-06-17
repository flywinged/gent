from distutils.core import setup

setup(
    name = 'TGL',
    packages = ['TGL'],
    version = '0.01',
    license = 'MIT',
    description = 'TGL (Terminal Graphics Library), is a library to allow interaction in user terminals',
    author = 'Clayton Brown',
    author_email = 'clayton.john.brown@gmail.com',
    url = 'https://github.com/flywinged/TGL',
    # download_url = 'https://github.com/flywinged/TGL/archive/v_01.tar.gz',
    keywords = ['Terminal', 'Graphics', 'Library', 'Game', 'Engine'],
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