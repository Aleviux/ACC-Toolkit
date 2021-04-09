import json, os

from Log_Class import Log
from Singleton_Metaclass import SingletonMetaclass

from MainWindow_Class import MainWindow
from Rule_Class import Rule
from Script_Class import Script

from MaxAPICommunicator_Class import MaxAPICommunicator
from MayaAPICommunicator_Class import MayaAPICommunicator

########################################
# MAIN WINDOW MANAGER CONTROLLER
########################################

class MainWindowManager ():
	
	__metaclass__ = SingletonMetaclass

	__mainWindow = None
	__API = None

	__fileDir = ""

	__rulePath = ""
	__ruleSet = None

	__preScriptsPath = ""
	__postScriptsPath = ""
	__preScriptList = []
	__postScriptList = []

	##### Object Functions #####

	# Class constructor
	def __init__ (self, fileDir):
		self.fileDir = fileDir

		Log.setLogPath(self.fileDir)
		Log.createLog()
		Log.printToLog("Initializing Main Window Manager")

		self.getAPI()

		self.readRulePath()
		self.__ruleSet = dict()
		self.loadRules()

		self.readScriptsPath()
		self.loadScripts("pre")
		self.loadScripts("post")

	# Class destructor
	def __del__ (self):
		Log.printToLog ("Deleting Main Window Manager")

		for rule in self.__ruleSet.keys():
			del self.__ruleSet[rule]

	##### Tool Configuration #####

	# Reads the configuration file data
	def readConfig (self):
		jdata = {}
		text = ""

		try: 
			file = open(self.fileDir + "\\Config.ini", "r")
			text = file.read()
			file.close()
		except: 
			text = ""

		try:
			jdata = json.loads(text)

			if not ("Rules" in jdata and "PreScripts" in jdata and "PostScripts" in jdata):
				raise Exception("")
		except:
			jdata = self.resetConfig()

		return jdata

	# Writes data to the configuration file
	def writeConfig (self, jdata):
		with open(self.fileDir + "\\Config.ini", "w") as file:
			json.dump(jdata, file, indent = 1)

	# Resets the configuration file to default data
	def resetConfig (self, rules = "", preScripts = "", postScripts = ""):
		if rules == "":
			if isinstance(self.__API, MaxAPICommunicator): rules = self.fileDir + "\\rules\\max\\"
			elif isinstance(self.__API, MayaAPICommunicator): rules = self.fileDir + "\\rules\\maya\\"

		if preScripts == "": preScripts = self.fileDir + "\\scripts\\pre\\"
		if postScripts == "": postScripts = self.fileDir + "\\scripts\\post\\"

		jsonData = {"Rules":rules, "PreScripts":preScripts, "PostScripts":postScripts}

		with open(self.fileDir + "\\Config.ini", "w") as file:
			json.dump(jsonData, file, indent = 1)

		return jsonData

	##### UI Window Management #####

	# Creates the Qt Window
	def createWindow (self):
		if self.__mainWindow is None: 
			self.__mainWindow = MainWindow()
			Log.printToLog("Main Window Created")

		self.refreshRuleUI()
		self.refreshScriptsUI("pre")
		self.refreshScriptsUI("post")

	# Shows the Qt Window
	def showWindow (self):
		Log.printToLog("Showing Main Window")
		self.__mainWindow.showWindow()

	# Returns the valid API for the application
	def getAPI(self):

		try:
			import maya.cmds as cmds
			del cmds

			self.__API = MayaAPICommunicator()
			Log.printToLog ("Maya API found")
		except: pass

		try:
			import pymxs
			del pymxs

			self.__API = MaxAPICommunicator()
			Log.printToLog ("Max API Found")
		except: pass

		if self.__API == None:
			Log.printToLog("No valid 3D software API found!")
			raise Exception("No valid 3D software API found!")

	##### Rule Management #####

	# Reads the Rules path from the config file
	def readRulePath (self):
		jdata = self.readConfig()
	
		if os.path.isdir(jdata["Rules"]):
			self.__rulePath = jdata["Rules"]
		else:
			jdata = self.resetConfig(preScripts = self.__preScriptsPath, postScripts = self.__postScriptsPath)
			self.__rulePath = jdata["Rules"]

		Log.printToLog("Rule path loaded: " + self.__rulePath)

	# Changes the Rules path to the chosen dir
	def changeRulePath (self):
		path = self.__API.browseFileDir("Rules Path", startDir = self.__rulePath)

		if path != None:
			self.__rulePath = path + "\\"
			Log.printToLog("Rule path changed: " + path)

			jdata = self.readConfig()
			jdata["Rules"] = self.__rulePath
			self.writeConfig(jdata)

			self.__ruleSet = dict()
			self.loadRules()
			self.refreshRuleUI()

	# Loads the Rules for the current path
	def loadRules (self):
		rulefiles = os.listdir(self.__rulePath)
		Log.printToLog("Loading rules: " + self.__rulePath)

		for rulefile in rulefiles:
			if "rule_" in rulefile and ".json" in rulefile:
				file = open ((self.__rulePath + rulefile), "r")
				jdata = json.load(file)
				file.close()

				jname = jdata["Name"]

				if not (jname in self.__ruleSet):
					self.__ruleSet[jname] = Rule()
					(self.__ruleSet[jname]).setProperties(jdata)

					Log.printToLog ("Rule Loaded: " + self.__ruleSet[jname].getProperty("Name"))
					Log.printToLog (self.__ruleSet[jname].debug_printRule())

		Log.printToLog ("Rule Dictionary Status: " + str(self.__ruleSet.keys()))

	# Returns the Rule Object Data
	def getRuleData (self, ruleName):
		rData = {
			"Name" : "",
			"Desc" : "",
			"CheckCode" : "",
			"CheckSyntax" : "",
			"FixCode" : "",
			"FixSyntax" : ""
		}

		for prop in rData.keys():
			rData[prop] = (self.__ruleSet[ruleName].getProperty(prop))

		return rData

	# Loads check script data from chosen file
	def browseCheckCode (self):
		path = self.__API.browseFileLoad("Check Script File", "script")

		if path != None:
			file = open (path, "r")
			data = file.read()
			file.close()

			rData = {}

			sp = path.split(".")
			ext = sp[len(sp) - 1]

			if ext == "py": rData["CheckSyntax"] = "Python"
			elif ext == "ms": rData["CheckSyntax"] = "MaxScript"
			elif ext == "mel": rData["CheckSyntax"] = "MEL"

			sp = path.split("\\")
			name = (sp[len(sp) - 1]).split(".")[0]

			rData["Name"] = name
			rData["CheckCode"] = data

			self.__mainWindow.setRuleWindowData(rData)

	# Loads fix script data from chosen file
	def browseFixCode (self):
		path = self.__API.browseFileLoad("Fix Script File", "script")
		
		if path != None:
			file = open (path, "r")
			data = file.read()
			file.close()

			rData = {}

			sp = path.split(".")
			ext = sp[len(sp) - 1]

			if ext == "py": rData["FixSyntax"] = "Python"
			elif ext == "ms": rData["FixSyntax"] = "MaxScript"
			elif ext == "mel": rData["FixSyntax"] = "MEL"

			rData["FixCode"] = data

			self.__mainWindow.setRuleWindowData(rData)

	# Creates the Rule Object
	def createRule (self, jsonData):
		r = Rule()
		r.setProperties(jsonData)
		self.__ruleSet[jsonData["Name"]] = r
		
		fileName = self.__rulePath + "rule_" + jsonData["Name"] + ".json"
		with open(fileName, "w") as file:
			json.dump(jsonData, file, indent = 1)

		self.refreshRuleUI()

		Log.printToLog ("Rule Created: " + r.getProperty("Name"))
		Log.printToLog (r.debug_printRule())
		Log.printToLog ("Rule Dictionary Status: " + str(self.__ruleSet.keys()))

	# Edits the Rule Object data
	def editRule (self, oldName, newName, jsonData):
		if oldName in self.__ruleSet:
			rule = self.__ruleSet[oldName]
			del self.__ruleSet[oldName]
			self.__ruleSet[newName] = rule
			self.__ruleSet[newName].setProperties(jsonData)

			Log.printToLog ("Rule Edited: " + oldName)
			Log.printToLog (self.__ruleSet[newName].debug_printRule())

			fileName = self.__rulePath + "rule_" + oldName + ".json"
			if os.path.exists(fileName):
				os.remove(fileName)

			fileName = self.__rulePath + "rule_" + newName + ".json"
			with open(fileName, "w") as file:
				json.dump(jsonData, file, indent=1)

		self.refreshRuleUI()

	# Deletes the Rule Object
	def deleteRule (self, ruleName):
		fileName = self.__rulePath + "rule_" + ruleName + ".json"
		if os.path.exists(fileName): os.remove(fileName)

		if ruleName in self.__ruleSet:
			del self.__ruleSet[ruleName]

			Log.printToLog ("Rule Deleted: " + ruleName)
			Log.printToLog ("Rule Dictionary Status: " + str(self.__ruleSet.keys()))

			self.__mainWindow.deleteRuleRow(ruleName)
			self.refreshRuleUI()

	# Deletes all Rule Objects
	def deleteAllRules (self):
		for rule in self.__ruleSet.keys():
			self.deleteRule(rule)

	# Runs the Rule Object's Check Code
	def checkRule (self, ruleName):
		if ruleName in self.__ruleSet:
			synt = self.__ruleSet[ruleName].getProperty("CheckSyntax")
			code = self.__ruleSet[ruleName].getProperty("CheckCode")

			res = self.__API.evaluateCode(synt, code)

			if res == False:
				self.__ruleSet[ruleName].setFixable(True)
				self.__mainWindow.setRuleRowStatus(ruleName, 1, self.__ruleSet[ruleName].isFixable())
			elif res == True:
				self.__ruleSet[ruleName].setFixable(False)
				self.__mainWindow.setRuleRowStatus(ruleName, 2)
			elif res == (-1):
				self.__ruleSet[ruleName].setFixable(False)
				self.__mainWindow.setRuleRowStatus(ruleName, -1)

			Log.printToLog("Rule {0} checked result: {1}".format(ruleName, res))

	# Checks all Rule Objects
	def checkAllRules (self):
		for rule in self.__ruleSet.keys():
			self.checkRule(rule)

	# Runs the Rule Object's Fix Code
	def fixRule (self, ruleName):
		if ruleName in self.__ruleSet:
			synt = self.__ruleSet[ruleName].getProperty("FixSyntax")
			code = self.__ruleSet[ruleName].getProperty("FixCode")

			self.__API.evaluateCode(synt, code)
			self.__ruleSet[ruleName].setFixable(False)
			self.__mainWindow.setRuleRowStatus(ruleName, 2)

			Log.printToLog("Rule {0} fixed".format(ruleName))

	# Fixes all Rule Objects
	def fixAllRules (self):
		for rule in self.__ruleSet.keys():
			if self.__ruleSet[rule].isFixable(): 
				self.fixRule(rule)

	# Shows the Rule Object Description Dialog
	def showRuleInfo (self, ruleName):
		self.__mainWindow.ruleInfoDialog(self.__ruleSet[ruleName].getProperty("Name"), self.__ruleSet[ruleName].getProperty("Desc"))

	# Reloads the Rules UI Qt Elements
	def refreshRuleUI (self):
		self.__mainWindow.clearRuleRows()
		self.__mainWindow.setRulePathText(self.__rulePath)

		for rName in sorted(self.__ruleSet.keys(), key = unicode.lower):
			self.__mainWindow.addRuleRow(rName)

	##### Export Scripts #####

	# Reads the Scripts path from the config file
	def readScriptsPath (self):
		jdata = self.readConfig()
	
		import os
		if os.path.isdir(jdata["PreScripts"]):
			self.__preScriptsPath = jdata["PreScripts"]
		else:
			jdata = self.resetConfig(rules = self.__rulePath, postScripts = self.__postScriptsPath)
			self.__preScriptsPath = jdata["PreScripts"]

		if os.path.isdir(jdata["PostScripts"]):
			self.__postScriptsPath = jdata["PostScripts"]
		else:
			jdata = self.resetConfig(rules = self.__rulePath, preScripts = self.__preScriptsPath)
			self.__postScriptsPath = jdata["PostScripts"]

		Log.printToLog("Pre-Scripts path loaded: " + self.__preScriptsPath)
		Log.printToLog("Post-Scripts path loaded: " + self.__postScriptsPath)

	# Changes the Pre-Scripts path to the chosen dir
	def changePreScriptsPath (self):
		path = self.__API.browseFileDir("Pre Scripts Path", startDir = self.__preScriptsPath)
		
		if path != None:
			self.__preScriptsPath = path + "\\"
			Log.printToLog("Pre-Scripts path changed: " + path)

			jdata = self.readConfig()
			jdata["PreScripts"] = self.__preScriptsPath
			self.writeConfig(jdata)

			self.__preScriptList = []
			self.loadScripts("pre")
			self.refreshScriptsUI("pre")

	# Changes the Post-Scripts path to the chosen dir
	def changePostScriptsPath (self):
		path = self.__API.browseFileDir("Post Scripts Path", startDir = self.__postScriptsPath)
		
		if path != None:
			self.__postScriptsPath = path + "\\"
			Log.printToLog("Post-Scripts path changed: " + path)

			jdata = self.readConfig()
			jdata["PostScripts"] = self.__postScriptsPath
			self.writeConfig(jdata)

			self.__postScriptList = []
			self.loadScripts("post")
			self.refreshScriptsUI("post")

	# Loads the Scripts for the current path
	def loadScripts (self, mode):
		path = ""
		if mode == "pre": path = self.__preScriptsPath
		elif mode == "post": path = self.__postScriptsPath

		Log.printToLog("Loading {0}-export scripts: {1}".format(mode, path))

		files = os.listdir(path)
		scriptFiles = []
		for file in files:
			sp = file.split(".")
			ext = sp[len(sp) - 1]

			if (isinstance (self.__API, MaxAPICommunicator) and (ext == "py" or ext == "ms")) or \
			(isinstance (self.__API, MayaAPICommunicator) and (ext == "py" or ext == "mel")):
				scriptFiles.append(file)

		scriptList = []
		for scriptFile in scriptFiles:
			file = open ((path + scriptFile), "r")
			code = file.read()
			file.close()

			sp = scriptFile.split(".")
			name = sp[0]
			ext = sp[len(sp) - 1]

			syntax = ""
			if ext == "py": syntax = "Python"
			elif ext == "ms": syntax = "MaxScript"
			elif ext == "mel": syntax = "MEL"

			script = Script(name, code, syntax)
			scriptList.append(script)

		if mode == "pre": self.__preScriptList = scriptList
		elif mode == "post": self.__postScriptList = scriptList

	# Raises the Script in the export list order
	def raiseScript(self, sName):
		mode = ""
		index = 0

		for preScript in self.__preScriptList:
			if sName == preScript.getName():
				mode = "pre"
				index = self.__preScriptList.index(preScript)

		for postScript in self.__postScriptList:
			if sName == postScript.getName():
				mode = "post"
				index = self.__postScriptList.index(postScript)

		if mode == "pre" and index > 0:
			self.__preScriptList[index - 1], self.__preScriptList[index] = self.__preScriptList[index], self.__preScriptList[index - 1]
		elif mode == "post" and index > 0:
			self.__postScriptList[index - 1], self.__postScriptList[index] = self.__postScriptList[index], self.__postScriptList[index - 1]

		self.refreshScriptsUI(mode)

	# Lowers the Script in the export list order
	def lowerScript(self, sName):
		mode = ""
		index = 0

		for preScript in self.__preScriptList:
			if sName == preScript.getName():
				mode = "pre"
				index = self.__preScriptList.index(preScript)

		for postScript in self.__postScriptList:
			if sName == postScript.getName():
				mode = "post"
				index = self.__postScriptList.index(postScript)

		if mode == "pre" and index < len(self.__preScriptList):
			self.__preScriptList[index - 1], self.__preScriptList[index] = self.__preScriptList[index], self.__preScriptList[index - 1]
		elif mode == "post" and index < len(self.__postScriptList):
			self.__postScriptList[index + 1], self.__postScriptList[index] = self.__postScriptList[index], self.__postScriptList[index + 1]

		self.refreshScriptsUI(mode)

	# Evaluates the Scripts
	def evaluateScripts (self, mode):
		scriptList = []

		if mode == "pre": scriptList = self.__preScriptList
		elif mode == "post": scriptList = self.__postScriptList

		Log.printToLog("Evaluating " + mode + " scripts")

		for script in scriptList:
			if (self.__mainWindow.isScriptChecked(script.getName())):
				Log.printToLog("Script eval: " + script.getName())
				self.__API.evaluateCode(script.getSyntax(), script.getCode())

	# Reloads the Scripts UI Qt Elements
	def refreshScriptsUI (self, mode):
		scriptList = []
		scriptNames = []

		if mode == "pre": 
			scriptList = self.__preScriptList
			self.__mainWindow.setPreScriptsPathText(self.__preScriptsPath)
		elif mode == "post": 
			scriptList = self.__postScriptList
			self.__mainWindow.setPostScriptsPathText(self.__postScriptsPath)

		for script in scriptList:
			scriptNames.append(script.getName())

		self.__mainWindow.clearScriptRows(mode)
		self.__mainWindow.loadScriptRows(mode, scriptNames)

		for script in scriptNames:
			self.__mainWindow.disableScriptArrows (script, isTop = (scriptNames.index(script) == 0), isBottom = (scriptNames.index(script) == (len(scriptNames) - 1)))

	##### Actions #####

	# Shows the Log
	def showLog (self):
		Log.showLog()

	# Saves the current scene
	def saveScene (self):
		path = self.__API.browseFileSave("Scene Save Destination", "save")
		if path != None: 
			Log.printToLog("Saving  scene: " + path)
			self.__API.saveScene(path)

	# Exports the selected objects to the chosen path
	def exportSelected (self):
		path = self.__API.browseFileSave("FBX Export Destination", "fbx")

		if path != None:
			self.evaluateScripts("pre")
			Log.printToLog("Exporting selected: " + path)
			self.__API.exportSelected(path)
			self.evaluateScripts("post")

	# Opens the exports settings window
	def exportSettings (self):
		Log.printToLog("Export Settings Dialog")
		self.__API.exportSettings()
