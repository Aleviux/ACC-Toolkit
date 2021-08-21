########################################
# RULE CLASS
########################################

class Rule ():

    __isEnabled = True
    __isFixable = False
    __properties = None
    
    # Class constructor
    def __init__ (self):
        self.__properties = {
            "Name" : None,
            "Desc" : None,
            "CheckCode" : None,
            "CheckSyntax" : None,
            "FixCode" : None,
            "FixSyntax" : None
        } 

    # Sets the given properties data to the Rule Object
    def setProperties (self, jsonData):
        for prop in jsonData:
            if prop in self.__properties:
                self.__properties[prop] = jsonData[prop]

    # Returns the desired property data from the Rule Object
    def getProperty (self, prop):
        if prop in self.__properties:
            return self.__properties[prop]

    # Returns whether the Rule Object is marked as fixable
    def isFixable (self):
        return self.__isFixable

    # Sets the Rule Object to be fixable if desired, providing it has some Fix Code on its properties
    def setFixable (self, fixable):
        self.__isFixable = fixable and self.__properties["FixCode"] != "" and self.__properties["FixCode"] != None

    # Returns whether the Rule Object is enabled
    def isEnabled (self):
        return self.__isEnabled

    # Sets the Rule Object to be enabled or disabled
    def setEnabled (self, enabled):
        self.__isEnabled = enabled

    # Debug function: returns a formatted string with all the Rule Object property data
    def debug_printRule (self):
        rData = ('Rule Data:' + '\n' 
            + '    --- Name: ' + self.__properties["Name"] + '\n' 
            + '    --- Description: ' + self.__properties["Desc"] + '\n' 
            + '    --- Check Code ({0}): '.format(self.__properties["CheckSyntax"]) 
            + '\n' + self.__properties["CheckCode"] + '\n' 
            + '    --- Fix Code ({0}): '.format(self.__properties["FixSyntax"]) 
            + '\n' + self.__properties["FixCode"] + '\n')
        return rData
