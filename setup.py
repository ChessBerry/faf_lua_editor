from setuptools import setup, find_packages
from faf_lua_editor import __version__

setup(
    name='faf_lua_editor',
    version=__version__,
    description='Editor for the FAF lua code',
    # long_description=long_description,
    url='https://github.com/ChessBerry/faf_lua_editor',
    author='CheeseBerry',
    author_email='cheeseberry@protonmail.com',
    license='MIT',
    packages=find_packages(),
    nclude_package_data=True,
    package_data={'faf_lua_editor': ['faf_lua_editor/moho_reference/*.json']},
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        'antlr4-python3-runtime<=4.7.2',
        'luaparser==3.0.1FAF',
    ]
)
