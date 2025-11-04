#!/usr/bin/env python3
"""
setup_check.py
Verifies SafeLab environment setup and dependencies.

Usage:
    python setup_check.py
"""

import os
import sys
import importlib.util

REQUIRED_DIRS = [
    "analysis",
    "collector",
    "demo",
    "docs",
    "emulation",
    "lab-setup",
    "reporting"
]

REQUIRED_FILES = [
    "README.md",
    "requirements.txt",
    "emulation/run_emulation.py",
    "collector/collect.py",
    "reporting/generate_report.py",
    "docs/ETHICS.md"
]

REQUIRED_LIBS = [
    "requests",
    "jinja2",
    "flask",
    "python_dateutil"
]

def check_dirs():
    print("📂 Checking directory structure...")
    all_ok = True
    for d in REQUIRED_DIRS:
        if not os.path.isdir(d):
            print(f"❌ Missing directory: {d}")
            all_ok = False
        else:
            print(f"✅ {d}/ found")
    return all_ok

def check_files():
    print("\n📄 Checking required files...")
    all_ok = True
    for f in REQUIRED_FILES:
        if not os.path.exists(f):
            print(f"❌ Missing file: {f}")
            all_ok = False
        else:
            print(f"✅ {f} found")
    return all_ok

def check_libs():
    print("\n🧩 Checking Python libraries...")
    all_ok = True
    for lib in REQUIRED_LIBS:
        if importlib.util.find_spec(lib) is None:
            print(f"❌ Missing library: {lib}")
            all_ok = False
        else:
            print(f"✅ {lib} installed")
    return all_ok

def summary(results):
    print("\n===============================")
    if all(results):
        print("🎉 SafeLab environment setup looks GOOD!")
    else:
        print("⚠️  Some checks failed — please fix the issues above before running SafeLab.")
    print("===============================")

if __name__ == "__main__":
    print("🔍 Running SafeLab setup verification...\n")
    ok_dirs = check_dirs()
    ok_files = check_files()
    ok_libs = check_libs()
    summary([ok_dirs, ok_files, ok_libs])
