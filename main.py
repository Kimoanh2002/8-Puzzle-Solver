import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from window.main_window import MainWindow

def main():
    window = MainWindow()
    window.run()

if __name__ == "__main__":
    main()
