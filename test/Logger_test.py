import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


from src import Logger
Logger.Logging('test')
