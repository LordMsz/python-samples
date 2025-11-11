"""
Modern Python Concurrency: 3.12 and 3.13
=========================================

This demonstrates the evolution of Python's concurrency model:

Python 3.12 (Oct 2023):
- PEP 684: Per-interpreter GIL (subinterpreters)
- Each subinterpreter has its own GIL
- True parallel execution across subinterpreters

Python 3.13 (Oct 2024):
- PEP 703: Experimental free-threading mode (no-GIL)
- Build with --disable-gil or use python3.13t
- True parallel CPU-bound execution in regular threads

This script detects your Python version and demonstrates available features.
"""

import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Version detection
PY_VERSION = sys.version_info
PY_312_PLUS = PY_VERSION >= (3, 12)
PY_313_PLUS = PY_VERSION >= (3, 13)

# Check for free-threading (Python 3.13+)
FREE_THREADING = hasattr(sys, '_is_gil_enabled') and not sys._is_gil_enabled()


# ============================================================================
# VERSION INFO
# ============================================================================

def print_version_info():
    """Display current Python version and capabilities"""
    print("\n" + "="*70)
    print(f"🐍 Python {PY_VERSION.major}.{PY_VERSION.minor}.{PY_VERSION.micro}")
    print("="*70)
    
    if FREE_THREADING:
        print("✓ FREE-THREADING ENABLED (GIL disabled!)")
        print("  → True parallel multi-threading available")
    else:
        print("✗ Traditional GIL mode (default)")
        print("  → Only one thread executes Python code at a time")
    
    print(f"\nCapabilities:")
    print(f"  • Per-interpreter GIL (PEP 684):  {'✓ Available' if PY_312_PLUS else '✗ Requires 3.12+'}")
    print(f"  • Free-threading (PEP 703):       {'✓ Available' if PY_313_PLUS else '✗ Requires 3.13+'}")
    
    if PY_313_PLUS and not FREE_THREADING:
        print(f"\n💡 To enable free-threading:")
        print(f"   • Install: python3.13t (t = free-threading build)")
        print(f"   • Or build with: ./configure --disable-gil")
        print(f"   • Or set env: PYTHON_GIL=0")


# ============================================================================
# CPU-Bound Benchmark - Shows GIL impact
# ============================================================================

def cpu_intensive(n):
    """CPU-intensive calculation"""
    result = 0
    for i in range(n):
        result += i ** 2
    return result


def benchmark_cpu_bound():
    """Benchmark CPU-bound tasks to show GIL impact"""
    print("\n" + "="*70)
    print("BENCHMARK: CPU-Bound Task")
    print("="*70)
    
    iterations = 10_000_000
    num_workers = 4
    
    # Sequential execution
    print(f"\n1️⃣  Sequential execution ({num_workers} tasks):")
    start = time.perf_counter()
    for _ in range(num_workers):
        cpu_intensive(iterations)
    seq_time = time.perf_counter() - start
    print(f"   Time: {seq_time:.3f}s")
    
    # Multi-threaded execution
    print(f"\n2️⃣  Multi-threaded execution ({num_workers} threads):")
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(cpu_intensive, iterations) for _ in range(num_workers)]
        for f in futures:
            f.result()
    mt_time = time.perf_counter() - start
    print(f"   Time: {mt_time:.3f}s")
    
    # Analysis
    speedup = seq_time / mt_time
    print(f"\n📊 Results:")
    print(f"   Speedup: {speedup:.2f}x")
    
    if FREE_THREADING:
        if speedup > 2.5:
            print(f"   ✓ TRUE PARALLELISM! Free-threading working!")
            print(f"   ✓ Multiple threads execute simultaneously")
        else:
            print(f"   ⚠️  Expected better speedup with free-threading")
    else:
        if speedup < 1.2:
            print(f"   ✓ GIL CONFIRMED: No parallel execution")
            print(f"   → Multiple threads take same time as sequential")
        else:
            print(f"   → Some speedup (context switching overhead varies)")


# ============================================================================
# Python 3.12+: Subinterpreters (PEP 684)
# ============================================================================

def demo_subinterpreters():
    """Demonstrate subinterpreters with per-interpreter GIL"""
    print("\n" + "="*70)
    print("DEMO: Subinterpreters (Python 3.12+, PEP 684)")
    print("="*70)
    
    if not PY_312_PLUS:
        print(f"\n⚠️  Requires Python 3.12+ (you have {PY_VERSION.major}.{PY_VERSION.minor})")
        return
    
    try:
        import _xxsubinterpreters as interpreters
        
        print("\n✓ Subinterpreters available!")
        print("\n📝 Key concepts:")
        print("   • Each subinterpreter = separate Python environment")
        print("   • Each has its OWN GIL (independent locking)")
        print("   • True parallel CPU execution across interpreters")
        print("   • Isolated namespaces (no shared state)")
        
        # Create and use subinterpreter
        print(f"\n🔧 Creating subinterpreter...")
        interp_id = interpreters.create()
        print(f"   Created with ID: {interp_id}")
        
        # Execute code in subinterpreter
        print(f"\n▶️  Executing code in subinterpreter:")
        code = """
import threading
print(f"   Thread ID: {threading.get_ident()}")
print(f"   I'm running in a separate interpreter!")
result = sum(i**2 for i in range(1000))
print(f"   Calculation result: {result}")
"""
        interpreters.run_string(interp_id, code)
        
        # Cleanup
        interpreters.destroy(interp_id)
        print(f"   ✓ Subinterpreter destroyed")
        
        print(f"\n💡 Use case:")
        print(f"   When you need true parallelism without multiprocessing overhead")
        
    except ImportError:
        print(f"\n⚠️  _xxsubinterpreters not available")
        print(f"   (Still experimental - use with caution)")


# ============================================================================
# Python 3.13+: Free-Threading Info
# ============================================================================

def demo_free_threading_info():
    """Show free-threading information and detection"""
    print("\n" + "="*70)
    print("DEMO: Free-Threading Mode (Python 3.13+, PEP 703)")
    print("="*70)
    
    if not PY_313_PLUS:
        print(f"\n⚠️  Requires Python 3.13+ (you have {PY_VERSION.major}.{PY_VERSION.minor})")
        print(f"\n📖 What is free-threading?")
        print(f"   • Python without the GIL")
        print(f"   • Multiple threads execute Python code simultaneously")
        print(f"   • CPU-bound tasks scale with number of cores")
        return
    
    print(f"\n✓ Python 3.13+ detected!")
    
    # Check GIL status
    print(f"\n🔍 GIL Status:")
    if hasattr(sys, '_is_gil_enabled'):
        gil_enabled = sys._is_gil_enabled()
        print(f"   sys._is_gil_enabled() = {gil_enabled}")
        
        if not gil_enabled:
            print(f"   ✓ FREE-THREADING ACTIVE!")
            print(f"\n✨ Benefits:")
            print(f"   • No GIL bottleneck")
            print(f"   • True parallel multi-threading")
            print(f"   • CPU-bound tasks scale linearly with cores")
            print(f"\n⚠️  Considerations:")
            print(f"   • Some C extensions may not work")
            print(f"   • Slightly higher memory usage")
            print(f"   • Thread safety becomes your responsibility")
        else:
            print(f"   ✗ GIL is ENABLED (traditional mode)")
            print(f"\n📦 To enable free-threading:")
            print(f"   1. Install free-threading build:")
            print(f"      apt install python3.13t  # Debian/Ubuntu")
            print(f"   2. Or build from source:")
            print(f"      ./configure --disable-gil")
            print(f"   3. Or use environment variable:")
            print(f"      PYTHON_GIL=0 python3.13 script.py")
    else:
        print(f"   sys._is_gil_enabled() not available")


# ============================================================================
# Comparison Guide
# ============================================================================

def show_comparison_guide():
    """Show when to use which approach"""
    print("\n" + "="*70)
    print("GUIDE: When to Use What?")
    print("="*70)
    
    current_setup = "Unknown"
    if FREE_THREADING:
        current_setup = "Free-Threading (No GIL)"
    elif PY_313_PLUS:
        current_setup = "Python 3.13 (GIL Active)"
    elif PY_312_PLUS:
        current_setup = "Python 3.12"
    else:
        current_setup = f"Python {PY_VERSION.major}.{PY_VERSION.minor}"
    
    print(f"\n📍 Your Setup: {current_setup}")
    print(f"\n📋 Recommendations:")
    
    if FREE_THREADING:
        print(f"""
✓ With free-threading enabled:
  ├─ CPU-bound tasks     → Use threading.Thread or ThreadPoolExecutor
  ├─ I/O-bound tasks     → Use async/await (still most efficient)
  ├─ Mixed workloads     → Use threading
  └─ Isolated execution  → Use subinterpreters (if available)
""")
    elif PY_313_PLUS:
        print(f"""
✓ With Python 3.13 (GIL active):
  ├─ CPU-bound tasks     → Use multiprocessing.Pool
  ├─ I/O-bound tasks     → Use async/await or threading
  ├─ Many concurrent I/O → Use async/await
  └─ Consider            → Enable free-threading for CPU-heavy apps
""")
    elif PY_312_PLUS:
        print(f"""
✓ With Python 3.12:
  ├─ CPU-bound tasks     → Use multiprocessing.Pool or subinterpreters
  ├─ I/O-bound tasks     → Use async/await or threading
  ├─ Many concurrent I/O → Use async/await
  └─ Isolated parallel   → Use subinterpreters (experimental)
""")
    else:
        print(f"""
With Python {PY_VERSION.major}.{PY_VERSION.minor}:
  ├─ CPU-bound tasks     → Use multiprocessing.Pool
  ├─ I/O-bound tasks     → Use async/await or threading
  ├─ Many concurrent I/O → Use async/await
  └─ Consider upgrading  → Python 3.13+ for free-threading
""")
    
    print(f"\n📊 Quick Reference:")
    print(f"""
Traditional GIL (Python < 3.13 or GIL enabled):
  • Threading: Good for I/O, bad for CPU
  • Async: Best for I/O with many concurrent tasks
  • Multiprocessing: Best for CPU-bound tasks

Free-Threading (Python 3.13+ with --disable-gil):
  • Threading: Good for CPU AND I/O
  • Async: Still best for I/O (lower overhead)
  • Multiprocessing: Less necessary, but still useful
""")


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n🚀 Modern Python Concurrency: 3.12 & 3.13 🚀")
    
    print_version_info()
    benchmark_cpu_bound()
    demo_subinterpreters()
    demo_free_threading_info()
    show_comparison_guide()
    
    print("\n" + "="*70)
    print("✨ The Future of Python Concurrency")
    print("="*70)
    print("""
Python's concurrency model is evolving rapidly:

2023: Python 3.12 → Per-interpreter GIL (subinterpreters)
2024: Python 3.13 → Experimental no-GIL mode (free-threading)
2025: Python 3.14 → Stdlib interpreters, free-threading Phase II

The GIL is no longer a limitation! 🎉
""")


if __name__ == "__main__":
    main()
