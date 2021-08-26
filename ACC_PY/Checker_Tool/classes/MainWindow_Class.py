# encoding: utf-8

# Pyside 2.0 Qt support
from PySide2 import QtWidgets as QWidget
from PySide2 import QtGui as QGui
from PySide2 import QtCore as QCore

from classes.MainWindowUI_QtClass import Ui_MainWindow as MainWindowUI
from classes.RuleUI_QtClass import Ui_MainWindow as RuleUI

import classes.MainWindowManager_Class

########################################
# MAIN WINDOW VIEW
########################################

class ScriptRow (QWidget.QWidget): # QWidget for each Script Row in the Main Window script list
	
	__Manager = None
	__scriptName = ""

	# Class constructor
	def __init__ (self, sName):
		super(ScriptRow, self).__init__()

		# Python 2 metaclasses
		# self.__Manager = classes.MainWindowManager_Class.MainWindowManager.__metaclass__\
		# .getInstance(classes.MainWindowManager_Class.MainWindowManager)

		# Python 3 metaclasses
		self.__Manager = classes.MainWindowManager_Class.MainWindowManager\
		.getInstance(classes.MainWindowManager_Class.MainWindowManager)

		self.__scriptName = sName

		self.createUI()
		self.setupSignals()

	# Qt UI Creation
	def createUI (self):
		lyt = QWidget.QHBoxLayout()

		self.chk_enabled = QWidget.QCheckBox("\t" + self.__scriptName, self)
		self.chk_enabled.setCheckState(QCore.Qt.Checked)
		self.btn_up = QWidget.QPushButton("▲")
		self.btn_up.setMaximumWidth(20)
		self.btn_down = QWidget.QPushButton("▼")
		self.btn_down.setMaximumWidth(20)

		lyt.addWidget(self.chk_enabled)
		lyt.addWidget(self.btn_up)
		lyt.addWidget(self.btn_down)

		self.setLayout(lyt)

	# Qt Signals Conections
	def setupSignals (self):
		self.chk_enabled.clicked.connect(lambda : self.__Manager.toggleScript(self.__scriptName))
		self.btn_up.clicked.connect(lambda : self.__Manager.raiseScript(self.__scriptName))
		self.btn_down.clicked.connect(lambda : self.__Manager.lowerScript(self.__scriptName))

	# Returns whether the Script Row is checked
	def isChecked (self):
		return bool(self.chk_enabled.isChecked())

	# Checks or unchecks the Script Row
	def setChecked (self, checked):
		self.chk_enabled.setChecked(checked)

	# Disables the up and down arrows for the Script Row
	def disableArrows (self, isTop, isBottom):
		self.btn_up.setEnabled(not isTop)
		self.btn_down.setEnabled(not isBottom)

class RuleRow (QWidget.QWidget): # QWidget for each Rule Row in the Main Window rules list

	__Manager = None
	__ruleName = ""

	# Class constructor
	def __init__ (self, rName):
		super(RuleRow, self).__init__()

		# Python 2 metaclasses
		# self.__Manager = classes.MainWindowManager_Class.MainWindowManager.__metaclass__\
		# .getInstance(classes.MainWindowManager_Class.MainWindowManager)

		# Python 3 metaclasses
		self.__Manager = classes.MainWindowManager_Class.MainWindowManager\
		.getInstance(classes.MainWindowManager_Class.MainWindowManager)

		self.__ruleName = rName

		self.createUI()
		self.setupSignals()

	# Qt UI Creation
	def createUI (self):
		lytV = QWidget.QHBoxLayout()

		wdgH1 = QWidget.QWidget()
		wdgH1.setMaximumWidth(20)
		lytH1 = QWidget.QHBoxLayout()

		wdgH2 = QWidget.QWidget()
		lytH2 = QWidget.QHBoxLayout()

		self.chk_enabled = QWidget.QCheckBox("", self)
		self.chk_enabled.setMaximumWidth(20)
		self.setChecked(True)

		self.lab_ruleName = QWidget.QLabel(self.__ruleName)
		self.lab_ruleName.setAlignment(QCore.Qt.AlignCenter)

		self.lab_ruleStatus = QWidget.QLabel("Status")
		self.lab_ruleStatus.setAlignment(QCore.Qt.AlignCenter)
		self.lab_ruleStatus.setMaximumWidth(400)

		self.btn_ruleCheck = QWidget.QPushButton("Check")
		self.btn_ruleCheck.setMaximumWidth(40)
		self.btn_ruleFix = QWidget.QPushButton("Fix")
		self.btn_ruleFix.setMaximumWidth(40)
		self.btn_ruleFix.setEnabled(False)
		self.btn_ruleEdit = QWidget.QPushButton("Edit")
		self.btn_ruleEdit.setMaximumWidth(40)
		self.btn_ruleDelete = QWidget.QPushButton("Delete")
		self.btn_ruleDelete.setMaximumWidth(40)
		self.btn_ruleInfo = QWidget.QPushButton("Info")
		self.btn_ruleInfo.setMaximumWidth(40)
		self.btn_up = QWidget.QPushButton("▲")
		self.btn_up.setMaximumWidth(20)
		self.btn_down = QWidget.QPushButton("▼")
		self.btn_down.setMaximumWidth(20)

		lytH1.addWidget(self.chk_enabled)
		lytH2.addWidget(self.btn_ruleCheck)
		lytH2.addWidget(self.btn_ruleFix)
		lytH2.addWidget(self.btn_ruleEdit)
		lytH2.addWidget(self.btn_ruleDelete)
		lytH2.addWidget(self.btn_ruleInfo)
		lytH2.addWidget(self.lab_ruleName)
		lytH2.addWidget(self.lab_ruleStatus)
		lytH2.addWidget(self.btn_up)
		lytH2.addWidget(self.btn_down)

		lytV.addWidget(wdgH1)
		lytV.addWidget(wdgH2)

		wdgH1.setLayout(lytH1)
		wdgH2.setLayout(lytH2)
		self.setLayout(lytV)

	# Qt Signals Conections
	def setupSignals (self):
		self.chk_enabled.clicked.connect(lambda : self.__Manager.toggleRule(self.__ruleName))
		self.btn_ruleCheck.clicked.connect(lambda : self.__Manager.checkRule(self.__ruleName))
		self.btn_ruleFix.clicked.connect(lambda : self.__Manager.fixRule(self.__ruleName))
		self.btn_ruleDelete.clicked.connect(self.confirmRuleDeleteDialog)
		self.btn_ruleInfo.clicked.connect(lambda : self.__Manager.showRuleInfo(self.__ruleName))
		self.btn_up.clicked.connect(lambda : self.__Manager.raiseRule(self.__ruleName))
		self.btn_down.clicked.connect(lambda : self.__Manager.lowerRule(self.__ruleName))

	# Returns whether the Rule Row is checked
	def isChecked (self):
		return self.chk_enabled.isChecked()

	# Checks or unchecks the Rule Row
	def setChecked (self, checked):
		self.chk_enabled.setChecked(checked)

	# Creates a dialog to confirm the Rule Row deletion
	def confirmRuleDeleteDialog (self):
		msgB = QWidget.QMessageBox()

		msgB.setWindowTitle("Warning!")
		msgB.setText("The rule \"" + self.__ruleName + "\" will be deleted! Do you wish to continue?")
		msgB.setStandardButtons(QWidget.QMessageBox.Ok | QWidget.QMessageBox.Cancel);
		msgB.setDefaultButton(QWidget.QMessageBox.Cancel);

		chosen = msgB.exec_()
		if chosen == QWidget.QMessageBox.Ok:
			self.__Manager.deleteRule(self.__ruleName)

	# Sets the Rule Row to the desired status (Not Checked, Needs Fixing, Correct or Unsupported API)
	def setStatus (self, status, isFixable):
		if status == 0: # Rule not checked
			self.lab_ruleStatus.setText("NOT CHECKED!")
			self.lab_ruleStatus.setStyleSheet("QLabel {background-color:yellow; color:black; font-weight: bold}")
			self.setFixable (False)
		elif status == 1: # Rule checked and needs to be fixed
			self.lab_ruleStatus.setText("NEEDS FIXING!")
			self.lab_ruleStatus.setStyleSheet("QLabel {background-color:red; color:black; font-weight: bold}")
			self.setFixable (isFixable)
		elif status == 2: # Rule checked and is correct
			self.lab_ruleStatus.setText("CORRECT!")
			self.lab_ruleStatus.setStyleSheet("QLabel {background-color:green; color:black; font-weight: bold}")
			self.setFixable (False)
		elif status == (-1): # Rule can't be checked because it uses a not supported API
			self.lab_ruleStatus.setText("UNSUPPORTED API!")
			self.lab_ruleStatus.setStyleSheet("QLabel {background-color:magenta; color:black; font-weight: bold}")
			self.setFixable (False)
		elif status == (-2): # Rule can't be checked because it is disabled
			self.lab_ruleStatus.setText("DISABLED")
			self.lab_ruleStatus.setStyleSheet("QLabel {background-color:gray; color:black; font-weight: bold}")
			self.setFixable (False)

	# Sets the Rule Row as fixable (enables/disables the Fix button)
	def setFixable (self, isFixable):
		self.btn_ruleFix.setEnabled(isFixable)

	# Enables/Disables the Rule Row
	def toggle (self, toggle):
		row = self.lab_ruleName.parentWidget()
		row.setEnabled(toggle)

		if toggle: self.setStatus(0, False)
		else: self.setStatus(-2, False)

	# Disables the up and down arrows for the Rule Row
	def disableArrows (self, isTop, isBottom):
		self.btn_up.setEnabled(not isTop)
		self.btn_down.setEnabled(not isBottom)

class RuleWindow (QWidget.QMainWindow, RuleUI): # QWidget for the Rule Window data input

	__Manager = None
	__ruleData = None

	# Class constructor
	def __init__ (self):
		super(RuleWindow, self).__init__()

		# Python 2 metaclasses
		# self.__Manager = classes.MainWindowManager_Class.MainWindowManager.__metaclass__\
		# .getInstance(classes.MainWindowManager_Class.MainWindowManager)

		# Python 3 metaclasses
		self.__Manager = classes.MainWindowManager_Class.MainWindowManager\
		.getInstance(classes.MainWindowManager_Class.MainWindowManager)
		
		self.setupUi(self)
		self.txt_checkCode.setTabStopWidth(self.txt_checkCode.fontMetrics().width(' ') * 8)
		self.txt_fixCode.setTabStopWidth(self.txt_fixCode.fontMetrics().width(' ') * 8)
		self.setupSignals()

		self.__ruleData = {
			"Name" : "",
			"Desc" : "",
			"CheckCode" : "",
			"CheckSyntax" : (self.cmb_checkCode.currentText()),
			"FixCode" : "",
			"FixSyntax" : (self.cmb_fixCode.currentText())
		}

		self.setWindowTitle("Rule Data")
		self.setWindowFlags(QCore.Qt.WindowStaysOnTopHint)

	# Qt Signals Conections
	def setupSignals (self):
		self.txt_ruleName.textEdited.connect(lambda : self.setRuleData({"Name": self.txt_ruleName.text()}))
		self.txt_ruleDesc.textChanged.connect(lambda : self.setRuleData({"Desc": self.txt_ruleDesc.toPlainText()}))

		self.cmb_checkCode.currentIndexChanged.connect(lambda : self.setRuleData({"CheckSyntax": self.cmb_checkCode.currentText()}))
		self.txt_checkCode.textChanged.connect(lambda : self.setRuleData({"CheckCode": self.txt_checkCode.toPlainText()}))
		self.btn_ruleCheckBrowse.clicked.connect(self.__Manager.browseCheckCode)

		self.cmb_fixCode.currentIndexChanged.connect(lambda : self.setRuleData({"FixSyntax": self.cmb_fixCode.currentText()}))
		self.txt_fixCode.textChanged.connect(lambda : self.setRuleData({"FixCode": self.txt_fixCode.toPlainText()}))
		self.btn_ruleFixBrowse.clicked.connect(self.__Manager.browseFixCode)

	# Qt Window Close Event
	def closeEvent (self, event):
		event.accept()
		del self

	# Sets the Rule data properties from given input
	def setRuleData (self, rData):
		for prop in rData.keys():
			if prop in self.__ruleData:
				self.__ruleData[prop] = rData[prop]

	# Sets the Rule data properties to the window UI
	def setRuleDataUI (self):
		self.txt_ruleName.setText(self.__ruleData["Name"])
		self.txt_ruleDesc.setText(self.__ruleData["Desc"])
		
		synt = self.cmb_checkCode.findText(self.__ruleData["CheckSyntax"], QCore.Qt.MatchFixedString)
		if synt >= 0: self.cmb_checkCode.setCurrentIndex(synt)
		self.txt_checkCode.setText(self.__ruleData["CheckCode"])

		synt = self.cmb_fixCode.findText(self.__ruleData["FixSyntax"], QCore.Qt.MatchFixedString)
		if synt >= 0: self.cmb_fixCode.setCurrentIndex(synt)
		self.txt_fixCode.setText(self.__ruleData["FixCode"])

	# Sends the rule data to the Manager, if valid
	def sendRuleData (self, editMode, rName = ""):
		if self.__ruleData["Name"] != "" and self.__ruleData["CheckCode"] != "": # Enough rule data
			if rName == "": rName = self.__ruleData["Name"]

			if editMode: self.__Manager.editRule (rName, self.__ruleData["Name"], self.__ruleData)
			else: self.__Manager.createRule (self.__ruleData)

			self.close()

		else: # Rule data insufficient
			msgB = QWidget.QMessageBox()

			msgB.setWindowTitle("Insufficient Rule Data!")
			msgB.setText("Please, you must specify a Name and valid Check Function for the rule!")
			msgB.exec_()

class MainWindow (QWidget.QMainWindow, MainWindowUI): # QWidget for the Main Window

	__Manager = None
	__ruleWindow = None

	__ruleRows = None
	__scriptRows = None

	############################
	##### Window Functions #####
	############################
	
	# Class constructor
	def __init__ (self):
		super(MainWindow, self).__init__()

		# Python 2 metaclasses
		# self.__Manager = classes.MainWindowManager_Class.MainWindowManager.__metaclass__\
		# .getInstance(classes.MainWindowManager_Class.MainWindowManager)

		# Python 3 metaclasses
		self.__Manager = classes.MainWindowManager_Class.MainWindowManager\
		.getInstance(classes.MainWindowManager_Class.MainWindowManager)

		self.setupUi(self)
		self.setupSignals()

		self.__ruleRows = {}
		self.clearRuleRows()

		self.__scriptRows = {}
		self.clearScriptRows("pre")
		self.clearScriptRows("post")

		self.setCurrentProfileText()

		self.resetProgressBar()

		self.setWindowTitle("Checker Tool")
		self.setWindowFlags(QCore.Qt.WindowStaysOnTopHint)

	# Qt Signals Conections
	def setupSignals (self):
		self.menuProfileSave.triggered.connect(self.__Manager.saveProfile)
		self.menuProfileLoad.triggered.connect(self.__Manager.changeProfilePath)
		self.menuProfileClear.triggered.connect(self.__Manager.clearProfile)

		self.btn_rulesPathBrowse.clicked.connect(self.__Manager.changeRulePath)

		self.btn_addRule.clicked.connect(self.createRuleUI)
		self.btn_checkRules.clicked.connect(self.__Manager.checkAllRules)
		self.btn_fixRules.clicked.connect(self.__Manager.fixAllRules)
		self.btn_deleteRules.clicked.connect(self.confirmRuleDeleteAllDialog)

		self.btn_preScriptsPathBrowse.clicked.connect(self.__Manager.changePreScriptsPath)
		self.btn_postScriptsPathBrowse.clicked.connect(self.__Manager.changePostScriptsPath)

		self.btn_log.clicked.connect(self.__Manager.showLog)
		self.btn_saveScene.clicked.connect(self.__Manager.saveScene)
		self.btn_exportSelected.clicked.connect(self.__Manager.exportSelected)
		self.btn_exportSettings.clicked.connect(self.__Manager.exportSettings)

	# Qt Window Show Function
	def showWindow (self):
		self.show()
		self.setFocus()
		self.activateWindow()

	# Qt Window Close Event
	def closeEvent (self, event):
		event.accept()

	############################
	##### Profiles MenuBar #####
	############################

	# Changes the display name for the current loaded Profile
	def setCurrentProfileText(self, profile = None):
		self.menuProfileCurrent.setTitle("Current Profile: " + str(profile))

	############################
	##### Rule Data Window #####
	############################

	# Opens the Rule Creation Window
	def createRuleUI (self):
		self.__ruleWindow = RuleWindow()
		self.__ruleWindow.btn_ruleCreate.clicked.connect(lambda : self.__ruleWindow.sendRuleData (False))
		
		self.__ruleWindow.setWindowModality(QCore.Qt.ApplicationModal)
		self.__ruleWindow.show()

	# Opens the Rule Edit Window
	def editRuleUI (self, rName, rData):
		self.__ruleWindow = RuleWindow()
		self.__ruleWindow.btn_ruleCreate.clicked.connect(lambda : self.__ruleWindow.sendRuleData (True, rName))

		self.__ruleWindow.setRuleData(rData)
		self.__ruleWindow.setRuleDataUI()
		
		self.__ruleWindow.setWindowModality(QCore.Qt.ApplicationModal)
		self.__ruleWindow.show()

	# Updates the Rule Window's rule data from given input
	def setRuleWindowData (self, rData):
		if self.__ruleWindow != None:
			self.__ruleWindow.setRuleData(rData)
			self.__ruleWindow.setRuleDataUI()

	#####################
	##### Rule Rows #####
	#####################

	# Updates the Rule Path text label
	def setRulePathText (self, text):
		self.lab_rulesPath.setText(text)

	# Adds the Rule Row
	def addRuleRow (self, rName):
		rule_row = RuleRow(rName)
		rule_row.setStatus(0, False)
		self.__ruleRows[rName] = rule_row

		lyt = self.scrollAreaWidgetContents_rulesList.layout()
		lyt.insertWidget((lyt.count() - 1), rule_row)

		rData = self.__Manager.getRuleData(rName)
		rule_row.btn_ruleEdit.clicked.connect(lambda : self.editRuleUI (rName, rData))

	# Clears the Rule Rows List
	def clearRuleRows (self):
		lyt = self.scrollAreaWidgetContents_rulesList.layout()

		while lyt.count():
			child = lyt.takeAt(0)

			if child.widget():
				child.widget().close()
				child.widget().deleteLater()

		lyt.addStretch()

		rules = list(self.__ruleRows.keys())
		for ruleRow in rules:
			del self.__ruleRows[ruleRow]

	# Deletes the Rule Row
	def deleteRuleRow (self, rName):
		del self.__ruleRows[rName]

	# Creates a dialog to confirm the deletion of all the Rule Rows
	def confirmRuleDeleteAllDialog (self):
		msgB = QWidget.QMessageBox()

		msgB.setWindowTitle("Warning!")
		msgB.setText("ALL RULES will be deleted! Are you sure you wish to continue?")
		msgB.setStandardButtons(QWidget.QMessageBox.Ok | QWidget.QMessageBox.Cancel);
		msgB.setDefaultButton(QWidget.QMessageBox.Cancel);

		chosen = msgB.exec_()
		if chosen == QWidget.QMessageBox.Ok:
			self.__Manager.deleteAllRules()

	# Creates a dialog to show the Rule Row info description
	def ruleInfoDialog (self, name, desc):
		msgB = QWidget.QMessageBox()
		msgB.setWindowTitle(name)
		msgB.setText(desc)
		msgB.exec_()

	# Sets the desired status for the desired Rule Row
	def setRuleRowStatus (self, rName, status, isFixable = False):
		if rName in self.__ruleRows:
			self.__ruleRows[rName].setStatus(status, isFixable)

	# Returns the checked value of the desired Rule Row
	def isRuleChecked (self, rName):
		if rName in self.__ruleRows:
			return self.__ruleRows[rName].isChecked()

	# Checks or unchecks the desired Rule Row
	def setRuleChecked (self, rName, checked):
		if rName in self.__ruleRows:
			self.__ruleRows[rName].setChecked(checked)

	# Toggles the desired rule
	def toggleRuleRow (self, rName, toggle):
		if rName in self.__ruleRows:
			self.__ruleRows[rName].toggle(toggle)

	# Disables the up and down  arrows for the desired Script Row
	def disableRuleRowArrows (self, rName, isTop = False, isBottom = False):
		if rName in self.__ruleRows.keys(): 
			self.__ruleRows[rName].disableArrows(isTop, isBottom)

	#######################
	##### Script Rows #####
	#######################

	# Updates the Pre-Scripts Path text label
	def setPreScriptsPathText (self, text):
		self.lab_preScriptsPath.setText(text)

	# Updates the Post-Scripts Path text label
	def setPostScriptsPathText (self, text):
		self.lab_postScriptsPath.setText(text)

	# Loads the Script Rows
	def loadScriptRows (self, mode, scripts):
		scroll_lyt = None
		if mode == "pre": scroll_lyt = self.scrollAreaWidgetContents_preScripts.layout()
		elif mode == "post": scroll_lyt = self.scrollAreaWidgetContents_postScripts.layout()

		for script in scripts:
			scriptRow = ScriptRow(script)
			self.__scriptRows[script] = scriptRow
			scroll_lyt.insertWidget((scroll_lyt.count() - 1), scriptRow)

	# Clears the Script Rows List
	def clearScriptRows (self, mode):
		scroll_lyt = None

		if mode == "pre": scroll_lyt = self.scrollAreaWidgetContents_preScripts.layout()
		elif mode == "post": scroll_lyt = self.scrollAreaWidgetContents_postScripts.layout()

		while scroll_lyt.count():
			child = scroll_lyt.takeAt(0)

			if child.widget():
				child.widget().close()
				child.widget().deleteLater()

		scroll_lyt.addStretch()

	# Returns the checked value of the desired Script Row
	def isScriptChecked (self, script):
		if script in self.__scriptRows: 
			return self.__scriptRows[script].isChecked()

	# Checks or unchecks the desired Script Row
	def setScriptChecked (self, script, checked):
		if script in self.__scriptRows: 
			self.__scriptRows[script].setChecked(checked)

	# Disables the up and down  arrows for the desired Script Row
	def disableScriptArrows (self, script, isTop = False, isBottom = False):
		if script in self.__scriptRows.keys(): 
			self.__scriptRows[script].disableArrows(isTop, isBottom)

	########################
	##### Progress Bar #####
	########################

	# Sets the given value to the progress bar
	def setProgressBarValue(self, value):
		self.progressBar.setValue(value)

	# Resets the progress bar back to zero
	def resetProgressBar(self):
		self.progressBar.reset()
