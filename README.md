# YouTube Downloader DLL

A DLL for downloading content from URLs using yt-dlp.

## Features

- Downloads videos from URLs using yt-dlp
- Outputs downloaded files to the 'output' directory
- Can be used as a Python module or compiled into a DLL

## Requirements

- Python 3.6+
- yt-dlp
- Cython
- A C compiler (e.g., Microsoft Visual C++ Build Tools)

## Installation

1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Building the DLL

To build the DLL, run:

```
python setup.py build_ext --inplace
```

This will create a `downloader_dll.pyd` file (on Windows) or a `downloader_dll.so` file (on Linux/macOS), which is the DLL that can be used in other applications.

## Usage

### As a Python Module

```python
import downloader

# Download a video
result = downloader.download_from_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
if result:
    print(f"Successfully downloaded to: {result}")
else:
    print("Download failed")
```

### From Command Line

```
python downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Using the DLL

The DLL exports a function `download_from_url` that takes a URL as a C string and returns 1 if the download was successful, 0 otherwise.

#### C++ Example

An example of how to use the DLL from C++ code is provided in `example_usage.cpp`. To compile and run the example:

1. Build the DLL using the provided batch file:
   ```
   build_dll.bat
   ```

2. Compile the C++ example (with Visual Studio):
   ```
   cl /EHsc example_usage.cpp /link downloader_dll.lib
   ```

3. Run the example:
   ```
   example_usage.exe https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
