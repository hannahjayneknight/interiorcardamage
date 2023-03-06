import os
from pathlib import Path
print(__file__)
print(os.path.join(os.path.dirname(__file__), '..'))
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.abspath(os.path.dirname(__file__)))
print(os.path.dirname(__file__))
print(Path(__file__).parent)