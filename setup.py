from setuptools import find_packages
from distutils.core import setup

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
    )