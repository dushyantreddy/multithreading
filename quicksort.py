import threading
import time
import random
import copy
import sys

# sys.setrecursionlimit(2000) # Uncomment if facing recursion depth issues

MAX_DEPTH = 3 # Controls max threads (approx 2^MAX_DEPTH)

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1

def quicksort_single_threaded_recursive(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quicksort_single_threaded_recursive(arr, low, pi - 1)
        quicksort_single_threaded_recursive(arr, pi + 1, high)

def quicksort_single_threaded(arr):
    quicksort_single_threaded_recursive(arr, 0, len(arr) - 1)

def quicksort_multi_threaded_recursive(arr, low, high, depth=0):
    if low < high:
        pi = partition(arr, low, high)

        if depth < MAX_DEPTH:
            left_thread = threading.Thread(target=quicksort_multi_threaded_recursive,
                                           args=(arr, low, pi - 1, depth + 1))
            right_thread = threading.Thread(target=quicksort_multi_threaded_recursive,
                                            args=(arr, pi + 1, high, depth + 1))
            left_thread.start()
            right_thread.start()
            left_thread.join()
            right_thread.join()
        else:
            # Depth limit reached, continue sequentially
            quicksort_multi_threaded_recursive(arr, low, pi - 1, depth + 1)
            quicksort_multi_threaded_recursive(arr, pi + 1, high, depth + 1)

def quicksort_multi_threaded(arr):
    quicksort_multi_threaded_recursive(arr, 0, len(arr) - 1, depth=0)

if __name__ == "__main__":
    list_size = 20000
    max_value = 100000
    print(f"Generating a list of {list_size} random integers...")
    random_list = [random.randint(0, max_value) for _ in range(list_size)]

    # Single-threaded
    list_to_sort_single = copy.deepcopy(random_list)
    print("\nStarting single-threaded quicksort...")
    start_time_single = time.time()
    quicksort_single_threaded(list_to_sort_single)
    end_time_single = time.time()
    time_single = end_time_single - start_time_single
    print(f"Single-threaded time: {time_single:.6f} seconds")

    # Multi-threaded
    list_to_sort_multi = copy.deepcopy(random_list)
    print(f"\nStarting multi-threaded quicksort (max_depth={MAX_DEPTH})...")
    start_time_multi = time.time()
    quicksort_multi_threaded(list_to_sort_multi)
    end_time_multi = time.time()
    time_multi = end_time_multi - start_time_multi
    print(f"Multi-threaded time: {time_multi:.6f} seconds")

    # Comparison
    print("\n--- Comparison ---")
    print(f"List size: {list_size}")
    print(f"Single-threaded time: {time_single:.6f} seconds")
    print(f"Multi-threaded time (max_depth={MAX_DEPTH}): {time_multi:.6f} seconds")