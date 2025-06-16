"""
Build script for creating a Windows Glitch Runner executable using Wine and PyInstaller
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

def build_windows_executable():
    """Build the Windows executable using Wine and PyInstaller"""
    print("Building Windows executable...")
    
    # Create a spec file for PyInstaller
    spec_content = """# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[('assets', 'assets'), ('resource_path.py', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='GlitchRunner',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='assets/images/icon.ico' if os.path.exists('assets/images/icon.ico') else None)
"""
    
    # Write the spec file
    with open('GlitchRunner.spec', 'w') as f:
        f.write(spec_content)
    
    # Run PyInstaller with Wine
    build_cmd = "wine pyinstaller GlitchRunner.spec"
    print(f"Running: {build_cmd}")
    
    try:
        subprocess.run(build_cmd, shell=True, check=True)
        print("\nBuild successful! Windows executable created in the 'dist' folder.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Build failed with error code {e.returncode}")
        return False

def main():
    """Main function"""
    print("=== Glitch Runner Windows Executable Builder ===")
    
    # Clean the project
    clean_project()
    
    # Build the executable
    success = build_windows_executable()
    
    if success:
        print("\nWindows executable build complete!")
        print("You can find your executable in the 'dist' folder.")
    else:
        print("\nWindows executable build failed. Please check the errors above.")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
