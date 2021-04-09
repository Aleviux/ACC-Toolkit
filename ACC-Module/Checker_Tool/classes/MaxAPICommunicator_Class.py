from APICommunicator_Class import APICommunicator

########################################
# API COMMUNICATOR MAX IMPLEMENTATION
########################################

class MaxAPICommunicator (APICommunicator):

	rt = None

	def __init__ (self):
		import pymxs # Max runtime module (MaxPlus not supported on Max 2021+)
		self.rt = pymxs.runtime

	def evaluateCode (self, syntax, code):
		result = None

		if syntax.lower() == "python": # Python Evaluation

			# Check if supported API
			if "import maya.cmds" in code or "import maya.mel" in code or "import pymel.core" in code: return -1 
			
			funcCall = ""

			split = ((code.split(":", 1))[0]).split(" ")
			for i in range(0, len(split)): 
				if (split[i] == "def"): funcCall = split[i + 1]
			if not ("()" in funcCall): funcCall += "()"

			exec(code)
			exec("result = {0}".format(funcCall))

		elif syntax.lower() == "maxscript": # MaxScript Evaluation

			funcCall = ""

			split = ((code.split("=", 1))[0]).split(" ")
			for i in range(0, len(split)): 
				if (split[i] == "fn"): funcCall = split[i + 1]
			
			self.rt.execute(code)
			self.rt.execute("result = " + funcCall + "()")
			result = self.rt.result

		elif syntax.lower() == "mel": result = -1 # MEL Evaluation (not supported)

		if result == True or result == False or result == -1: 
			return result
		else: 
			return None

	def browseFileDir (self, message, startDir = ""):
		file = self.rt.getSavePath (caption = message, initialDir = startDir)
		if file != None: return file

	def browseFileLoad (self, message = "", pattern = "All Formats|*.*"):
		if pattern == "save": pattern = "3ds Max (*.max)|*.max"
		elif pattern == "fbx": pattern = "Autodesk (*.fbx)|*.fbx"
		elif pattern == "script": pattern = "Python (*.py)|*.py|MaxScript (*.ms)|*.ms"
		
		file = self.rt.getOpenFileName (caption = message, types = pattern, filename = self.rt.maxfilepath)
		if file != None: return file

	def browseFileSave (self, message = "", pattern = "All Formats|*.*"):
		if pattern == "save": pattern = "3ds Max (*.max)|*.max"
		elif pattern == "fbx": pattern = "Autodesk (*.fbx)|*.fbx"
		elif pattern == "script": pattern = "Python (*.py)|*.py|MaxScript (*.ms)|*.ms"
		
		file = self.rt.getSaveFileName (caption = message, types = pattern, filename = self.rt.maxfilepath)
		if file != None: return file

	def exportSelected (self, path):
		self.rt.exportfile (path, self.rt.Name("noPrompt"), selectedOnly = True)

	def exportSettings (self):
		self.rt.OpenFbxSetting()

	def saveScene (self, path):
		self.rt.saveMaxFile(path)

	def debug_abstractTest (self):
		print ("MaxAPICommunicator Abstract Test Working!")
