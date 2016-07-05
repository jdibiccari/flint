from setuptools import setup, find_packages
from flint import __version__

setup(
    name='Flint',
    version=__version__,
    author='Janel diBiccari',
    author_email='janel.dibiccari@gmail.com',
    description='A simple command line Kickstarter application',
    url='https://github.com/jdibiccari/flint',
    license='MIT',
    packages=find_packages(),
    package_data={
        "flint.db": ["flint/db/*"]
    },
    install_requires=[
    	'click',
    	'yoyo-migrations'
    ],
    include_package_data=True,
    extras_require = {
        'test': ['coverage', 'pytest', 'pytest-cov'],
    },
    setup_requires=['pytest-runner', 'pytest'],
    entry_points= {'console_scripts': [
            'flint=flint.cli:flint',
        ],
    },
)

