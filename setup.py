from setuptools import setup

setup(
    name='fixdtx',
    version='0.1.0',
    packages=['fixdtx'],
    install_requires=[
        'Click',
    ],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fixdtx = fixdtx.cli:cli',
        ],
    },
)