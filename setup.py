from setuptools import setup, find_packages

setup(
    name="ytls",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "PyYAML",
        "deepdiff"
        # add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "ytls = ytls.cli:main"
        ]
    },
)
