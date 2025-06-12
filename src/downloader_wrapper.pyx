# cython: language_level=3
"""
Cython wrapper for the downloader module.
This file defines the C-compatible functions that will be exposed in the DLL.
"""

import os
import sys
from libc.stdlib cimport malloc, free
from libc.string cimport strcpy, strlen

# Import our Python module
from src import downloader

# Define a C-compatible function that will be exposed in the DLL
cdef public int download_from_url(const char* url_c):
    """
    C-compatible function that downloads content from a URL.

    Args:
        url_c: The URL to download from (as a C string)

    Returns:
        1 if successful, 0 if failed
    """
    # Convert C string to Python string
    url = url_c.decode('utf-8')

    # Call our Python function
    result = downloader.download_video(url)

    return result

cdef public int delete_file(const char* file_path_c):
    """
    C-compatible function that deletes a specified file.

    Args:
        file_path_c: The path to the file to delete (as a C string)

    Returns:
        1 if successful, 0 if failed
    """
    # Convert C string to Python string
    file_path = file_path_c.decode('utf-8')

    # Call our Python function
    result = downloader.delete_file(file_path)

    return result