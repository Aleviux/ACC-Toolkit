import abc

########################################
# API COMMUNICATOR ABSTRACT CLASS
########################################

class APICommunicator (object):
	
	__metaclass__ = abc.ABCMeta

	# Evaluates the given code according to the given syntax
	# Depending on the syntax, it executes the code string in different ways, returning different results:
	# * True -> If the check code was successful 
	# * False -> If the check code found an error
	# * -1 -> If the syntax is not supported in the application
	# * None -> If the code has no return value (ex: it's just a Fix code)
	@abc.abstractmethod
	def evaluateCode (self, syntax, code):
		pass

	# Opens the file browser dialog in folder-only mode
	@abc.abstractmethod
	def browseFileDir (self, message, startDir):
		pass

	# Opens the file load dialog in file loading mode
	@abc.abstractmethod
	def browseFileLoad (self, message, pattern):
		pass

	# Opens the file load dialog in file saving mode
	@abc.abstractmethod
	def browseFileSave (self, message, pattern):
		pass

	# Exports the selected scene elements to the given path as an FBX file
	@abc.abstractmethod
	def exportSelected (self, path):
		pass
	
	# Opens the FBX export configuration window
	@abc.abstractmethod
	def exportSettings (self):
		pass

	# Saves the current scene to the given path
	@abc.abstractmethod
	def saveScene (self, path):
		pass

	# Debug function: checks that the API Communicator is working correctly
	@abc.abstractmethod
	def debug_abstractTest (self):
		pass
