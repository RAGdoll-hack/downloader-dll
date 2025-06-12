from setuptools import setup, Extension
from Cython.Build import cythonize
import os

# Create a Cython extension module
ext_modules = [
    Extension(
        "downloader_dll",
        sources=["src/downloader_wrapper.pyx"],
        libraries=[]
    )
]

# Setup configuration
setup(
    name="downloader_dll",
    version="1.0.0",
    description="A DLL for downloading content from URLs using yt-dlp",
    author="",
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': "3"}),
    install_requires=[
        "yt-dlp",
        "Cython",
        "requests",
    ],
)
