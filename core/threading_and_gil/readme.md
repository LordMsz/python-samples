# Python Threading and GIL Demos

This folder contains demonstrations of Python's threading model, the Global Interpreter Lock (GIL), and modern concurrency features.

## What's Inside

### async_threading_gil_demo.py
Demonstrates the fundamentals of Python's concurrency model:
- **GIL behavior**: Shows how the Global Interpreter Lock affects multi-threaded execution
- **CPU-bound vs I/O-bound tasks**: Compares threading performance for different workload types
- **Async/await**: Demonstrates cooperative multitasking for I/O operations

**Key concepts**: GIL limitations, thread scheduling, async I/O, concurrent futures

### modern_python_concurrency.py
Showcases new concurrency features in Python 3.12+ and 3.13+:
- **Python 3.12**: Per-interpreter GIL with subinterpreters (PEP 684)
- **Python 3.13**: Experimental free-threading mode (PEP 703, no-GIL build)
- **Version detection**: Automatically detects your Python version and available features

**Key concepts**: Subinterpreters, free-threading, GIL removal, parallel CPU execution

**Note**: Free-threading requires a special Python 3.13 build (`python3.13t`) compiled with `--disable-gil`. The standard Python 3.13 installation always has GIL enabled - there's no environment variable to disable it at runtime.

## Running the Demos

```bash
# Basic GIL and threading demo
python async_threading_gil_demo.py

# Modern concurrency features (Python 3.12+)
python modern_python_concurrency.py
```

**WSL Tip**: For better performance in WSL2, keep files in the Linux filesystem (`~/projects`) rather than accessing through `/mnt/c/`.

## What You'll Learn

- Why Python is multi-threaded but not truly parallel (due to GIL)
- When to use threading vs async for concurrent operations
- How Python 3.12+ improves parallel execution with subinterpreters
- The future of Python concurrency with free-threading in 3.13+
