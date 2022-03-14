from setuptools import find_packages
from distutils.core import setup

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(install_requires=['aiohttp==3.8.1', 'aioresponses==0.7.3', "aiosignal==1.2.0; python_version >= '3.6'", "async-timeout==4.0.2; python_version >= '3.6'", 'asyncio==3.4.3', "attrs==21.4.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'cached-property==1.5.2', 'cerberus==1.3.4', 'certifi==2021.10.8', "chardet==4.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "charset-normalizer==2.0.12; python_full_version >= '3.5.0'", "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", 'distlib==0.3.4', "frozenlist==1.3.0; python_version >= '3.7'", "idna==3.3; python_version >= '3'", "multidict==6.0.2; python_version >= '3.7'", 'orderedmultidict==1.0.1', "packaging==20.9; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", 'pep517==0.12.0', "pip==22.0.4; python_version >= '3.7'", "pip-shims==0.6.0; python_version >= '3.6'", 'pipenv-setup==3.2.0', 'pipfile==0.0.2', "platformdirs==2.5.1; python_version >= '3.7'", "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'", "pyparsing==3.0.7; python_version >= '3.6'", "python-dateutil==2.8.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'", 'requests==2.27.1', "requirementslib==1.6.1; python_version >= '3.6'", "setuptools==60.9.3; python_version >= '3.7'", "six==1.16.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2'", "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2'", "tomli==2.0.1; python_version >= '3.6'", "tomlkit==0.10.0; python_version >= '3.6' and python_version < '4.0'", "urllib3==1.26.8; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4.0'", "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'", "wheel==0.37.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'", "yarl==1.7.2; python_version >= '3.6'"],
    name="monitor",
    version="0.1.1",
    description="Build monitor GPIO",
    long_description=readme,
    author="Matthew Z Worthington",
    author_email="worthingtown@gmail.com",
    url="https://github.com/worthington10TW/gpio-build-monitor",
    include_package_data=True,
    license=license,
    packages=find_packages(
        include=("monitor", "monitor.*"), exclude=("test", "text.*")
    ),
    entry_points={"console_scripts": ["monitor=monitor.app:main"]},
    package_data={"integrations.yml": ["monitor/integrations.yml"]},
    )