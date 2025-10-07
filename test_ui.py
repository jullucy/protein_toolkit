#!/usr/bin/env python3
"""Quick test to verify Beer-Lambert UI styling is working correctly"""

import sys
from PySide6.QtWidgets import QApplication
from protein_tool.viewmodels.beer_lambert_vm import BeerLambertViewModel
from protein_tool.ui.modules.beer_lambert_view import BeerLambertView

def test_ui():
    app = QApplication(sys.argv)
    
    # Create viewmodel and view
    vm = BeerLambertViewModel()
    view = BeerLambertView(vm)
    
    # Show the window
    view.show()
    view.resize(1200, 800)
    
    print("Beer-Lambert UI Test Window opened.")
    print("Check that:")
    print("1. All text is readable (no white text on white background)")
    print("2. Blue color scheme is consistently applied")
    print("3. Calculator tab input fields work properly")
    print("4. Standard Curve tab data entry works")
    print("5. Theory tab displays educational content correctly")
    print("Press Ctrl+C to close when testing is complete.")
    
    try:
        app.exec()
    except KeyboardInterrupt:
        print("\nTest completed.")

if __name__ == "__main__":
    test_ui()
