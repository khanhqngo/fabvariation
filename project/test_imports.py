"""
Quick test script to verify all dependencies are installed correctly.
Run this before running the main app to check your environment.

Usage: python test_imports.py
"""

import sys

def test_imports():
    """Test all required imports."""
    print("Testing FabVariation dependencies...\n")

    required_packages = [
        ('streamlit', 'Streamlit'),
        ('pandas', 'Pandas'),
        ('numpy', 'NumPy'),
        ('plotly', 'Plotly'),
        ('scipy', 'SciPy'),
        ('reportlab', 'ReportLab'),
        ('PIL', 'Pillow'),
    ]

    all_passed = True

    for package_name, display_name in required_packages:
        try:
            __import__(package_name)
            print(f"✓ {display_name:20s} - OK")
        except ImportError as e:
            print(f"✗ {display_name:20s} - MISSING")
            all_passed = False

    print("\n" + "="*50)

    if all_passed:
        print("✓ All dependencies installed successfully!")
        print("\nYou can now run: streamlit run app.py")
        return 0
    else:
        print("✗ Some dependencies are missing.")
        print("\nPlease run: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(test_imports())
