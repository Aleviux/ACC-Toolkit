# Checker Tool
__author__ = 'Alejandro Camunas Casas'
__copyright__ = 'Copyright (C) 2021 Alejandro Camunas Casas'
__license__ = 'Public Domain'
__version__ = '0.1'

# Custom modules import path
import sys, os
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PACKAGE_DIR)

# Reload custom modules (Debug)
#from debug.ReloadCustomModules_Debug import *
#reloadCustomModules()

from classes.MainWindowManager_Class import MainWindowManager

#######################################
# RUN FUNCTION
#######################################

def run_global():

	# Global Manager Single Instance
	global mainWindowManager
	mainWindowManager = None

	if not mainWindowManager or not mainWindowManager in globals():
		mainWindowManager = MainWindowManager(PACKAGE_DIR)
		mainWindowManager.createWindow()
	
	mainWindowManager.showWindow()

def run_local():

	# Local Manager Instance (Debug)
	mainWindowManager = None
	
	if mainWindowManager is None:
		mainWindowManager = MainWindowManager(PACKAGE_DIR)
		mainWindowManager.createWindow()
	
	mainWindowManager.showWindow()

if __name__ == '__main__': run_global()
