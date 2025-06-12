/**
 * Example of how to use the downloader_dll from C++ code.
 * 
 * To compile (with Visual Studio):
 * cl /EHsc example_usage.cpp /link downloader_dll.lib
 */

#include <iostream>
#include <string>
#include <windows.h>

// Define the function types for the DLL functions
typedef int (*DownloadFromUrlFunc)(const char*);
typedef int (*DeleteFileFunc)(const char*);

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "Usage: example_usage <url> [--delete]" << std::endl;
        std::cout << "Example: example_usage https://www.youtube.com/watch?v=dQw4w9WgXcQ" << std::endl;
        std::cout << "Add --delete to test the file deletion functionality" << std::endl;
        return 1;
    }

    const char* url = argv[1];

    // Check if we should delete the file after downloading
    bool delete_after_download = false;
    for (int i = 2; i < argc; i++) {
        if (std::string(argv[i]) == "--delete") {
            delete_after_download = true;
            break;
        }
    }

    // Load the DLL
    HMODULE hDLL = LoadLibrary("downloader_dll.pyd");
    if (hDLL == NULL) {
        std::cerr << "Failed to load DLL. Error code: " << GetLastError() << std::endl;
        return 1;
    }

    // Get the download function address
    DownloadFromUrlFunc download_from_url = (DownloadFromUrlFunc)GetProcAddress(hDLL, "download_from_url");
    if (download_from_url == NULL) {
        std::cerr << "Failed to get download function address. Error code: " << GetLastError() << std::endl;
        FreeLibrary(hDLL);
        return 1;
    }

    // Get the delete function address if needed
    DeleteFileFunc delete_file = NULL;
    if (delete_after_download) {
        delete_file = (DeleteFileFunc)GetProcAddress(hDLL, "delete_file");
        if (delete_file == NULL) {
            std::cerr << "Failed to get delete function address. Error code: " << GetLastError() << std::endl;
            FreeLibrary(hDLL);
            return 1;
        }
    }

    // Call the download function
    std::cout << "Downloading from URL: " << url << std::endl;
    int result = download_from_url(url);

    if (result) {
        std::cout << "Download successful!" << std::endl;

        // Test file deletion if requested
        if (delete_after_download) {
            std::string file_path;
            std::cout << "Enter the path of the file to delete: ";
            std::getline(std::cin, file_path);

            if (!file_path.empty()) {
                std::cout << "Deleting file: " << file_path << std::endl;
                int delete_result = delete_file(file_path.c_str());

                if (delete_result) {
                    std::cout << "File deletion successful!" << std::endl;
                } else {
                    std::cout << "File deletion failed." << std::endl;
                }
            } else {
                std::cout << "No file path provided, skipping deletion." << std::endl;
            }
        }
    } else {
        std::cout << "Download failed." << std::endl;
    }

    // Unload the DLL
    FreeLibrary(hDLL);

    return 0;
}
