from setuptools import setup

setup(
    name="bqformat",
    packages=["bqformat"],
    package_dir={"bqformat": "src/bqformat"},
    package_data={"bqformat": ["data/*.txt"]},
    entry_points={"console_scripts": ["bqformat=bqformat.main:main",],},
)
