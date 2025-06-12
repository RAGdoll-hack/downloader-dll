"""
Test script to demonstrate how to use the downloader module directly.
"""

import sys
import os
from src import downloader

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_downloader.py <url> [--delete]")
        print("Example: python test_downloader.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        print("Add --delete to test the file deletion functionality")
        return

    url = sys.argv[1]
    delete_after_download = "--delete" in sys.argv

    print(f"Downloading from URL: {url}")

    result = downloader.download_from_url(url)

    if result:
        print(f"Successfully downloaded to: {result}")

        # Test file deletion if requested
        if delete_after_download:
            print(f"Testing file deletion for: {result}")
            if os.path.exists(result):
                delete_result = downloader.delete_file(result)
                if delete_result:
                    print(f"Successfully deleted file: {result}")
                    # Verify the file is actually gone
                    if not os.path.exists(result):
                        print("Verified: File no longer exists")
                    else:
                        print("Error: File still exists despite successful deletion report")
                else:
                    print(f"Failed to delete file: {result}")
            else:
                print(f"Warning: File {result} does not exist, cannot test deletion")
    else:
        print("Download failed")

if __name__ == "__main__":
    main()