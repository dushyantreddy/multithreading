import threading
import time
import random
import copy

MAX_DEPTH = 3 # Controls max threads (approx 2^MAX_DEPTH)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_single_threaded(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left_sorted = merge_sort_single_threaded(arr[:mid])
    right_sorted = merge_sort_single_threaded(arr[mid:])
    return merge(left_sorted, right_sorted)

def merge_sort_multi_threaded(arr, depth=0):
    if len(arr) <= 1:
        return arr

    if depth >= MAX_DEPTH:
        return merge_sort_single_threaded(arr)

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    result_container = {}

    def thread_target(arr_part, depth_level, container, key):
        container[key] = merge_sort_multi_threaded(arr_part, depth_level)

    right_thread = threading.Thread(target=thread_target,
                                    args=(right_half, depth + 1, result_container, 'right'))
    right_thread.start()

    left_sorted = merge_sort_multi_threaded(left_half, depth + 1)

    right_thread.join()
    right_sorted = result_container['right']

    return merge(left_sorted, right_sorted)

if __name__ == "__main__":
    list_size = 20000
    max_value = 100000
    print(f"Generating a list of {list_size} random integers...")
    random_list = [random.randint(0, max_value) for _ in range(list_size)]

    # Single-threaded
    list_to_sort_single = copy.deepcopy(random_list)
    print("\nStarting single-threaded merge sort...")
    start_time_single = time.time()
    sorted_list_single = merge_sort_single_threaded(list_to_sort_single)
    end_time_single = time.time()
    time_single = end_time_single - start_time_single
    print(f"Single-threaded time: {time_single:.6f} seconds")

    # Multi-threaded
    list_to_sort_multi = copy.deepcopy(random_list)
    print(f"\nStarting multi-threaded merge sort (max_depth={MAX_DEPTH})...")
    start_time_multi = time.time()
    sorted_list_multi = merge_sort_multi_threaded(list_to_sort_multi, depth=0)
    end_time_multi = time.time()
    time_multi = end_time_multi - start_time_multi
    print(f"Multi-threaded time: {time_multi:.6f} seconds")

    # Comparison
    print("\n--- Comparison ---")
    print(f"List size: {list_size}")
    print(f"Single-threaded time: {time_single:.6f} seconds")
    print(f"Multi-threaded time (max_depth={MAX_DEPTH}): {time_multi:.6f} seconds")