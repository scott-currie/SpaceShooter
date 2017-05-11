import os, sys

'''Dirty little module for holding globals'''
resource_path = os.path.join(os.path.dirname(sys.argv[0]), 'resources')
playerScore = 0
FPS = 30