from setuptools import setup, find_packages

setup(
    name="logincraw",
    version="1.0",
    description=("login craw library"),
    #license="MIT Licence",
    url="http://test.com",
    author="aaronhua",
    author_email="cjhdwyyx@163.com",
    packages=find_packages(),
    platforms=["all"],
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'logincrawmain = logincraw.main:main'
        ]
    }
)