########################################
# SCRIPT CLASS
########################################

class Script ():

    __name = ""
    __code = ""
    __syntax = "" 

    # Class constructor
    def __init__ (self, name, code, syntax):
        self.__name = name
        self.__code = code
        self.__syntax = syntax

    # Returns the Script Object Name
    def getName (self):
        return self.__name

    # Returns the Script Object Code
    def getCode (self):
        return self.__code

    # Returns the Script Object Syntax
    def getSyntax (self):
        return self.__syntax
