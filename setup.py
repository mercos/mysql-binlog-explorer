from setuptools import setup

setup(
    name='mysql-binlog-explorer',
    version='0.1.1',
    description='Web UI to Explore MySQL\'s binlog files a little easier.',
    long_description_markdown_filename='README.md',
    keywords='mysql binlog analysis ui web explore',
    url='https://github.com/meuspedidos/mysql-binlog-explorer',
    author='MeusPedidos Engineering Team',
    author_email='israel.bgf@gmail.com, jorge.klemm@hotmail.com, cleberben.warmling@gmail.com',
    license='MIT',
    packages=['binlogexplorer'],
    setup_requires=['setuptools-markdown'],
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'bottle==0.12.10',
    ],
    entry_points={
        'console_scripts': ['mysql-binlog-explorer=binlogexplorer.webui:main'],
    },

)
