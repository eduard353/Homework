from setuptools import setup

setup(
    name='rss-reader',
    version='0.9.2',
    description='Pure Python command-line RSS reader.',
    author='Eduard Malyautskiy',
    packages=['rss_reader'],
    python_requires=">=3.9",
    include_package_data=True,
    install_requires=[
'beautifulsoup4 == 4.11.1',
'build == 0.8.0',
'certifi == 2022.5.18.1',
'charset-normalizer == 2.0.12',
'colorama == 0.4.4',
'idna == 3.3',
'lxml == 4.9.0',
'packaging == 21.3',
'pep517 == 0.12.0',
'pip == 22.1.2',
'pycodestyle == 2.8.0',
'pyparsing == 3.0.9',
'python-dateutil == 2.8.2',
'requests == 2.27.1',
'setuptools == 62.4.0',
'six == 1.16.0',
'soupsieve == 2.3.2.post1',
'tomli == 2.0.1',
'urllib3 == 1.26.9'],
    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader.rss_reader:run',
        ]
    }
)