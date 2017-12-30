import sysimport osimport platformimport subprocessimport threadingimport shutilimport previewUI#Packages used: PyQt5, PyMuPDF(fitz)...from PyQt5.QtWidgets import *from PyQt5.QtCore import QDate, QFile, Qt, QTextStream, pyqtSlot, QThread, pyqtSignalfrom PyQt5.QtGui import QIcon, QTextDocument, QTextCursor, QPixmap, QPaletteimport fitz#Build project from this file to run program#mainWindow class is used to create an instance of the text editor window.class EditorWindow(QMainWindow):    #Initializes an instance of mainWindow and QMainWindow class    def __init__(self):        super().__init__()        self.setCurrentFile('')        self.initUI()    def initUI(self):        #Setting properties for the newly initialized window        self.setWindowTitle('LaTeX editor')        self.toolbar = self.addToolBar('Toolbar')        WindowUtilityFunctions.setTopLeft(self)        self.resize(screenX/2, screenY/1.25)        self.init_menuBar()        self.footerBar_init()        self.leftDock_sideBar()        self.mainActivity_init()        self.toolBar_init()        self.show()    def closeEvent(self, event):        close_dialogBox = QMessageBox()        if self.text.document().isModified():            close_dialogBox.setText("Current loaded document has not been saved.\nDo you want to save the document and then quit?")            close_dialogBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)            response = close_dialogBox.exec_()            if response == QMessageBox.Yes:                self.saveFile_action()                if self.text.document().isModified() == True:                    event.ignore()                else:                    event.accept()            elif response == QMessageBox.No:                event.accept()            else:                event.ignore()                    else:            close_dialogBox.setText("Are you sure you want to quit?")            close_dialogBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)            if close_dialogBox.exec_() == QMessageBox.Yes:                event.accept()            else:                event.ignore()                def closeEvent_quitButton(self):        #Modified closeEvent method to ensure that quit button works from menu bar as quit button passes a bool (and not an event).        close_dialogBox = QMessageBox()        if self.text.document().isModified():            close_dialogBox.setText("Current loaded document has not been saved.\nDo you want to save the document and then quit?")            close_dialogBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)            response = close_dialogBox.exec_()                        if response == QMessageBox.Yes:                self.saveFile_action()                qApp.quit()            elif response == QMessageBox.No:                qApp.quit()            else:                pass        else:            close_dialogBox.setText("Are you sure you want to quit?")            close_dialogBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)            if close_dialogBox.exec_() == QMessageBox.Yes:                qApp.quit()            else:                pass    def mainActivity_init(self):        #Initializes an editable text box and sets it as the central widget to cover the whole window.        self.text = QTextEdit(self)        self.setCentralWidget(self.text)    def init_menuBar(self):        menuBar = self.menuBar()        fileMenu = menuBar.addMenu('&File')        quitAction = fileMenu.addAction('Quit')        quitAction.triggered.connect(self.closeEvent_quitButton)        newFile_fileMenu = fileMenu.addAction('&New File')        newFile_fileMenu.setShortcut('CTRL+N')        newFile_fileMenu.triggered.connect(self.newFile_action)        openFile_fileMenu = fileMenu.addAction('&Open document...')        openFile_fileMenu.setShortcut('CTRL+O')        openFile_fileMenu.triggered.connect(self.openFile_action)        save_fileMenu = fileMenu.addAction('&Save')        save_fileMenu.setShortcut('CTRL+S')        save_fileMenu.triggered.connect(self.saveFile_action)        saveAs_fileMenu = fileMenu.addAction('&Save as...')        saveAs_fileMenu.setShortcut('CTRL+SHIFT+S')        saveAs_fileMenu.triggered.connect(self.saveAs)        editMenu = menuBar.addMenu('&Edit')        undo_editMenu = editMenu.addAction('Undo')        undo_editMenu.setShortcut('CTRL+Z')        #Lambda expressions used to ensure that methods function properly when called on event trigger.        undo_editMenu.triggered.connect(lambda: \                    (self.text.undo(), self.footerBar_setMessage("Menu -> Edit: Undo", 500)))                redo_editMenu = editMenu.addAction('Redo')        redo_editMenu.setShortcut('CTRL+Y')        redo_editMenu.triggered.connect(self.redoAction)        findText_editMenu = editMenu.addAction('Find text...')        findText_editMenu.setShortcut('CTRL+F')        findText_editMenu.triggered.connect(lambda: self.testing_QLineEdit.setFocus())        editMenu.addSeparator()        cut_editMenu = editMenu.addAction('Cut')        cut_editMenu.setShortcut('CTRL+X')        cut_editMenu.triggered.connect(lambda: \                    (self.text.cut(), self.footerBar_setMessage("Menu -> Edit: Cut", 500)))        copy_editMenu = editMenu.addAction('Copy')        copy_editMenu.setShortcut('CTRL+C')        copy_editMenu.triggered.connect(lambda: \                    (self.text.copy(), self.footerBar_setMessage("Menu -> Edit: Copy", 500)))        paste_editMenu = editMenu.addAction('Paste')        paste_editMenu.setShortcut('CTRL+V')        paste_editMenu.triggered.connect(lambda: \                    (self.text.paste(), self.footerBar_setMessage("Menu -> Edit: Paste", 500)))        viewMenu = menuBar.addMenu('&View')        view_Test = viewMenu.addAction('Filler')        windowMenu = menuBar.addMenu('&Window')        window_Test = windowMenu.addAction('Filler')        window_Preferences = windowMenu.addAction('Preferences')        #Need to add preferences menu as a new window to adjust visual settings on editor.        helpMenu = menuBar.addMenu('&Help')        if WindowUtilityFunctions.isMacOS() == True:            print("-- Help menu items appears in the 'applicationName' dropdown menu on MacOS.")        helpMenu_about = helpMenu.addAction('About')        helpMenu_about.triggered.connect(self.about)        self.show()     def toolBar_init(self):        self.toolbar.setMovable(False)        self.toolbar.setMinimumSize(0,30)        self.openFile = QAction(QIcon('Assets/Icons/of_Icon.png'), '&Open file', self)        self.openFile.setShortcut('CTRL+O')        self.openFile.triggered.connect(self.openFile_action)        self.toolbar.addAction(self.openFile)        self.saveFile = QAction(QIcon('Assets/Icons/sf_Icon.png'), '&Save file', self)        self.saveFile.setShortcut('CTRL+S')        self.saveFile.triggered.connect(self.saveFile_action)        self.toolbar.addAction(self.saveFile)        self.newFile = QAction(QIcon('Assets/Icons/nf_Icon.png'), '&New file', self)        self.newFile.setShortcut('CTRL+N')        self.newFile.triggered.connect(self.newFile_action)        self.toolbar.addAction(self.newFile)        self.previewTexFile = QAction(QIcon('Assets/Icons/pftex_Icon.png'), '&Preview in LaTeX format', self)        self.previewTexFile.triggered.connect(self.previewTex)        self.toolbar.addAction(self.previewTexFile)        self.toolbar_spacer()        self.findText_toolbar()        self.show()    def toolbar_spacer(self):        tb_Spacer = QWidget()        tb_Spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)        self.toolbar.addWidget(tb_Spacer)    def newFile_action(self):        childWindow = EditorWindow()        childWindow.show()        childWindow.statusBar().showMessage("New window", 2000)        #Need to be able to detect if file is opened in another window to prevent user from editing same document twice in 2 different windows.    def footerBar_init(self):        #May need to create an instance of statusBar in this function to add more widgets if needed.        self.statusBar().showMessage('LaTeX editor booted up!', 2000)        self.show()    def footerBar_setMessage(self, message, mSecs):        self.statusBar().showMessage(message, mSecs)        self.show()    #Code adapted from https://github.com/baoboa/pyqt5/blob/master/examples/mainwindows/recentfiles.py    #Start    def openFile_action(self):        fileName, _ = QFileDialog.getOpenFileName(self)        if fileName:            self.loadFile(fileName)        self.text.document().setModified(False)    def saveFile_action(self):        if self.currentFile:            self.save(self.currentFile)            self.text.document().setModified(False)        else:            self.saveAs()    def saveAs(self):        fileName, _ = QFileDialog.getSaveFileName(self)        if fileName:            self.save(fileName)            self.text.document().setModified(False)    def save(self, fileName):        file = QFile(fileName)        if not file.open( QFile.WriteOnly | QFile.Text):            QMessageBox.warning(self, "Recent Files",                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))            return        outstr = QTextStream(file)        QApplication.setOverrideCursor(Qt.WaitCursor)        outstr << self.text.toPlainText()        QApplication.restoreOverrideCursor()        self.setCurrentFile(fileName)        self.statusBar().showMessage("File saved", 1000)    def setCurrentFile(self, fileName):        self.currentFile = fileName        if self.currentFile:            self.setWindowTitle("LaTeX editor --- " + fileName)        else:            self.setWindowTitle("LaTeX editor")    def loadFile(self, fileName):        file = QFile(fileName)        if not file.open( QFile.ReadOnly | QFile.Text):            QMessageBox.warning(self, "Recent Files",                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))            return        instr = QTextStream(file)        QApplication.setOverrideCursor(Qt.WaitCursor)        self.text.setPlainText(instr.readAll())        QApplication.restoreOverrideCursor()        self.setCurrentFile(fileName)        self.statusBar().showMessage("File loaded", 2000)    #End    def about(self):        QMessageBox.about(self, "About LaTeX text editor...",                         "LaTeX text editor created by Matthew Lam. \                          \nGithub page: https://www.github.com/matthew-lam")    def redoAction(self):            self.text.redo()            redo_actionsLeft = self.text.document().availableRedoSteps()            self.footerBar_setMessage("Redo actions remaining on stack: " \                                        + str(redo_actionsLeft), 2000)    def findText_toolbar(self):        self.toolbar.addSeparator()        self.testing_QLineEdit = QLineEdit()        self.testing_QLineEdit.setPlaceholderText(" 🔍   Find text...")        self.testing_QLineEdit.setMaximumWidth(200)        self.toolbar.addWidget(self.testing_QLineEdit)        self.testing_QLineEdit.returnPressed.connect(lambda: self.findText())            def findText(self):        text_toFind = self.testing_QLineEdit.text()        textCursor = self.text.textCursor()        if text_toFind:            if self.text.find(text_toFind) == False and not textCursor.atStart():                textCursor.movePosition(QTextCursor.Start, QTextCursor.MoveAnchor, 1)                                self.text.setTextCursor(textCursor)            else:                self.text.document().find(text_toFind)        else:            self.footerBar_setMessage("Search bar is empty. Please enter a word to find.", 2000)    def previewTex(self):        #Compiles contents of current document into LaTeX format and then displays it on a preview window.        #Thread used to run function so GUI remains responsive due to non-blocking processing from multi-threading.        pathNameExt = os.path.splitext(self.currentFile)        copiedFile_name = pathNameExt[0] + '.tex'        if pathNameExt[0] == '':            invalidFile_message = QMessageBox()            invalidFile_message.setText("No file / invalid file referenced. \                \n\nPlease choose a valid .tex file to convert and preview as a PDF.")            invalidFile_message.exec_()        elif pathNameExt[1] != '.tex':            self.saveFile_action()            warning_message = QMessageBox()            warning_message.setText("File being previewed did not have a .tex extension.\                File was copied and file was changed to have a .tex extension.")            warning_message.exec_()            self.save(copiedFile_name)            print("File copied:" + self.currentFile + " -- and saved as: " + copiedFile_name)            self.workThread = previewUI.preview_thread(self)            self.workThread.start()            self.workThread.thread_message.connect(self.std_err_message)            self.workThread.returnCode.connect(self.get_returnCode)        else:            self.footerBar_setMessage("File being converted to viewable PDF .tex file.", 5000)            self.workThread = previewUI.preview_thread(self)            self.workThread.start()            self.workThread.thread_message.connect(self.std_err_message)            self.workThread.returnCode.connect(self.get_returnCode)    def std_err_message(self, message):        #executed when preview_thread.thread_message emits signal        thread_message = QMessageBox()        thread_message.setText(message)        thread_message.exec_()    def get_returnCode(self, returnCode):        if returnCode == 0:            self.testingdoc = previewUI.PreviewWindow(self, screenX/2, screenY/1.25)        else:            pass    def leftDock_sideBar(self):        #Initializes a dock widget to be used as a side bar.        dock = QDockWidget("LaTeX symbols and actions", self)        dock.setAllowedAreas(Qt.LeftDockWidgetArea)        #dock.setFeatures(QDockWidget.DockWidgetClosable)        dock.setFeatures(QDockWidget.NoDockWidgetFeatures)        dock.setMinimumSize(200, 0)        self.addDockWidget(Qt.LeftDockWidgetArea, dock)class WindowUtilityFunctions(QWidget):    def getScreenDims():        screenObj = app.primaryScreen()        screenSize = screenObj.size()        screenDims = screenObj.availableGeometry()        return screenDims    def getScreenSizeX(screenDims):        return screenDims.width()    def getScreenSizeY(screenDims):        return screenDims.height()    def setCenter(self):    #Probably will need to be moved to a different class / may be removed        windowProp = self.frameGeometry()        centerPosition = QDesktopWidget().availableGeometry().center()        windowProp.moveCenter(centerPosition)        self.move(windowProp.topLeft())    def setTopLeft(self):   #Probably will need to be moved to a different class        #Ensures that window is always set to the top left no matter the screen res        windowProp = self.frameGeometry()        topLeftPosition = QDesktopWidget().availableGeometry().topLeft()        windowProp.moveLeft(0)        self.move(windowProp.topLeft())       def setTopRight(self):   #Probably will need to be moved to a different class        #Ensures that window is always set to the top left no matter the screen res        windowProp = self.frameGeometry()        topRightPosition = QDesktopWidget().availableGeometry().topRight()        windowProp.moveCenter(topRightPosition)        self.move(windowProp.topRight())        def isMacOS():            try:            #Detects if OS is MacOS.                if platform.system() == "Darwin":                    print(platform.system() + " -- OS used is MacOS.")                    return True            except:                return False#Put this block of code into desired main file. mainWindow() is used as a constructor for creating windows.if __name__ == '__main__':    #Application main loop for event handling and continuous running of application.    print(fitz.__doc__)    app = QApplication(sys.argv)    screenDims = WindowUtilityFunctions.getScreenDims()       #Can use this variable to re-size preview tex window.    screenX = WindowUtilityFunctions.getScreenSizeX(screenDims)    screenY = WindowUtilityFunctions.getScreenSizeY(screenDims)    testWindow = EditorWindow()    sys.exit(app.exec_())