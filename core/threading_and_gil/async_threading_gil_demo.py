"""
Python Async, Threading, and GIL Demo
======================================

This example demonstrates three key concepts:
1. **GIL (Global Interpreter Lock)**: Only one thread executes Python bytecode at a time
2. **Multi-threading**: Python IS multi-threaded, but threads share the GIL
3. **Async/Await**: Cooperative multitasking that releases GIL during I/O operations

Key Takeaways:
- Python is NOT single-threaded (it can run multiple threads)
- GIL ensures only ONE thread executes Python code at a time
- CPU-bound tasks don't benefit from threading (GIL blocks parallel execution)
- I/O-bound tasks benefit from threading (GIL is released during I/O)
- Async is best for I/O-bound tasks with many concurrent operations
"""

import time
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor


# ============================================================================
# PART 1: CPU-Bound Task - GIL BLOCKS parallel execution
# ============================================================================

def cpu_bound_task(n):
    """Simulates CPU-intensive work (GIL stays locked)"""
    count = 0
    for i in range(n):
        count += i ** 2
    return count


def demo_cpu_bound_with_gil():
    """Shows that multi-threading DOESN'T help CPU-bound tasks due to GIL"""
    print("\n" + "="*60)
    print("DEMO 1: CPU-Bound Task (GIL Blocks Parallelism)")
    print("="*60)
    
    iterations = 10_000_000
    
    # Single-threaded execution
    start = time.perf_counter()
    cpu_bound_task(iterations)
    cpu_bound_task(iterations)
    single_time = time.perf_counter() - start
    print(f"Single-threaded: {single_time:.3f} seconds")
    
    # Multi-threaded execution (still serial due to GIL!)
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=2) as executor:
        future1 = executor.submit(cpu_bound_task, iterations)
        future2 = executor.submit(cpu_bound_task, iterations)
        future1.result()
        future2.result()
    multi_time = time.perf_counter() - start
    print(f"Multi-threaded:  {multi_time:.3f} seconds")
    
    print(f"\n💡 Notice: Multi-threading is NOT faster for CPU tasks!")
    print(f"   Reason: GIL allows only ONE thread to execute Python code at a time")


# ============================================================================
# PART 2: I/O-Bound Task - GIL RELEASES during I/O
# ============================================================================

def io_bound_task(task_id, sleep_time):
    """Simulates I/O operation (file, network, etc.) - GIL is released"""
    print(f"  Task {task_id} started (thread: {threading.current_thread().name})")
    time.sleep(sleep_time)  # GIL is RELEASED during sleep/I/O!
    print(f"  Task {task_id} completed")
    return task_id


def demo_io_bound_with_threading():
    """Shows that multi-threading DOES help I/O-bound tasks"""
    print("\n" + "="*60)
    print("DEMO 2: I/O-Bound Task (GIL Releases During I/O)")
    print("="*60)
    
    sleep_time = 0.5
    num_tasks = 4
    
    # Single-threaded execution
    print("\nSingle-threaded I/O:")
    start = time.perf_counter()
    for i in range(num_tasks):
        io_bound_task(i, sleep_time)
    single_time = time.perf_counter() - start
    print(f"Total time: {single_time:.3f} seconds")
    
    # Multi-threaded execution (runs concurrently!)
    print("\nMulti-threaded I/O:")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(io_bound_task, i, sleep_time) for i in range(num_tasks)]
        for future in futures:
            future.result()
    multi_time = time.perf_counter() - start
    print(f"Total time: {multi_time:.3f} seconds")
    
    print(f"\n💡 Notice: Multi-threading IS faster for I/O tasks!")
    print(f"   Reason: GIL is RELEASED during I/O operations (sleep, network, disk)")


# ============================================================================
# PART 3: Async/Await - Cooperative Multitasking
# ============================================================================

async def async_io_task(task_id, sleep_time):
    """Async I/O operation - cooperative multitasking"""
    print(f"  Async task {task_id} started")
    await asyncio.sleep(sleep_time)  # Yields control to event loop
    print(f"  Async task {task_id} completed")
    return task_id


async def demo_async_io():
    """Shows async/await for concurrent I/O operations"""
    print("\n" + "="*60)
    print("DEMO 3: Async/Await (Cooperative Multitasking)")
    print("="*60)
    
    sleep_time = 0.5
    num_tasks = 4
    
    print("\nAsync I/O (all tasks run concurrently):")
    start = time.perf_counter()
    tasks = [async_io_task(i, sleep_time) for i in range(num_tasks)]
    await asyncio.gather(*tasks)
    async_time = time.perf_counter() - start
    print(f"Total time: {async_time:.3f} seconds")
    
    print(f"\n💡 Notice: Async is also fast for I/O tasks!")
    print(f"   Reason: Tasks cooperatively yield control during I/O")
    print(f"   Benefit: More lightweight than threads (no thread overhead)")


# ============================================================================
# PART 4: Visualizing Thread Execution
# ============================================================================

def demonstrate_threads_are_real():
    """Proves Python uses real threads (not single-threaded!)"""
    print("\n" + "="*60)
    print("DEMO 4: Python IS Multi-Threaded!")
    print("="*60)
    
    def worker(name):
        print(f"  Thread '{name}' | Thread ID: {threading.get_ident()} | Native ID: {threading.get_native_id()}")
        time.sleep(0.1)
    
    print("\nCreating 3 threads with different IDs:")
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"Worker-{i}",))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()
    
    print(f"\n💡 Notice: Each thread has a unique ID!")
    print(f"   Python IS multi-threaded, but GIL ensures only ONE executes at a time")


# ============================================================================
# SUMMARY
# ============================================================================

def print_summary():
    """Prints a summary of key concepts"""
    print("\n" + "="*60)
    print("SUMMARY: Async, Threading, and GIL")
    print("="*60)
    print("""
✅ Python IS multi-threaded (multiple threads can exist)
✅ GIL (Global Interpreter Lock) allows only ONE thread to execute Python code at a time
✅ GIL is RELEASED during I/O operations (sleep, network, disk)
✅ GIL is HELD during CPU-bound operations

When to use what:
├─ CPU-bound tasks    → Use multiprocessing (separate processes, separate GILs)
├─ I/O-bound tasks    → Use threading OR async/await
└─ Many I/O tasks     → Use async/await (more efficient, less overhead)

Async vs Threading:
├─ Async: Single-threaded, cooperative multitasking, lightweight
└─ Threading: Multi-threaded, preemptive multitasking, more overhead

Remember: Python is NOT single-threaded, it's GIL-limited!
""")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n🐍 Python Async, Threading, and GIL Demo 🐍")
    
    demo_cpu_bound_with_gil()
    demo_io_bound_with_threading()
    asyncio.run(demo_async_io())
    demonstrate_threads_are_real()
    print_summary()


if __name__ == "__main__":
    main()
