########################################
# LOG STATIC CLASS
########################################

class Log ():
	
	__logFilePath = ''
	__logFileName = 'Log.txt'

	# Sets the directory where to save the Log file
	@classmethod
	def setLogPath (cls, fileDir):
		cls.__logFilePath = fileDir + "/" + cls.__logFileName

	# Creates the Log, with empty content
	@classmethod
	def createLog (cls):
		log_file = open (cls.__logFilePath, "w")
		log_file.write("LOG" + "\n" + "---" + "\n")
		log_file.close()

	# Resets the Log content, creating it again
	@classmethod
	def clearLog (cls):
		Log.createLog()

	# Adds the given message to the Log and prints it to the output console
	@classmethod
	def printToLog (cls, message):
		log_file = open (cls.__logFilePath, "a")
		log_file.write(message + "\n")
		log_file.close()

		print("LOG --- " + message)

	# Returns all written text from the Log
	@classmethod
	def readLog (cls):
		log_file = open (cls.__logFilePath, "r")
		logData = log_file.readlines()
		log_file.close()

		return logData

	# Shows the Log in the default app configured to open txt in the user's PC
	@classmethod
	def showLog (cls):
		import os
		os.startfile(cls.__logFilePath)
