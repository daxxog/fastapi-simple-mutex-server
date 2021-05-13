from setuptools import setup, find_packages
PACKAGE_NAME='fastapi-simple-mutex-server'


requirements = [
    "fastapi",
    "uvicorn",
    "hiredis",
    "aioredis"
]

tests_require = [
    'jedi',
    'pudb',
    'pytest',
    'pytest-cov',
    'pytest-pudb',
    'responses',
    'pyfakefs',
    'tox',
    'tox-pyenv'
]


with open('README.md') as f:
    long_desc = f.read()

with open('VERSION') as f:
    version = f.read()

setup(
    name=PACKAGE_NAME,
    version=version,
    description='A simple FastAPI microservice for manging locks.',
    long_description=long_desc,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.9',
        'Topic :: System :: Distributed Computing',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers'
    ],
    keywords="",
    author="David Volm",
    author_email="david@volminator.com",
    url="https://github.com/daxxog/fastapi_simple_mutex_server",
    license="Apache 2.0",
    install_requires=requirements,
    packages=find_packages("src"),
    package_dir={'': 'src'},
    test_suite='tests',
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3'],
    extras_require={
        "test": tests_require
    },
    entry_points={
        'console_scripts': [
            'fastapi-simple-mutex-server = fastapi_simple_mutex_server.cli:main'
        ],
    },
)

