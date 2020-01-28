from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="csquizgen",
    version="0.0.1",
    author="Kenji Imasaki",
    author_email="kenji.imasaki@sijp.org",
    description="CS Quiz Generator",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://csinenglish.club",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)