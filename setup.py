from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pyct",
    version="0.1.0",
    author="Youssef Sidhom",
    author_email="youssefsidhom8@gmail.com",
    description="A Python wrapper for the ClinicalTrials.gov API (v2) with full pagination support and a few extra features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUSSEFSAIDHOM/pyct",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests",
        "pandas",
        "tqdm",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
    ],
)