#!/usr/bin/env python3
from setuptools import setup, find_packages

with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()


setup(
    name='Master-Workers-Scraper',
    version='0.5.2',
    packages=find_packages(exclude=["build.*", "tests", "tests.*"]),
    license='MIT',
    description='DIND structure to scrap data with master-workers stucture, using master to manipulate the lifecycle of workers',
    author='ryanyen2',
    author_email='ryanmigi90840@gmail.com',
    url='https://github.com/ryanyen2/master-slave-scraper',
    download_url='https://github.com/ryanyen2/master-slave-scraper/archive/v0.5.2.tar.gz',
    keywords=['twitter', 'scraper', 'python', "crawl", "twitter-scraper", "master", "workers", "DIND", "docker"],
    install_requires=required,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
