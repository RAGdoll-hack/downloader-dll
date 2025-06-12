import os
import sys
import ctypes
import re
import requests
from typing import Optional, Union
from urllib.parse import urlparse

# We'll need to install yt-dlp when building the DLL
try:
    import yt_dlp
except ImportError:
    print("yt-dlp not installed. Please install it with: pip install yt-dlp")
    sys.exit(1)

def is_direct_media_url(url: str) -> bool:
    """
    Check if the URL is a direct link to a media file.

    Args:
        url: The URL to check

    Returns:
        True if the URL is a direct media file link, False otherwise
    """
    # Parse the URL
    parsed_url = urlparse(url)

    # Check if the path ends with a common video or audio extension
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg']
    audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac', '.flac']

    path = parsed_url.path.lower()
    return any(path.endswith(ext) for ext in video_extensions + audio_extensions)

def download_direct_file(url: str, output_dir: str) -> Optional[str]:
    """
    Download a file directly from a URL using requests.

    Args:
        url: The URL to download from
        output_dir: The directory to save the downloaded file to

    Returns:
        The path to the downloaded file or None if download failed
    """
    try:
        # Parse the URL to get the filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)

        if not filename:
            filename = "downloaded_file.mp4"

        # Create the full output path
        output_path = os.path.join(output_dir, filename)

        # Download the file with streaming to handle large files
        print(f"Downloading file directly from: {url}")
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Get the total file size if available
        total_size = int(response.headers.get('content-length', 0))

        # Write the file
        with open(output_path, 'wb') as f:
            if total_size > 0:
                print(f"Total file size: {total_size / (1024 * 1024):.2f} MB")
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        # Print progress
                        progress = downloaded / total_size * 100
                        if downloaded % (1024 * 1024) < 8192:  # Update roughly every 1MB
                            print(f"Downloaded: {downloaded / (1024 * 1024):.2f} MB ({progress:.2f}%)")
            else:
                print("Unknown file size. Downloading...")
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

        print(f"Successfully downloaded file to: {output_path}")
        return output_path

    except Exception as e:
        print(f"Error downloading direct file: {e}")
        return None

def download_from_url(url: str, output_dir: str = "output") -> Optional[str]:
    """
    Download video content from a URL to the specified output directory.
    Handles both direct file URLs and platform-specific URLs (YouTube, Vimeo, etc.).
    Attempts to download in mp4 format when possible.

    Args:
        url: The URL to download from
        output_dir: The directory to save the downloaded content to (default: "output")

    Returns:
        The path to the downloaded file or None if download failed
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Check if this is a direct media file URL
        if is_direct_media_url(url):
            return download_direct_file(url, output_dir)

        # For platform-specific URLs, use yt-dlp
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestvideo[ext!=webm]+bestaudio[ext!=webm]/best[ext!=webm]/best',  # Prefer non-webm formats with fallback
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,  # Continue on download errors
            'nocheckcertificate': True,  # Bypass SSL certificate verification
            'geo_bypass': True,  # Bypass geo-restrictions
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Convert to mp4 after download
            }],
        }

        # First, extract info without downloading to check available formats
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=False)

                # Check if info_dict is None (extraction failed)
                if info_dict is None:
                    print(f"Failed to extract info from URL: {url}")
                    return None

                # Check if there are video formats available
                formats = info_dict.get('formats', [])
                video_formats = [f for f in formats if f.get('vcodec') != 'none' and not f.get('vcodec', '').startswith('image')]

                if not video_formats:
                    print(f"No video formats available for URL: {url}")
                    return None

                # Download the video
                info = ydl.extract_info(url, download=True)

                # Check if info is None (download failed)
                if info is None:
                    print(f"Failed to download video from URL: {url}")
                    return None

                if 'entries' in info:
                    # Playlist
                    entries = info.get('entries', [])
                    if not entries:
                        print(f"No entries found in playlist: {url}")
                        return None

                    entry = entries[0]
                    title = entry.get('title', 'unknown_title')
                    # Use mp4 as the extension since we're converting to mp4
                    file_path = os.path.join(output_dir, f"{title}.mp4")
                else:
                    # Single video
                    title = info.get('title', 'unknown_title')
                    # Use mp4 as the extension since we're converting to mp4
                    file_path = os.path.join(output_dir, f"{title}.mp4")

                # Check if the file exists
                if os.path.exists(file_path):
                    print(f"Successfully downloaded video to: {file_path}")
                    return file_path
                else:
                    print(f"File not found after download: {file_path}")
                    return None

            except Exception as e:
                print(f"Error during info extraction or download: {e}")
                return None
    except Exception as e:
        print(f"Error downloading from URL: {e}")
        return None

# Functions to be exported in the DLL
def download_video(url: str) -> int:
    """
    Function to be exported in the DLL.
    Downloads a video from the given URL to the 'output' directory.

    Args:
        url: The URL to download from

    Returns:
        1 if successful, 0 if failed
    """
    result = download_from_url(url)
    return 1 if result else 0

def delete_file(file_path: str) -> int:
    """
    Function to be exported in the DLL.
    Deletes the specified file.

    Args:
        file_path: The path to the file to delete

    Returns:
        1 if successful, 0 if failed
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return 1
        else:
            print(f"File not found: {file_path}")
            return 0
    except Exception as e:
        print(f"Error deleting file: {e}")
        return 0

# For testing the script directly
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        result = download_from_url(url)
        if result:
            print(f"Successfully downloaded to: {result}")
        else:
            print("Download failed")
    else:
        print("Usage: python downloader.py <url>")