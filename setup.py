from setuptools import setup, find_packages

with open("README.md") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
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
    package_data={"integrations.json": ["monitor/integrations.json"]},
    install_requires=[
        "aiohttp==3.7.4",
        "aioresponses==0.7.1",
        "appdirs==1.4.4",
        "async-timeout==3.0.1; python_full_version >= '3.5.3'",
        "asyncio==3.4.3",
        "attrs==20.3.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "black==19.10b0; python_version >= '3.6'",
        "cached-property==1.5.2",
        "cerberus==1.3.2",
        "certifi==2020.12.5",
        "chardet==3.0.4",
        "click==7.1.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "colorama==0.4.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "distlib==0.3.1",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "multidict==5.1.0; python_version >= '3.6'",
        "orderedmultidict==1.0.1",
        "packaging==20.8; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pathspec==0.8.1",
        "pep517==0.9.1",
        "pip-shims==0.5.3; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "pipenv-setup==3.1.1",
        "pipfile==0.0.2",
        "plette[validation]==0.2.3; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "regex==2020.11.13",
        "requests==2.25.1",
        "requirementslib==1.5.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "toml==0.10.2; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "tomlkit==0.7.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "typed-ast==1.4.2",
        "typing-extensions==3.7.4.3",
        "urllib3==1.26.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "vistir==0.5.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "wheel==0.36.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "yarl==1.6.3; python_version >= '3.6'",
    ],
)
