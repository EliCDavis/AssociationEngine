import os
from setuptools import setup
from setuptools import find_packages

README = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'README.md')

setup(
    name="association_engine",
    version="0.1.4",
    packages=find_packages(),
    author="Senior Design Team MSU",
    author_email="ecd157@msstate.edu",
    description="Correlation values between variables",
    license="MIT",
    keywords="association correlation spearman",
    url="https://github.com/EliCDavis/AssociationEngine",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        "numpy>=1.12.0,<2.0.0",
        "scipy>=0.18.1,<0.19.0"
    ],
)
