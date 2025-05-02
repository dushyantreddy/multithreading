import threading
import time
import requests
import os
import sys
from urllib.parse import urlparse

DOWNLOAD_DIR = "downloads"
URL_FILE = "urls.txt"

def download_file(url, index):
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path) if parsed_url.path else f"download_{index+1}.file"
        if not filename: filename = f"download_{index+1}.file" # Ensure filename exists
        filepath = os.path.join(DOWNLOAD_DIR, filename)

        print(f"[Thread {threading.current_thread().name}] Downloading {url} ...")
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk: f.write(chunk)
        print(f"[Thread {threading.current_thread().name}] Finished {url}")
        return url, True, None

    except Exception as e:
        print(f"[Thread {threading.current_thread().name}] ERROR downloading {url}: {e}")
        return url, False, str(e)

def download_sequentially(urls):
    print("\n--- Starting Sequential Download ---")
    start_time = time.time()
    results = [download_file(url, i) for i, url in enumerate(urls)]
    end_time = time.time()
    time_taken = end_time - start_time

    success_count = sum(1 for _, success, _ in results if success)
    error_count = len(urls) - success_count

    print("\n--- Sequential Download Complete ---")
    print(f"Total time taken: {time_taken:.2f} seconds")
    print(f"Successfully downloaded: {success_count} files")
    print(f"Errors: {error_count} files")
    return time_taken

def download_concurrently(urls):
    print("\n--- Starting Concurrent Download ---")
    start_time = time.time()
    threads = []
    results = [] # Shared list to store results

    # Wrapper needed to append result to the shared list
    def thread_target(url, index, result_list):
        result = download_file(url, index)
        result_list.append(result)

    for i, url in enumerate(urls):
        thread_name = f"Downloader-{i+1}"
        thread = threading.Thread(target=thread_target, args=(url, i, results), name=thread_name)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    time_taken = end_time - start_time

    success_count = sum(1 for _, success, _ in results if success)
    error_count = len(urls) - success_count

    print("\n--- Concurrent Download Complete ---")
    print(f"Total time taken: {time_taken:.2f} seconds")
    print(f"Successfully downloaded: {success_count} files")
    print(f"Errors: {error_count} files")
    return time_taken

if __name__ == "__main__":
    default_urls = [
        "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
        "https://raw.githubusercontent.com/git/git/master/README.md",
        "https://httpbin.org/delay/2", # 2 second delay
        "https://httpbin.org/image/jpeg",
        "https://this.url.will.fail/probably.zip"
    ]

    urls_to_download = []
    if os.path.exists(URL_FILE):
        try:
            with open(URL_FILE, 'r') as f:
                urls_to_download = [line.strip() for line in f if line.strip()]
            if not urls_to_download:
                print(f"Warning: '{URL_FILE}' is empty. Using default URLs.")
                urls_to_download = default_urls
            else:
                print(f"Loaded {len(urls_to_download)} URLs from '{URL_FILE}'.")
        except Exception as e:
            print(f"Error reading '{URL_FILE}': {e}. Using default URLs.")
            urls_to_download = default_urls
    else:
        print(f"'{URL_FILE}' not found. Using default URLs.")
        urls_to_download = default_urls

    if not urls_to_download:
        print("No URLs to download. Exiting.")
        sys.exit(1)

    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    print(f"Downloads will be saved in './{DOWNLOAD_DIR}/'")

    time_sequential = download_sequentially(urls_to_download)
    time_concurrent = download_concurrently(urls_to_download)

    print("\n--- Comparison Summary ---")
    print(f"Number of files to download: {len(urls_to_download)}")
    print(f"Sequential download time: {time_sequential:.2f} seconds")
    print(f"Concurrent download time: {time_concurrent:.2f} seconds")

    if time_concurrent > 0:
      speedup = time_sequential / time_concurrent
      print(f"Speedup: {speedup:.2f}x")