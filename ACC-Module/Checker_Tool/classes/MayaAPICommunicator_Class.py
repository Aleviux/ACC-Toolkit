from APICommunicator_Class import APICommunicator

########################################
# API COMMUNICATOR MAYA IMPLEMENTATION
########################################

class MayaAPICommunicator (APICommunicator):

	cmds = None

	def __init__ (self):
		import maya.cmds # Maya runtime module
		self.cmds = maya.cmds

	def evaluateCode (self, syntax, code):
		result = None

		if syntax.lower() == "python": # Python Evaluation

			# Check if supported API
			if "import pymxs" in code or "import MaxPlus" in code: return -1

			funcCall = ""

			split = ((code.split(":", 1))[0]).split(" ")
			for i in range(0, len(split)): 
				if (split[i] == "def"): funcCall = split[i + 1]
			if not ("()" in funcCall): funcCall += "()"

			exec(code)
			exec("result = {0}".format(funcCall))

		elif syntax.lower() == "mel": # MEL Evaluation

			funcCall = ""

			split = ((code.split("{", 1))[0]).split(" ")
			for i in range(0, len(split)): 
				if (split[i] == "proc"): funcCall = split[i + 2]
			if not ("()" in funcCall): funcCall += "()"

			import maya.mel as mel
			mel.eval(code)
			result = mel.eval(funcCall)

		elif syntax.lower() == "maxscript": result = -1 # MaxScript Evaluation (not supported)

		if result == True or result == False or result == -1: 
			return result
		else: 
			return None

	def browseFileDir (self, message, startDir = ""):
		file = self.cmds.fileDialog2 (caption = message, startingDirectory = startDir, fileMode = 3, okCaption = "Choose Folder", dialogStyle = 2)
		if file != None: return file[0]

	def browseFileLoad (self, message = "", pattern = "All Formats (*.*)"):
		if pattern == "save": pattern = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
		elif pattern == "fbx": pattern = "Autodesk (*.fbx)"
		elif pattern == "script": pattern = "Python (*.py);;MEL (*.mel)"

		file = self.cmds.fileDialog2 (caption = message, fileFilter = pattern, startingDirectory = (self.cmds.workspace(q = True, dir = True)), okCaption = "Load File", dialogStyle = 2)
		if file != None: return file[0]

	def browseFileSave (self, message = "", pattern = "All Formats (*.*)"):
		if pattern == "save": pattern = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb)"
		elif pattern == "fbx": pattern = "Autodesk (*.fbx)"
		elif pattern == "script": pattern = "Python (*.py);;MEL (*.mel)"

		file = self.cmds.fileDialog2 (caption = message, fileFilter = pattern, startingDirectory = (self.cmds.workspace(q = True, dir = True)), okCaption = "Save File", dialogStyle = 2)
		if file != None: return file[0]

	def exportSelected (self, path):
		import pymel.core as pm
		pm.loadPlugin("fbxmaya")
		pm.mel.FBXExport(f = path)

	def exportSettings (self):
		import pymel.core as pm
		pm.loadPlugin("fbxmaya")
		pm.mel.ExportSelection()

	def saveScene (self, path):
		sceneName = self.cmds.file(query = True, sceneName = True, shortName = True)
		ext = (sceneName.split("."))[-1]

		self.cmds.file(rename = path)
		if ext == "ma": self.cmds.file(save = True, f = True, type = "mayaAscii")
		elif ext == "mb": self.cmds.file(save = True, f = True, type = "mayaBinary")

	def debug_abstractTest (self):
		print ("MayaAPICommunicator Abstract Test Working!")
