from setuptools import setup
from flint import __version__

setup(
    name='Flint',
    version=__version__,
    author='Janel diBiccari',
    author_email='janel.dibiccari@gmail.com',
    description='A simple command line Kickstarter application',
    license='MIT',
    packages=['flint'],
    install_requires=[
    	'click',
    	'yoyo-migrations'
    ],
    include_package_data=True,
    entry_points= {'console_scripts': [
            'flint=flint.cli:flint',
        ],
    },
)

