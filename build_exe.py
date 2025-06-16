"""
Build script for creating a Glitch Runner executable
"""
import os
import sys
import shutil
import subprocess

def clean_project():
    """Clean up cached Python files and previous builds"""
    print("Cleaning project directory...")
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                path = os.path.join(root, dir_name)
                print(f"Removing {path}")
                shutil.rmtree(path, ignore_errors=True)
    
    # Remove .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                path = os.path.join(root, file)
                print(f"Removing {path}")
                os.remove(path)
    
    # Remove build directories
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name} directory")
            shutil.rmtree(dir_name, ignore_errors=True)
    
    # Remove spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            print(f"Removing {file}")
            os.remove(file)

def build_executable():
    """Build the executable using PyInstaller"""
    print("Building executable...")
    
    # Determine the correct command to run PyInstaller
    pyinstaller_cmd = None
    commands_to_try = [
        'pyinstaller',
        'python -m PyInstaller',
        'python3 -m PyInstaller',
        'py -m PyInstaller'
    ]
    
    for cmd in commands_to_try:
        try:
            subprocess.run(f"{cmd} --version", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            pyinstaller_cmd = cmd
            print(f"Using PyInstaller command: {cmd}")
            break
        except subprocess.CalledProcessError:
            continue
    
    if not pyinstaller_cmd:
        print("ERROR: PyInstaller not found. Please install it with 'pip install pyinstaller'")
        return False
    
    # Build the executable
    build_cmd = f"{pyinstaller_cmd} --name GlitchRunner --onefile --windowed --add-data assets:assets --add-data resource_path.py:. --clean main.py"
    print(f"Running: {build_cmd}")
    
    try:
        subprocess.run(build_cmd, shell=True, check=True)
        print("\nBuild successful! Executable created in the 'dist' folder.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Build failed with error code {e.returncode}")
        return False

def main():
    """Main function"""
    print("=== Glitch Runner Executable Builder ===")
    
    # Clean the project
    clean_project()
    
    # Build the executable
    success = build_executable()
    
    if success:
        print("\nExecutable build complete!")
        print("You can find your executable in the 'dist' folder.")
    else:
        print("\nExecutable build failed. Please check the errors above.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
