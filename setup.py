from setuptools import setup
from os.path import join as path

with open(path('README.md')) as markdown_content:
    readme_text = markdown_content.read()
with open(path('binlogexplorer', 'version')) as version_content:
    version_text = version_content.read().strip()

setup(
    name='mysql-binlog-explorer',
    version=version_text,
    description='Web UI to Explore MySQL\'s binlog files a little easier.',
    long_description=readme_text,
    long_description_content_type='text/markdown',
    keywords='mysql binlog analysis ui web explore',
    url='https://github.com/meuspedidos/mysql-binlog-explorer',
    author='MeusPedidos Engineering Team',
    author_email='israel.bgf@gmail.com, jorge.klemm@hotmail.com, cleberben.warmling@gmail.com',
    license='MIT',
    packages=['binlogexplorer'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'bottle==0.12.17',
        'simplejson==3.16.0'
    ],
    entry_points={
        'console_scripts': ['mysql-binlog-explorer=binlogexplorer.webui:main'],
    },

)
