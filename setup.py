#!/usr/bin/env python3
"""
Setup Script for AI-Powered DevOps Incident Response System
Automates initial project setup and configuration
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header"""
    print("AI-Powered DevOps Incident Response System Setup")
    print("=" * 55)

def check_python_version():
    """Check Python version compatibility"""
    print("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"SUCCESS: Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("SUCCESS: Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install dependencies: {e}")
        return False

def setup_env_file():
    """Setup .env file from example"""
    print("\nSetting up environment configuration...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("WARNING: .env file already exists")
        response = input("   Overwrite existing .env file? (y/N): ").strip().lower()
        if response != 'y':
            print("   Keeping existing .env file")
            return True
    
    if not env_example.exists():
        print("ERROR: .env.example file not found")
        return False
    
    try:
        # Copy example to .env
        with open(env_example, 'r') as src, open(env_file, 'w') as dst:
            dst.write(src.read())
        
        print("SUCCESS: .env file created from .env.example")
        print("HINT: Please edit .env and update GEMINI_API_KEY with your actual key")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to create .env file: {e}")
        return False

def create_logs_directory():
    """Create logs directory"""
    print("\nCreating logs directory...")
    
    logs_dir = Path("logs")
    
    if logs_dir.exists():
        print("SUCCESS: Logs directory already exists")
        return True
    
    try:
        logs_dir.mkdir(exist_ok=True)
        print("SUCCESS: Logs directory created")
        return True
    except Exception as e:
        print(f"ERROR: Failed to create logs directory: {e}")
        return False

def validate_setup():
    """Validate the setup"""
    print("\nValidating setup...")
    
    try:
        # Try to import core modules
        from core.config import validate_config, print_config_status
        
        print("SUCCESS: Core modules imported successfully")
        
        # Check configuration
        print("\nConfiguration Status:")
        print_config_status()
        
        return True
        
    except ImportError as e:
        print(f"ERROR: Failed to import modules: {e}")
        return False
    except Exception as e:
        print(f"WARNING: Configuration validation: {e}")
        print("HINT: This is expected if you haven't set GEMINI_API_KEY yet")
        return True

def print_next_steps():
    """Print next steps for the user"""
    print("\nNext Steps:")
    print("1. Edit .env file and add your GEMINI_API_KEY:")
    print("   nano .env")
    print("   # Get your key from: https://makersuite.google.com/app/apikey")
    print()
    print("2. Check configuration:")
    print("   python main.py --config")
    print()
    print("3. Run system test:")
    print("   python main.py --test")
    print()
    print("4. Try the interactive demo:")
    print("   python main.py --demo")
    print()
    print("5. Process an incident:")
    print('   python main.py "Payment API database timeout"')

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nERROR: Setup failed during dependency installation")
        sys.exit(1)
    
    # Setup .env file
    if not setup_env_file():
        print("\nERROR: Setup failed during .env file creation")
        sys.exit(1)
    
    # Create logs directory
    if not create_logs_directory():
        print("\nERROR: Setup failed during logs directory creation")
        sys.exit(1)
    
    # Validate setup
    if not validate_setup():
        print("\nERROR: Setup validation failed")
        sys.exit(1)
    
    print("\nSUCCESS: Setup completed successfully!")
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup interrupted!")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Setup error: {e}")
        sys.exit(1)