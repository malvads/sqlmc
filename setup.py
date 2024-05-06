from setuptools import setup, find_packages

setup(
    name='sqlmc',
    version='1.0.0',
    packages=find_packages(),
    package_data={'': ['VERSION']},
    include_package_data=True,
    install_requires=[
        'aiohttp',
        'beautifulsoup4',
        'pyfiglet',
        'tabulate'
    ],
    entry_points={
        'console_scripts': [
            'sqlmc=sqlmc.sqlmc:main',
        ]
    },
    author='Miguel Álvarez',
    description='SQL Injection Massive Checker for a domain',
    license='AGPL-3.0',
    url='https://github.com/malvads/sqlmc',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: OS Independent',
    ],
)
