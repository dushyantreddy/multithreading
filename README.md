# Python Multithreading Assignment

This repository contains Python scripts demonstrating multithreaded implementations of sorting algorithms and a file downloader.

## Files

*   `merge_sort.py`: Implements single-threaded and multi-threaded merge sort.
*   `quicksort.py`: Implements single-threaded and multi-threaded quicksort.
*   `file_downloader.py`: Implements sequential and concurrent file downloading.
*   `urls.txt`: Sample input file containing URLs for `file_downloader.py`.
*   `README.md`: This file.

## Setup

1.  **Python:** Ensure Python 3 is installed.
2.  **Dependencies:** Install the `requests` library needed for `file_downloader.py`:
    ```bash
    pip install requests
    ```

## How to Run

Execute the scripts from your terminal.

1.  **Merge Sort:**
    ```bash
    python merge_sort.py
    ```
    Compares the execution time of single-threaded vs multi-threaded merge sort on a random list.

2.  **Quicksort:**
    ```bash
    python quicksort.py
    ```
    Compares the execution time of single-threaded vs multi-threaded quicksort on a random list.

3.  **File Downloader:**
    ```bash
    python file_downloader.py
    ```
    Downloads files listed in `urls.txt` (or default URLs if the file is missing/empty) both sequentially and concurrently using threads. It compares the total time taken. Downloaded files are saved in a `downloads/` directory.

## Approach Summary

*   **Sorting (`merge_sort.py`, `quicksort.py`):**
    *   The multi-threaded versions create new threads for recursive sub-problems up to a defined `MAX_DEPTH`.
    *   Beyond `MAX_DEPTH`, sorting continues sequentially within the existing thread to limit thread overhead.
    *   Performance is compared against standard single-threaded versions. Gains might be limited for CPU-bound tasks in CPython due to the GIL.
*   **File Downloader (`file_downloader.py`):**
    *   Compares downloading files one after another (sequential) vs. using a separate thread for each download (concurrent).
    *   Concurrent downloading is expected to be significantly faster for I/O-bound tasks like network requests, as threads can wait for network responses independently.
