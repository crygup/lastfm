from setuptools import setup

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="lastfm",
    version="1.0.4",
    description="python last.fm api wrapper",
    packages=["lastfm"],
    python_requires=">=3.8",
    install_requires=requirements,
)
