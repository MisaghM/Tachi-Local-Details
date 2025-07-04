from pathlib import Path
from setuptools import setup, find_packages


PROGRAM_NAME = "tachi-local"
PROJECT_DIR = "tachi_local"


here = Path(__file__).resolve().parent
src_path = here / PROJECT_DIR

readme = (here / "README.md").read_text(encoding="utf-8")

version = {}
exec((src_path / "version.py").read_text(encoding="utf-8"), version)
version = version["__version__"]


setup(
    name=PROGRAM_NAME,
    version=version,
    description="Tachiyomi local manga 'details.json' creator.",
    long_description=readme,
    long_description_content_type='text/markdown',
    url="https://github.com/MisaghM/Tachi-Local-Details/",
    author="MisaghM",
    keywords=["tachiyomi", "mihon", "manga"],
    python_requires=">=3.7",
    packages=find_packages(exclude=["test", "tests"]),
    install_requires=[
        "beautifulsoup4>=4.12.3",
        "requests>=2.31.0"
    ],
    entry_points={
        "console_scripts": [f"{PROGRAM_NAME}={PROJECT_DIR}.main:main"],
    },
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Topic :: Games/Entertainment"
    ]
)
