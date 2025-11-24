#!/usr/bin/env python3
"""
Setup verification script for Shazam Prototype
Checks if all dependencies are installed and configured correctly.
"""

import sys

def check_import(module_name, package_name=None):
    """Check if a module can be imported."""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        print(f"✅ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False

def check_ffmpeg():
    """Check if FFmpeg is available."""
    import subprocess
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.DEVNULL, 
                      stderr=subprocess.DEVNULL,
                      check=True)
        print("✅ FFmpeg is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg is NOT installed")
        return False

def main():
    print("=" * 50)
    print("Shazam Prototype - Setup Verification")
    print("=" * 50)
    print()
    
    all_ok = True
    
    # Check Python version
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 7):
        print("⚠️  Python 3.7+ is recommended")
        all_ok = False
    print()
    
    # Check required packages
    print("Checking Python packages...")
    packages = [
        ('numpy', 'numpy'),
        ('scipy', 'scipy'),
        ('librosa', 'librosa'),
        ('flask', 'Flask'),
        ('sounddevice', 'sounddevice'),
        ('soundfile', 'soundfile'),
        ('requests', 'requests'),
        ('yt_dlp', 'yt-dlp'),
    ]
    
    for module, package in packages:
        if not check_import(module, package):
            all_ok = False
    
    print()
    
    # Check FFmpeg
    print("Checking external dependencies...")
    if not check_ffmpeg():
        all_ok = False
    
    print()
    print("=" * 50)
    
    if all_ok:
        print("✅ All dependencies are installed!")
        print("You can now run: python app.py")
    else:
        print("❌ Some dependencies are missing.")
        print("Please run: pip install -r requirements.txt")
        print("And install FFmpeg from: https://ffmpeg.org/download.html")
    
    print("=" * 50)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
