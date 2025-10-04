#!/usr/bin/env python3
"""
Skyluxe Application Runner
Simple script to run the application with proper setup
"""
import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)

def run_application():
    """Run the Skyluxe application"""
    print("🚀 Starting Skyluxe Climate Analysis Platform...")
    print("📍 Backend API will be available at: http://localhost:8000")
    print("📊 API Documentation: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run the application
        subprocess.run([sys.executable, "-m", "skyluxe.main"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed to start: {e}")
        sys.exit(1)

def main():
    """Main application runner"""
    print("🌍 Skyluxe Climate Analysis Platform")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("skyluxe").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    install_dependencies()
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main()
