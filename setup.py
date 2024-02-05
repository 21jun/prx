from setuptools import setup, find_packages

setup(
    name="prx",
    version="0.0.1",
    packages=find_packages(),
    package_data={
        "": [
            "rsync_box.sh",
        ]
    },
    entry_points={
        "console_scripts": [
            "prx=main:main",
        ],
    },
)
