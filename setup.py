from setuptools import setup
from flint import __version__

setup(
    name='Flint',
    version=__version__,
    author='Janel diBiccari',
    author_email='janel.dibiccari@gmail.com',
    description='A simple command line Kickstarter application',
    url='https://github.com/jdibiccari/flint',
    license='MIT',
    packages=['flint'],
    install_requires=[
    	'click',
    	'yoyo-migrations'
    ],
    include_package_data=True,
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points= {'console_scripts': [
            'flint=flint.cli:flint',
        ],
    },
)

