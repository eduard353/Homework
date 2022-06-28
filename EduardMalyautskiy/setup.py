from setuptools import setup, find_packages

setup(
    name='rss-reader',
    version='0.9.4',
    description='Pure Python command-line RSS reader.',
    author='Eduard Malyautskiy',
    python_requires=">=3.9",
    packages=find_packages(),
    package_data={'': ['*.txt', '*.db', '*.ttf', '*.html', '*.jpg', '*.sql']
                  },
    install_requires=[
'beautifulsoup4==4.11.1',
'bs4==0.0.1',
'certifi==2022.6.15',
'charset-normalizer==2.0.12',
'defusedxml==0.7.1',
'fpdf2==2.5.5',
'idna==3.3',
'Jinja2==3.1.2',
'lxml==4.9.0',
'MarkupSafe==2.1.1',
'Pillow==9.1.1',
'progress==1.6',
'python-dateutil==2.8.2',
'requests==2.28.0',
'six==1.16.0',
'soupsieve==2.3.2.post1',
'urllib3==1.26.9',],

    entry_points={
        'console_scripts': [
            'rss_reader=rss_reader.rss_reader:run',
        ]
    }
)
