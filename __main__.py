"""python -m fortune 入口。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fortune import main

if __name__ == "__main__":
    sys.exit(main())
