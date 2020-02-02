from setuptools import setup

setup(
    name='clockify_cli',
    version='0.10',
    py_modules=['clockify_cli'],
    author='Attila Csoma',
    url='https://github.com/csomaati/clockify-cli',
    install_requires=[
        'click>=7.0',
        'certifi==2018.8.13',
        'chardet==3.0.4',
        'idna==2.7',
        'requests>=2.20.0',
        'urllib3==1.23',
    ],
    entry_points='''
        [console_scripts]
        clockify=clockify_cli.cli:main
   ''', 
)
