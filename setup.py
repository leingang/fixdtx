from setuptools import setup

setup(
    name='fixdtx',
    version='0.1.0',
    py_modules=['fix'],
    install_requires=[
        'Click',
    ],
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'fixdtx = fix:cli',
        ],
    },
)